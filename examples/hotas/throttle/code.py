"""
JoystickXL HOTAS (Hands On Throttle And Stick) Example - Throttle Component.

Tested on an Adafruit Grand Central M4 Express, but should work on other CircuitPython
boards with a sufficient quantity/type of pins.

* Throttle buttons are on pins D22-D37
* Throttle axes are on pins A8-A11
* Throttle hat switches are on pins D14-D21

The throttle board needs to be connected to the stick board as follows:

* Throttle TX to Stick RX
* Throttle RX to Stick TX
* Throttle GND to Stick GND

You don't need to copy boot.py to the throttle component - all USB HID communication
is handled by the stick component.
"""

import struct

import board  # type: ignore (This is a CircuitPython built-in)
import busio  # type: ignore (This too!)
from joystick_xl.inputs import Axis, Button, Hat

# Prepare serial (UART) comms to communicate with stick component.
uart = busio.UART(board.TX, board.RX, baudrate=115200)

# Serial protocol constants.
STX = 0x02  # start-of-transmission
ETX = 0x03  # end-of-transmission
REQ = 0x05  # data request

# Set up local I/O.
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
]

axes = [
    # We are only interested in raw values here - deadband/min/max processing will
    # be handled in the code running on the stick component.
    Axis(board.A8),
    Axis(board.A9),
    Axis(board.A10),
    Axis(board.A11),
]

hats = [
    Hat(up=board.D14, down=board.D15, left=board.D16, right=board.D17),
    Hat(up=board.D18, down=board.D19, left=board.D20, right=board.D21),
]

# Throttle input processing loop.
while True:

    # There's nothing to do unless we've received at least 3 bytes.
    #   Byte 0 = STX
    #   Byte 1 = Command Byte (Current only REQ is implemented)
    #   Byte 2 = ETX
    if uart.in_waiting >= 3:
        rx = uart.read(3)  # Read 3 bytes (stx, command, etx).

        # Make sure no framing error has occurred (missing STX or ETX).
        if rx[0] != STX or rx[2] != ETX:
            uart.reset_input_buffer()
            continue

        # Process state request command.
        if rx[1] == REQ:

            # Collect raw button states.
            button_states = 0
            for i, b in enumerate(buttons):
                if b.source_value:
                    button_states |= 0x01 << i

            # Collect raw hat switch states.
            hat_states = 0
            for i, h in enumerate(hats):
                hat_states |= h.packed_source_values << (4 * i)

            # Pack up all the data in a byte array.
            tx = bytearray(15)
            struct.pack_into(
                "<BBHHHHHBBB",
                tx,
                0,
                STX,
                REQ,
                button_states,
                axes[0].source_value,
                axes[1].source_value,
                axes[2].source_value,
                axes[3].source_value,
                hat_states,
                0x00,  # checkbyte placeholder
                ETX,
            )

            # Calculate the byte used by the stick component to ensure data integrity.
            checkbyte = 0x00
            for b in tx[1:13]:
                checkbyte ^= b
            tx[13] = checkbyte

            # Send the data to the stick component
            uart.write(tx)
