"""
JoystickXL Example #5 - External Analog-to-Digital Converter (8 axes).

This example uses a Microchip MCP3008-I/P analog-to-digital converter
(https://www.adafruit.com/product/856), and requires the `adafruit_mcp3xxx` and
`adafruit_bus_device` libraries from the CircuitPython Library Bundle.

Tested on an Adafruit ItsyBitsy M4 Express, but should work on other CircuitPython
boards with a sufficient quantity/type of pins.

* 3V from CircuitPython board to MCP3008 Vdd and Vref
* G from CircuitPython board to MCP3008 AGND and DGND
* MOSI from CircuitPython board to MCP3008 Din
* MISO from CircuitPython board to MCP3008 Dout
* SCK from CircuitPython board to MCP3008 CLK
* D7 from CircuitPython board to MCP3008 !CS/SHDN
* Axes are on MCP3008 pins CH0-CH7

Don't forget to copy boot.py from the example folder to your CIRCUITPY drive.
"""

import adafruit_mcp3xxx.mcp3008 as MCP
import board  # type: ignore (this is a CircuitPython built-in)
import busio  # type: ignore (this is a CircuitPython built-in)
import digitalio  # type: ignore (this is a CircuitPython built-in)
from adafruit_mcp3xxx.analog_in import AnalogIn
from joystick_xl.inputs import Axis
from joystick_xl.joystick import Joystick

# Set up SPI MCP3008 Analog-to-Digital converter
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D7)
mcp = MCP.MCP3008(spi, cs)

# Set up JoystickXL!
js = Joystick()

js.add_input(
    Axis(AnalogIn(mcp, MCP.P0)),
    Axis(AnalogIn(mcp, MCP.P1)),
    Axis(AnalogIn(mcp, MCP.P2)),
    Axis(AnalogIn(mcp, MCP.P3)),
    Axis(AnalogIn(mcp, MCP.P4)),
    Axis(AnalogIn(mcp, MCP.P5)),
    Axis(AnalogIn(mcp, MCP.P6)),
    Axis(AnalogIn(mcp, MCP.P7)),
)

while True:
    js.update()
