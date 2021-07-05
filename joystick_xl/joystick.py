"""Put a docstring here."""
import struct
import time

try:
    from typing import Tuple, Union
except ImportError:
    pass

import usb_hid

# from typing import Tuple, Union


class Joystick:
    """Put a docstring here."""

    try:
        from . import config

        _num_buttons = config.buttons
        _num_axes = config.axes
        _num_hats = config.hats
    except ImportError:
        _num_buttons = 64
        _num_axes = 8
        _num_hats = 4

    _axes = {"x": 0, "y": 1, "z": 2, "rx": 3, "ry": 4, "rz": 5, "s0": 6, "s1": 7}
    _hats = {"h1": 0, "h2": 1, "h3": 2, "h4": 3}

    @property
    def num_buttons(self) -> int:
        """Return the number of configured buttons."""
        return self._num_buttons

    @property
    def num_axes(self) -> int:
        """Return the number of configured axes."""
        return self._num_axes

    @property
    def num_hats(self) -> int:
        """Return the number of configured hat switches.."""
        return self._num_hats

    @property
    def report_size(self) -> int:
        """Return the length (in bytes) of an outgoing usb-hid report."""
        return self.num_buttons // 8 + self.num_axes + self.num_hats // 2

    @staticmethod
    def _get_axis(axis: str) -> int:
        try:
            return Joystick._axes[axis.lower()]
        except KeyError:
            raise ValueError(f"'{axis}' is not a valid axis name.")

    @staticmethod
    def _get_hat(hat: str) -> int:
        try:
            return Joystick._hats[hat.lower()]
        except KeyError:
            raise ValueError(f"'{hat}' is not a valid hat switch name.")

    @staticmethod
    def find_device() -> usb_hid.Device:
        for device in usb_hid.devices:
            if (
                device.usage_page == 0x01
                and device.usage == 0x04
                and hasattr(device, "send_report")
            ):
                return device
        raise ValueError("Could not find JoystickXL HID device.")

    def __init__(self) -> None:
        """Put a docstring here."""
        self._device = self.find_device()
        self._report = bytearray(self.report_size)
        self._last_report = bytearray(self.report_size)
        self._buttons = 0
        self._format = "<"
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

    def reset_all(self) -> None:
        self._buttons = 0
        for i in range(self.num_axes):
            self._axis[i] = 0
        for i in range(self.num_hats):
            self._hat[i] = 8
        self._send(always=True)

    def _send(self, always: bool = False) -> None:
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

    @staticmethod
    def _validate_button_number(button: int) -> bool:
        if Joystick._num_buttons == 0:
            raise ValueError("There are no buttons configured.")
        if not 1 <= button <= Joystick._num_buttons:
            raise ValueError(f"Button must be in range 1 to {Joystick._num_buttons}")
        return True

    @staticmethod
    def _validate_axis_value(axis: int, value: int) -> bool:
        if Joystick._num_axes == 0:
            raise ValueError("There are no axes configured.")
        if axis + 1 > Joystick._num_axes:
            raise ValueError("Specified axis is out of range.")
        if not -127 <= value <= 127:
            raise ValueError("Axis value must be in range -127 to 127")
        return True

    @staticmethod
    def _validate_hat_value(hat: int, position: int) -> bool:
        if Joystick._num_hats == 0:
            raise ValueError("There are no hats configured.")
        if hat + 1 > Joystick._num_hats:
            raise ValueError("Specified hat is out of range.")
        if not 0 <= position <= 8:
            raise ValueError("Hat value must be in range 0 to 8")
        return True

    def press_buttons(self, *buttons: int) -> None:
        for button in buttons:
            if self._validate_button_number(button):
                self._buttons |= 1 << button - 1
        self._send()

    def release_buttons(self, *buttons: int) -> None:
        for button in buttons:
            if self._validate_button_number(button):
                self._buttons &= ~(1 << button - 1)
        self._send()

    def release_all_buttons(self) -> None:
        self._buttons = 0
        self._send()

    def click_buttons(self, *buttons: int) -> None:
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def move_axes(self, *axes: Tuple[Union[int, str], int]) -> None:
        for axis, position in axes:
            if isinstance(axis, str):
                axis = self._get_axis(axis)
            if self._validate_axis_value(axis, position):
                self._axis[axis] = position
        self._send()

    def move_hats(self, *hats: Tuple[Union[int, str], int]) -> None:
        for hat, position in hats:
            if isinstance(hat, str):
                hat = self._get_hat(hat)
            if self._validate_hat_value(hat, position):
                self._hat[hat] = position
        self._send()
