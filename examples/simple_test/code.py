"""
JoystickXL simple test.

No physical I/O required, just use a joystick/gamepad testing application (like the one
built-in to Windows) and watch the inputs cycle.

Tested on an Adafruit QT-Py, but should work on other CircuitPython boards.

Don't forget to copy boot.py from the example folder to your CIRCUITPY drive.
"""
import time

from joystick_xl.joystick import Joystick

js = Joystick()

while True:

    # Exercise every defined button.
    for i in range(js.num_buttons):
        js.update_button((i, True))
        time.sleep(0.05)
        js.update_button((i, False))
        time.sleep(0.05)

    # Exercise every defined axis.
    for a in range(js.num_axes):
        for i in range(0, -128, -1):
            js.update_axis((a, i))
        for i in range(-127, 128):
            js.update_axis((a, i))
        for i in range(127, -1, -1):
            js.update_axis((a, i))

    # Exercise every defined hat switch.
    for h in range(js.num_hats):
        for i in range(0, 9):
            js.update_hat((h, i))
            time.sleep(0.25)
