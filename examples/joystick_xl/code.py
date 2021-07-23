"""
JoystickXL advanced example with 8 axes, 24 buttons, 4 hat switches.

Tested on an Adafruit Grand Central M4 Express, but should work on other CircuitPython
boards with a sufficient quantity/type of pins.

* Buttons are on pins D9, D10, D11 and D12
* Axes are on pins A2 and A3
* Hat switch is on pins D2 (up), D3 (down), D4 (left) and D7 (right)

Don't forget to copy boot.py from the example folder to your CIRCUITPY drive.
"""

import board  # type: ignore (this is a CircuitPython built-in)

from joystick_xl.helpers import Axis, Button, Hat
from joystick_xl.joystick import Joystick

joystick = Joystick()

buttons = [
    Button(board.D22),
    Button(board.D23),
    Button(board.D24),
    Button(board.D25),
    Button(board.D26),
    Button(board.D27),
    Button(board.D28),
    Button(board.D29),
    Button(board.D30),
    Button(board.D31),
    Button(board.D32),
    Button(board.D33),
    Button(board.D34),
    Button(board.D35),
    Button(board.D36),
    Button(board.D37),
    Button(board.D38),
    Button(board.D39),
    Button(board.D40),
    Button(board.D41),
    Button(board.D42),
    Button(board.D43),
    Button(board.D44),
    Button(board.D45),
]

axes = [
    Axis(board.A8),
    Axis(board.A9),
    Axis(board.A10),
    Axis(board.A11),
    Axis(board.A12),
    Axis(board.A13),
    Axis(board.A14),
    Axis(board.A15),
]

hats = [
    Hat(up=board.D2, down=board.D3, left=board.D4, right=board.D5),
    Hat(up=board.D6, down=board.D7, left=board.D8, right=board.D9),
    Hat(up=board.D14, down=board.D15, left=board.D16, right=board.D17),
    Hat(up=board.D18, down=board.D19, left=board.D20, right=board.D21),
]

while True:
    # update button states, defer usb hid report
    button_values = [(i, b.value) for i, b in enumerate(buttons)]
    joystick.update_button(*button_values, defer=True)

    # update axis values, defer usb hid report
    axis_values = [(i, a.value) for i, a in enumerate(axes)]
    joystick.update_axis(*axis_values, defer=True)

    # update hat switch values, send usb hid report when done
    hat_values = [(i, h.value) for i, h in enumerate(hats)]
    joystick.update_hat(*hat_values)
