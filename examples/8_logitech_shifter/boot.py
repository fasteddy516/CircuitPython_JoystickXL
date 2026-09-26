"""JoystickXL standard boot.py."""

import usb_hid  # type: ignore (this is a CircuitPython built-in)
from joystick_xl.hid import create_joystick

# This will enable all of the standard CircuitPython USB HID devices along with
# a USB HID joystick. At least two are required for reliable Linux support,
# according to the documentation.
usb_hid.enable(
    (
        usb_hid.Device.KEYBOARD,
        usb_hid.Device.MOUSE,
        usb_hid.Device.CONSUMER_CONTROL,
        create_joystick(axes=2, buttons=7, hats=0),
    )
)
