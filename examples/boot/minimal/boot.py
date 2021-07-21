"""JoystickXL minimal boot.py."""

import usb_hid  # type: ignore
from joystick_xl.hid import create_joystick

# This will enable a joystick USB HID device.  All other standard CircuitPython USB HID
# devices (keyboard, mouse, consumer control) will be disabled.
usb_hid.enable((create_joystick(),))
