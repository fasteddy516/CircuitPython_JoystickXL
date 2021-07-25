"""
The base JoystickXL class for updating input states and sending USB HID reports.

This module provides the necessary functions to create a JoystickXL object,
retrieve its input counts, associate input objects and update its input states.
"""

import struct
import time

from joystick_xl.inputs import Axis, Button, Hat

# These typing imports help during development in vscode but fail in CircuitPython
try:
    from typing import Tuple, Union
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
    except (ImportError, AttributeError):
        _num_buttons = 64
        _num_axes = 8
        _num_hats = 4

    # reduce button count on platforms that don't handle 64-bit integers
    if _num_buttons > 24:
        try:
            i = 2 ** _num_buttons  # if this fails, the platform won't do 64-bit values
        except OverflowError:
            _num_buttons = 24

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

        self.button = list()
        """List of button inputs associated with this joystick."""

        self._button_states = 0
        for _ in range(int(self.num_buttons / 8)):
            self._format += "B"

        self.axis = list()
        """List of axis inputs associated with this joystick."""

        self._axis_states = list()
        for _ in range(self.num_axes):
            self._axis_states.append(0)
            self._format += "b"

        self.hat = list()
        """List of hat inputs associated with this joystick."""

        self._hat_states = list()
        for i in range(self.num_hats):
            self._hat_states.append(8)
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

    def add_input(self, *input: Union[Axis, Button, Hat]) -> None:
        """
        Associate one or more axis, button or hat inputs with the joystick.

        The provided input(s) are automatically added to the ``axis``, ``button`` and
        ``hat`` lists based on their type.  The order in which inputs are added will
        determine their index/reference number. (i.e., the first button object that is
        added will be ``Joystick.button[0]`` and will correspond to ``Button 1`` on
        the host device.)  Inputs of all types can be added at the same time.

        :param input: One or more ``Axis``, ``Button`` or ``Hat`` objects.
        :type input: Union[Axis, Button, Hat]
        :raises TypeError: If an object that is not an ``Axis``, ``Button`` or ``Hat``
            is passed in.
        :raises OverflowError: If an attempt is made to add more than the available
            number of axes, buttons or hat switches to the respective list.
        """
        for i in input:
            if isinstance(i, Axis):
                if len(self.axis) < self._num_axes:
                    self.axis.append(i)
                else:
                    raise OverflowError("List is full, cannot add another axis.")
            elif isinstance(i, Button):
                if len(self.button) < self._num_buttons:
                    self.button.append(i)
                else:
                    raise OverflowError("List is full, cannot add another button.")
            elif isinstance(i, Hat):
                if len(self.hat) < self._num_hats:
                    self.hat.append(i)
                else:
                    raise OverflowError("List is full, cannot add another hat switch.")
            else:
                raise TypeError("Input must be a Button, Axis or Hat object.")

    def update(self, always: bool = False) -> None:
        """
        Update all inputs in associated input lists, generate a USB HID report and send
        it to the host if necessary.

        :param always: When ``True``, send a report even if it is identical to the last
           report that was sent out.  Defaults to ``False``.
        :type always: bool, optional
        """
        # Update button states but defer USB HID report generation.
        if len(self.button):
            button_values = [(i, b.value) for i, b in enumerate(self.button)]
            self.update_button(*button_values, defer=True)

        # Update axis values but defer USB HID report generation.
        if len(self.axis):
            axis_values = [(i, a.value) for i, a in enumerate(self.axis)]
            self.update_axis(*axis_values, defer=True)

        # Update hat switch values, but defer USB HID report generation.
        if len(self.hat):
            hat_values = [(i, h.value) for i, h in enumerate(self.hat)]
            self.update_hat(*hat_values, defer=True)

        # Generate a USB HID report.
        report_data = list()

        for i in range(self.num_buttons // 8):
            report_data.append((self._button_states >> (i * 8)) & 0xFF)

        report_data.extend(self._axis_states)

        for i in range(self.num_hats - 1, 0, -2):
            report_data.append(
                ((self._hat_states[i - 1] << 4) | (self._hat_states[i])) & 0xFF
            )

        struct.pack_into(self._format, self._report, 0, *report_data)

        # Send the USB HID report if required.
        if always or self._last_report != self._report:
            self._device.send_report(self._report)
            self._last_report[:] = self._report

    def reset_all(self) -> None:
        """Reset all inputs to their resting states."""
        self._button_states = 0
        for i in range(self.num_axes):
            self._axis_states[i] = 0
        for i in range(self.num_hats):
            self._hat_states[i] = 8
        self.update(always=True)

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

        .. note::

           ``update_button`` is called automatically for any button objects added to the
           built in ``Joystick.button[]`` list when ``Joystick.update()`` is called.
        """
        for b, value in button:
            if self._validate_button_number(b):
                if value:
                    self._button_states |= 1 << b
                else:
                    self._button_states &= ~(1 << b)
        if not defer:
            self.update()

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

        .. note::

           ``update_axis`` is called automatically for any axis objects added to the
           built in ``Joystick.axis[]`` list when ``Joystick.update()`` is called.
        """
        for a, value in axis:
            if self._validate_axis_value(a, value):
                self._axis_states[a] = value
        if not defer:
            self.update()

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

        .. note::

           ``update_hat`` is called automatically for any hat switch objects added to
           the built in ``Joystick.hat[]`` list when ``Joystick.update()`` is called.
        """
        for h, value in hat:
            if self._validate_hat_value(h, value):
                self._hat_states[h] = value
        if not defer:
            self.update()
