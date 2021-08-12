"""
JoystickXL Example #6 - HOTAS (Hands On Throttle And Stick) Stick Component.

Tested on an Adafruit Grand Central M4 Express, but should work on other CircuitPython
boards with a sufficient quantity/type of pins.

* Stick buttons are on pins D22-D37
* Stick axes are on pins A8-A11
* Stick hat switches are on pins D14-D21

The stick board needs to be connected to the throttle board as follows:

* Stick TX to Throttle RX
* Stick RX to Throttle TX
* Stick GND to Throttle GND

Don't forget to copy boot.py from the example folder to your CIRCUITPY drive.
"""

import struct

import board  # type: ignore (This is a CircuitPython built-in)
import busio  # type: ignore (This too!)
from joystick_xl.inputs import Axis, Button, Hat
from joystick_xl.joystick import Joystick

# Prepare serial (UART) comms to communicate with throttle component.
uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0.1)

# Serial protocol constants.
STX = 0x02  # start-of-transmission
ETX = 0x03  # end-of-transmission
REQ = 0x05  # data request

# Axis configuration constants
AXIS_DB = 2500  # Deadband to apply to axis center points.
AXIS_MIN = 250  # Minimum raw axis value.
AXIS_MAX = 65285  # Maximum raw axis value.

# Prepare USB HID HOTAS device.
hotas = Joystick()

hotas.add_input(
    # The first 16 buttons are local I/O associated with the stick component, which
    # connects to the host via USB.
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
    # The last set of 16 buttons are virtual I/O associated with the throttle
    # component, which connects to the stick component via serial.
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    Button(),
    # The first 4 axes are local I/O associated with the stick component.
    Axis(board.A8, deadband=AXIS_DB, min=AXIS_MIN, max=AXIS_MAX),
    Axis(board.A9, deadband=AXIS_DB, min=AXIS_MIN, max=AXIS_MAX),
    Axis(board.A10, deadband=AXIS_DB, min=AXIS_MIN, max=AXIS_MAX),
    Axis(board.A11, deadband=AXIS_DB, min=AXIS_MIN, max=AXIS_MAX),
    # The last 4 axes are virtual I/O associated with the throttle component.
    Axis(deadband=AXIS_DB, min=AXIS_MIN, max=AXIS_MAX),
    Axis(deadband=AXIS_DB, min=AXIS_MIN, max=AXIS_MAX),
    Axis(deadband=AXIS_DB, min=AXIS_MIN, max=AXIS_MAX),
    Axis(deadband=AXIS_DB, min=AXIS_MIN, max=AXIS_MAX),
    # The first 2 hat switches are local I/O associated with the stick component.
    Hat(up=board.D14, down=board.D15, left=board.D16, right=board.D17),
    Hat(up=board.D18, down=board.D19, left=board.D20, right=board.D21),
    # The last 2 hat switches are virtual I/O associated with the throttle component.
    Hat(),
    Hat(),
)

# Stick and Throttle input processing loop.
while True:

    # Request raw state data from the throttle component.
    uart.write(bytearray((STX, REQ, ETX)))

    # we're looking for exactly 15 bytes of data from the throttle:
    #   Byte  0    = STX
    #   Byte  1    = REQ
    #   Bytes 2-3  = 16 bits of button data
    #   Bytes 4-11 = 4 x 16 bits of axis data
    #   Byte  12   = 2 x 4 bits of hat switch data
    #   Byte  13   = Checkbyte (for rudimentary error checking)
    #   Byte  14   = ETX
    rx = uart.read(15)

    if rx is not None and len(rx) == 15:

        # Calculate correct checkbyte value by XORing all command and data bytes.
        # Framing bytes (STX/ETX) and the incoming checkbyte are excluded.
        checkbyte = 0x00
        for b in rx[1:13]:
            checkbyte ^= b

        # Continue processing if framing and checkbyte are correct.
        if rx[0] == STX and rx[14] == ETX and rx[13] == checkbyte:

            # At this point there is only one 'command' to process - a data request.
            if rx[1] == REQ:

                # Unpack raw data.
                data = struct.unpack_from("<HHHHHB", rx, offset=2)

                # Update button virtual inputs with raw states from throttle.
                for i in range(16):
                    hotas.button[i + 16].source_value = (data[0] >> i) & 0x01

                # Update axis virtual inputs with raw states from throttle.
                for i in range(4):
                    hotas.axis[i + 4].source_value = data[1 + i]

                # update hat switch virtual inputs with raw states from throttle.
                for i in range(2):
                    hotas.hat[i + 2].unpack_source_values(data[5] >> (4 * i))

    # At this point we have collected all remote data and can update everything.
    hotas.update()
