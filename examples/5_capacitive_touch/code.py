"""
JoystickXL capacitive touch example with 8 buttons and 1 hat switch.

MPR121 12-Key Capacitive Touch Sensor Breakout https://www.adafruit.com/product/1982

Requires the `adafruit_mpr121` and `adafruit_bus_device` libraries

Tested on an Adafruit ItsyBitsy M4 Express, but should work on other CircuitPython
boards with a sufficient quantity/type of pins.

* 3V, G, SCL, SDA from CircuitPython board to MPR121 board
* Buttons are on MPR121 inputs 0-7
* Hat Switch is on MPR121 inputs 8-11 (8=UP, 9=DOWN, 10=LEFT, 11=RIGHT)

Don't forget to copy boot.py from the example folder to your CIRCUITPY drive.
"""

import adafruit_mpr121
import board  # type: ignore (this is a CircuitPython built-in)
import busio  # type: ignore (this is a CircuitPython built-in)
from joystick_xl.inputs import Button, Hat
from joystick_xl.joystick import Joystick

# Set up I2C MPR121 capacitive touch sensor
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

# Set up JoystickXL!
js = Joystick()

# Add 8 buttons - no `source=Board.X` here, since we will be using the MPR121.
for _ in range(8):
    js.add_input(Button(active_low=False))

# Add a hat switch - again, no `Board.X` sources.
js.add_input(Hat(active_low=False))

while True:

    # Manually update the source values for our inputs using the MPR121.
    for i in range(8):
        js.button[i].source_value = mpr121[i].value
    js.hat[0].up.source_value = mpr121[8].value
    js.hat[0].down.source_value = mpr121[9].value
    js.hat[0].left.source_value = mpr121[10].value
    js.hat[0].right.source_value = mpr121[11].value

    # Update the joystick device
    js.update()
