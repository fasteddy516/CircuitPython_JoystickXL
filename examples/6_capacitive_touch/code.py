"""
JoystickXL Example #6 - Capacitive Touch (8 buttons and 1 hat switch).

This example uses an MPR121 12-Key Capacitive Touch Sensor Breakout
(https://www.adafruit.com/product/1982), and requires the `adafruit_mpr121` and
`adafruit_bus_device` libraries from the CircuitPython Library Bundle.

Tested on an Adafruit Metro M4 Express, but should work on other CircuitPython
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

# The MPR121 library returns True when a capacitive touch channel is activated.  This
# makes it "active high", so we set `active_low` to False
for i in range(8):
    js.add_input(Button(mpr121[i], active_low=False))

js.add_input(
    Hat(
        up=mpr121[8],
        down=mpr121[9],
        left=mpr121[10],
        right=mpr121[11],
        active_low=False,
    )
)

while True:
    js.update()
