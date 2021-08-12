"""
JoystickXL Example #1 - Start Simple (2 axes, 2 buttons, 1 hat switch).

Tested on an Adafruit ItsyBitsy M4 Express, but should work on other CircuitPython
boards with a sufficient quantity/type of pins.

* Buttons are on pins D9 and D10
* Axes are on pins A2 and A3
* Hat switch is on pins D2 (up), D3 (down), D4 (left) and D7 (right)

Don't forget to copy boot.py from the example folder to your CIRCUITPY drive.
"""

import board  # type: ignore (this is a CircuitPython built-in)
from joystick_xl.inputs import Axis, Button, Hat
from joystick_xl.joystick import Joystick

joystick = Joystick()

joystick.add_input(
    Button(board.D9),
    Button(board.D10),
    Axis(board.A2),
    Axis(board.A3),
    Hat(up=board.D2, down=board.D3, left=board.D4, right=board.D7),
)

while True:
    joystick.update()
