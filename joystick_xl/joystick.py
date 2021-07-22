"""
The base JoystickXL class for updating input states and sending USB HID reports.

This module provides the necessary functions to create a JoystickXL object,
retrieve its input counts and update its input states.
"""

import struct
import time

# These typing imports help during development in vscode but fail in CircuitPython
try:
    from typing import Tuple
except ImportError:
    pass

import usb_hid  # type: ignore (this is a CircuitPython built-in)


class Joystick:
    """Base JoystickXL class for updating input states and sending USB HID reports."""

    # Use custom input count configuration if it exists, otherwise use defaults.
    try:
        from . import config  # type: ignore (config file is optional and may not exist)

        _num_buttons = config.buttons
        _num_axes = config.axes
        _num_hats = config.hats
    except ImportError:
        _num_buttons = 64
        _num_axes = 8
        _num_hats = 4

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
    def _validate_button_number(button: int) -> bool:
        """
        Ensure the supplied button index is valid.

        :param button: The 0-based index of the button to validate.
        :type button: int
        :raises ValueError: No buttons are configured for the JoystickXL device.
        :raises ValueError: The supplied button index is out of range.
        :return: ``True`` if the supplied button index is valid.
        :rtype: bool
        """
        if Joystick._num_buttons == 0:
            raise ValueError("There are no buttons configured.")
        if not 0 <= button <= Joystick._num_buttons - 1:
            raise ValueError("Specified button is out of range.")
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

    def update_button(
        self,
        *button: Tuple[int, int],
        defer: bool = False,
    ) -> None:
        """
        Update the value of one or more button input(s).

        :param button: One or more tuples containing a button index (0-based) and
           value (``True`` if pressed, ``False`` if released).
        :type button: Tuple[int, int]
        :param defer: When ``True``, prevents sending a USB HID report upon completion.
           Defaults to ``False``.
        :type defer: bool

        .. code::

           # Update a single button
           update_button((0, True))  # 0 = b1

           # Updates multiple buttons
           update_button((1, False), (7, True))  # 1 = b2, 7 = b8
        """
        for b, value in button:
            if self._validate_button_number(b):
                if value:
                    self._buttons |= 1 << b
                else:
                    self._buttons &= ~(1 << b)
        if not defer:
            self._send()

    def update_axis(
        self,
        *axis: Tuple[int, int],
        defer: bool = False,
    ) -> None:
        """
        Update the value of one or more axis input(s).

        :param axis: One or more tuples containing an axis index (0-based) and value
           (``-127`` to ``127``, with ``0`` indicating the axis is at rest/centered).
        :type axis: Tuple[int, int]
        :param defer: When ``True``, prevents sending a USB HID report upon completion.
           Defaults to ``False``.
        :type defer: bool

        .. code::

           # Updates a single axis
           update_axis((0, -121))  # 0 = x-axis

           # Updates multiple axes
           update_axis((1, 22), (3, -42))  # 1 = y-axis, 3 = rx-axis
        """
        for a, value in axis:
            if self._validate_axis_value(a, value):
                self._axis[a] = value
        if not defer:
            self._send()

    def update_hat(
        self,
        *hat: Tuple[int, int],
        defer: bool = False,
    ) -> None:
        """
        Update the value of one or more hat switch input(s).

        :param hat: One or more tuples containing a hat switch index (0-based) and
           value.  Valid hat switch values range from ``0`` to ``8`` as follows:

              * ``0`` = UP
              * ``1`` = UP + RIGHT
              * ``2`` = RIGHT
              * ``3`` = DOWN + RIGHT
              * ``4`` = DOWN
              * ``5`` = DOWN + LEFT
              * ``6`` = LEFT
              * ``7`` = UP + LEFT
              * ``8`` = IDLE

        :type hat: Tuple[int, int]
        :param defer: When ``True``, prevents sending a USB HID report upon completion.
           Defaults to ``False``.
        :type defer: bool

        .. code::

           # Updates a single hat switch
           update_hat((0, 3))  # 0 = h1

           # Updates multiple hat switches
           update_hat((1, 8), (3, 1))  # 1 = h2, 3 = h4
        """
        for h, value in hat:
            if self._validate_hat_value(h, value):
                self._hat[h] = value
        if not defer:
            self._send()
