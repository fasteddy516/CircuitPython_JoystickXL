"""
JoystickXL basic example with 2 axes, 2 buttons, 1 hat switch.

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

b1 = Button(board.D9)
b2 = Button(board.D10)
x = Axis(board.A2)
y = Axis(board.A3)
h = Hat(up=board.D2, down=board.D3, left=board.D4, right=board.D7)

while True:
    joystick.update_button((0, b1.value), (1, b2.value))
    joystick.update_axis((0, x.value), (1, y.value))
    joystick.update_hat((0, h.value))
