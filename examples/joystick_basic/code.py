"""
JoystickXL basic example with 2 axes, 4 buttons, 1 hat switch.

(Don't forget to also copy boot.py from the example folder to your CIRCUITPY drive!)
"""

import analogio
import board
import digitalio
from joystick_xl.helpers import Axis, Hat
from joystick_xl.joystick import Joystick

joystick = Joystick()

buttons = [
    digitalio.DigitalInOut(board.D2),
    digitalio.DigitalInOut(board.D3),
    digitalio.DigitalInOut(board.D4),
    digitalio.DigitalInOut(board.D5),
]

for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

x = Axis(analogio.AnalogIn(board.A2))
y = Axis(analogio.AnalogIn(board.A3))
h = Hat(up=board.D6, down=board.D7, left=board.D8, right=board.D9)

while True:

    for i, button in enumerate(buttons, start=1):
        if button.value:
            joystick.release_buttons(i)
        else:
            joystick.press_buttons(i)

    joystick.move_hats(("h1", h.update()))
    joystick.move_axes(("x", x.update()), ("y", y.update()))
