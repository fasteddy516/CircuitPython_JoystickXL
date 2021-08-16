"""
JoystickXL Example #4 - GPIO Expander (8 buttons and 1 hat switch).

This example uses a Microchip MCP23017-E/SP I/O expander
(https://www.adafruit.com/product/732), and requires the `adafruit_mcp230xx` and
`adafruit_bus_device` libraries from the CircuitPython Library Bundle.

Tested on an Adafruit ItsyBitsy M4 Express, but should work on other CircuitPython
boards with a sufficient quantity/type of pins.

* 3V from CircuitPython board to MCP23017 Vdd and !Reset pins
* G from CircuitPython board to MCP23017 Vss and address (A0, A1, A2) pins
* SCL, SDA from CircuitPython board to MCP23017 (with 10k pull-up resistors)
* Buttons are on MCP23017 pins GPA0-GPA7
* Hat Switch is on MCP23017 pins GPB0-GPB3 (GPB0=UP, GPB1=DOWN, GPB2=LEFT, GPB3=RIGHT)

Don't forget to copy boot.py from the example folder to your CIRCUITPY drive.
"""


import board  # type: ignore (this is a CircuitPython built-in)
import busio  # type: ignore (this is a CircuitPython built-in)
import digitalio  # type: ignore (this is a CircuitPython built-in)
from adafruit_mcp230xx.mcp23017 import MCP23017
from joystick_xl.inputs import Button, Hat
from joystick_xl.joystick import Joystick

# Set up I2C MCP23017 I/O expander
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)

# JoystickXL doesn't know how to configure I/O pins on peripheral devices like it does
# with on-board pins, so we'll have to do the set up manually here.
for i in range(12):
    pin = mcp.get_pin(i)
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP

# Set up JoystickXL!
js = Joystick()

for i in range(8):
    js.add_input(Button(mcp.get_pin(i)))

js.add_input(
    Hat(
        up=mcp.get_pin(8),
        down=mcp.get_pin(9),
        left=mcp.get_pin(10),
        right=mcp.get_pin(11),
    )
)

while True:
    js.update()
