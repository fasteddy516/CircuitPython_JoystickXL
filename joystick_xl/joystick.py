"""
Base JoystickXL class for updating input states and sending USB HID reports.

This module provides the necessary functions to create a JoystickXL object,
retrieve its input counts and update its input states.
"""

import struct
import time

# These typing imports help during development in vscode but fail in CircuitPython
try:
    from typing import Tuple, Union
except ImportError:
    pass

import usb_hid  # type: ignore


class Joystick:
    """Base JoystickXL class for updating input states and sending USB HID reports."""

    # Use custom input count configuration if it exists, otherwise use defaults.
    try:
        from . import config  # type: ignore

        _num_buttons = config.buttons
        _num_axes = config.axes
        _num_hats = config.hats
    except ImportError:
        _num_buttons = 64
        _num_axes = 8
        _num_hats = 4

    # Dictionaries to map fiendly names to i/o indices.
    _axes = {"x": 0, "y": 1, "z": 2, "rx": 3, "ry": 4, "rz": 5, "s0": 6, "s1": 7}
    _hats = {"h1": 0, "h2": 1, "h3": 2, "h4": 3}

    @property
    def num_buttons(self) -> int:
        """Return the number of available buttons in the USB HID descriptor."""
        return self._num_buttons

    @property
    def num_axes(self) -> int:
        """Return the number of available axes in the USB HID descriptor."""
        return self._num_axes

    @property
    def num_hats(self) -> int:
        """Return the number of available hat switches in the USB HID descriptor."""
        return self._num_hats

    @property
    def _report_size(self) -> int:
        """Return the length (in bytes) of an outgoing USB HID report."""
        return self.num_buttons // 8 + self.num_axes + self.num_hats // 2

    def __init__(self) -> None:
        """
        Create a JoystickXL object with all inputs at rest.

        .. code::

           from joystick_xl.joystick import Joystick

           js = Joystick()

        .. note:: A JoystickXL ``usb_hid.Device`` object has to be created in
           ``boot.py`` before creating a ``Joystick()`` object in ``code.py``,
           otherwise an exception will be thrown.
        """
        self._device = self._find_device()
        self._report = bytearray(self._report_size)
        self._last_report = bytearray(self._report_size)
        self._format = "<"

        self._buttons = 0
        for _ in range(int(self.num_buttons / 8)):
            self._format += "B"

        self._axis = list()
        for _ in range(self.num_axes):
            self._axis.append(0)
            self._format += "b"

        self._hat = list()
        for i in range(self.num_hats):
            self._hat.append(8)
            if (i + 1) % 2 == 0:
                self._format += "B"

        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    @staticmethod
    def _find_device() -> usb_hid.Device:
        """Find a JoystickXL device in the list of active USB HID devices."""
        for device in usb_hid.devices:
            if (
                device.usage_page == 0x01
                and device.usage == 0x04
                and hasattr(device, "send_report")
            ):
                return device
        raise ValueError("Could not find JoystickXL HID device - check boot.py.)")

    @staticmethod
    def _get_axis(axis: str) -> int:
        """Map a friendly axis name <str> to a list index <int>."""
        try:
            return Joystick._axes[axis.lower()]
        except KeyError:
            raise ValueError(f"'{axis}' is not a valid axis name.")

    @staticmethod
    def _get_hat(hat: str) -> int:
        """Map a friendly hat switch name <str> to a list index <int>."""
        try:
            return Joystick._hats[hat.lower()]
        except KeyError:
            raise ValueError(f"'{hat}' is not a valid hat switch name.")

    @staticmethod
    def _validate_button_number(button: int) -> bool:
        """
        Ensure the supplied button index is valid.

        :param button: The 1-based index of the button to validate.
        :type button: int
        :raises ValueError: No buttons are configured for the JoystickXL device.
        :raises ValueError: The supplied button index is out of range.
        :return: ``True`` if the supplied button index is valid.
        :rtype: bool
        """
        if Joystick._num_buttons == 0:
            raise ValueError("There are no buttons configured.")
        if not 1 <= button <= Joystick._num_buttons:
            raise ValueError(f"Button must be in range 1 to {Joystick._num_buttons}")
        return True

    @staticmethod
    def _validate_axis_value(axis: int, value: int) -> bool:
        """
        Ensure the supplied axis index and value are valid.

        :param axis: The 0-based index of the axis to validate.
        :type axis: int
        :param value: The axis value to validate.
        :type value: int
        :raises ValueError: No axes are configured for the JoystickXL device.
        :raises ValueError: The supplied axis index is out of range.
        :raises ValueError: The supplied axis value is out of range.
        :return: ``True`` if the supplied axis index and value are valid.
        :rtype: bool
        """
        if Joystick._num_axes == 0:
            raise ValueError("There are no axes configured.")
        if axis + 1 > Joystick._num_axes:
            raise ValueError("Specified axis is out of range.")
        if not -127 <= value <= 127:
            raise ValueError("Axis value must be in range -127 to 127")
        return True

    @staticmethod
    def _validate_hat_value(hat: int, position: int) -> bool:
        """
        Ensure the supplied hat switch index and position are valid.

        :param hat: The 0-based index of the hat switch to validate.
        :type hat: int
        :param value: The hat switch position to validate.
        :type value: int
        :raises ValueError: No hat switches are configured for the JoystickXL device.
        :raises ValueError: The supplied hat switch index is out of range.
        :raises ValueError: The supplied hat switch position is out of range.
        :return: ``True`` if the supplied hat switch index and position are valid.
        :rtype: bool
        """
        if Joystick._num_hats == 0:
            raise ValueError("There are no hat switches configured.")
        if hat + 1 > Joystick._num_hats:
            raise ValueError("Specified hat is out of range.")
        if not 0 <= position <= 8:
            raise ValueError("Hat value must be in range 0 to 8")
        return True

    def _send(self, always: bool = False) -> None:
        """
        Generate a USB HID report and send it to the host if necessary.

        :param always: When ``True``, send a report even if it is identical to the last
           report that was sent out.  Defaults to ``False``.
        :type always: bool, optional
        """
        report_data = list()

        for i in range(self.num_buttons // 8):
            report_data.append((self._buttons >> (i * 8)) & 0xFF)

        report_data.extend(self._axis)

        for i in range(self.num_hats - 1, 0, -2):
            report_data.append(((self._hat[i - 1] << 4) | (self._hat[i])) & 0xFF)

        struct.pack_into(self._format, self._report, 0, *report_data)

        if always or self._last_report != self._report:
            self._device.send_report(self._report)
            self._last_report[:] = self._report

    def reset_all(self) -> None:
        """Reset all inputs to their resting states."""
        self._buttons = 0
        for i in range(self.num_axes):
            self._axis[i] = 0
        for i in range(self.num_hats):
            self._hat[i] = 8
        self._send(always=True)

    def press_buttons(self, *buttons: int) -> None:
        """Press stuff."""
        for button in buttons:
            if self._validate_button_number(button):
                self._buttons |= 1 << button - 1
        self._send()

    def release_buttons(self, *buttons: int) -> None:
        """Release stuff."""
        for button in buttons:
            if self._validate_button_number(button):
                self._buttons &= ~(1 << button - 1)
        self._send()

    def release_all_buttons(self) -> None:
        """Release all stuff."""
        self._buttons = 0
        self._send()

    def click_buttons(self, *buttons: int) -> None:
        """Press then release stuff."""
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def move_axes(
        self,
        *axes: Tuple[Union[int, str], int],
        defer: bool = False,
    ) -> None:
        """
        Update the value of one or more axis input(s).

        :param axes: One or more Tuples containing an axis index and value.  The axis
           index can be the 0-based index:

              .. code::

                 move_axes((0, -127), (1, 61))

           or can use an axis name:

              .. code::

                 move_axes(("x", -127), ("y", 61))

           Valid axis names are ``x``, ``y``, ``z``, ``rx``, ``ry``, ``rz``, ``s0``
           and ``s1``.  Valid axis values range from ``-127`` to ``127``, with ``0``
           indicating the axis is at rest (centered).
        :type axes: Tuple[int, int] or Tuple[str, int]
        :param defer: When ``True``, prevents sending a USB HID report upon completion.
           Defaults to ``False``.
        :type defer: bool
        """
        for axis, position in axes:
            if isinstance(axis, str):
                axis = self._get_axis(axis)
            if self._validate_axis_value(axis, position):
                self._axis[axis] = position
        if not defer:
            self._send()

    def move_hats(
        self,
        *hats: Tuple[Union[int, str], int],
        defer: bool = False,
    ) -> None:
        """
        Update the value of one or more hat switch input(s).

        :param hats: One or more Tuples containing a hat switch index and position.  The
           hat switch index can be the 0-based index:

              .. code::

                 move_hats((0, 1), (1, 8))

           or can use a hat switch name:

              .. code::

                 move_axes(("h1", 1), ("h2", 8))

           Valid hat switch names are ``h1``, ``h2``, ``h3`` and ``h4``.  Valid hat
           switch values range from ``0`` to ``8`` as follows:

              * ``0`` = UP
              * ``1`` = UP + RIGHT
              * ``2`` = RIGHT
              * ``3`` = DOWN + RIGHT
              * ``4`` = DOWN
              * ``5`` = DOWN + LEFT
              * ``6`` = LEFT
              * ``7`` = UP + LEFT
              * ``8`` = IDLE

        :type hats: Tuple[int, int] or Tuple[str, int]
        :param defer: When ``True``, prevents sending a USB HID report upon completion.
           Defaults to ``False``.
        :type defer: bool
        """
        for hat, position in hats:
            if isinstance(hat, str):
                hat = self._get_hat(hat)
            if self._validate_hat_value(hat, position):
                self._hat[hat] = position
        if not defer:
            self._send()
