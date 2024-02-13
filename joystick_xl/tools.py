"""Tools to assist in the development and general use of JoystickXL."""

import time

# These are all CircuitPython built-ins
import board  # type: ignore
import digitalio  # type: ignore
from microcontroller import Pin  # type: ignore
from supervisor import runtime  # type: ignore

from joystick_xl import __version__
from joystick_xl.inputs import Axis, Hat, VirtualInput
from joystick_xl.joystick import Joystick


def TestAxes(js: Joystick, step: int = 5, quiet: bool = False) -> None:
    """
    Exercise each axis in the supplied ``Joystick`` object.

    :param js: The ``Joystick`` object to test.
    :type js: Joystick
    :param step: The size of axis adjustment steps.  A higher value provides coarser
        axis movement and faster tests.  Set to ``1`` to test every possible axis value
        (which can result in long test runs).  (Default is 5)
    :type step: int, optional
    :param quiet: Set to ``True`` to disable console output during testing.  (Defaults
        to ``False``)
    :type quiet: bool, optional
    """
    if not js.num_axes:
        if not quiet:
            print("> No axis inputs configured! (check boot.py)")
        return
    if not quiet:
        print("> Testing axes...", end="")
    for a in range(js.num_axes):
        for i in range(Axis.IDLE, Axis.MIN, -step):
            js.update_axis((a, i))
        for i in range(Axis.MIN, Axis.MAX, step):
            js.update_axis((a, i))
        for i in range(Axis.MAX, Axis.IDLE - 1, -step):
            js.update_axis((a, i))
        js.update_axis((a, Axis.IDLE))
    if not quiet:
        print("DONE")


def TestButtons(js: Joystick, pace: float = 0.05, quiet: bool = False) -> None:
    """
    Exercise each button in the supplied ``Joystick`` object.

    :param js: The ``Joystick`` object to test.
    :type js: Joystick
    :param pace: Duration (in seconds) and time between button presses.  (Default is
        0.05 seconds)
    :type pace: float, optional
    :param quiet: Set to ``True`` to disable console output during testing.  (Defaults
        to ``False``.)
    :type quiet: bool, optional
    """
    if not js.num_buttons:
        if not quiet:
            print("> No button inputs configured! (check boot.py)")
        return
    if not quiet:
        print("> Testing buttons...", end="")
    for i in range(js.num_buttons):
        js.update_button((i, True))
        time.sleep(pace)
        js.update_button((i, False))
        time.sleep(pace)
    if not quiet:
        print("DONE")


def TestHats(js: Joystick, pace: float = 0.25, quiet: bool = False) -> None:
    """
    Exercise each hat switch in the supplied ``Joystick`` object.

    :param js: The ``Joystick`` object to test.
    :type js: Joystick
    :param pace: Duration (in seconds) that each hat switch direction will be engaged
        for.  (Default is 0.25 seconds)
    :type pace: float, optional
    :param quiet: Set to ``True`` to disable console output during testing.  (Defaults
        to ``False``.)
    :type quiet: bool, optional
    """
    if not js.num_hats:
        if not quiet:
            print("> No hat switch inputs configured! (check boot.py)")
        return
    if not quiet:
        print("> Testing hat switches...", end="")
    for h in range(js.num_hats):
        for i in range(Hat.U, Hat.IDLE + 1):
            js.update_hat((h, i))
            time.sleep(pace)
    if not quiet:
        print("DONE")


def TestConsole(button_pin: Pin = None):
    """
    Run JoystickXL's REPL-based, built-in test console.

    :param button_pin: Specify the pin to use as TestConsole's test button.  Defaults
        to ``board.D2`` (``board.GP2`` on RP2040-based devices).
    :type button_pin: microcontroller.Pin, optional
    """
    INVALID_OPERATION = "> Invalid operation."

    js = Joystick()
    last_cmd = ""
    si = 1  # start index
    pt = 0.25  # press time

    def ValidateIndex(i: int, limit: int, name: str) -> int:
        if not limit:
            print("> No", name, "inputs configured! (check boot.py)")
            return -1
        if i < si or i > limit - (1 - si):
            print("> Invalid", name, "specified.")
            return -1
        else:
            return i - si

    def MoveAxis(axis: int, stop: int, step: int) -> None:
        for i in range(Axis.IDLE, stop, step):
            js.update_axis((axis, i))
        for i in range(stop, Axis.IDLE, -step):
            js.update_axis((axis, i))
        js.update_axis((axis, Axis.IDLE))

    print("\nJoystickXL", __version__, "- Test Console\n")
    print("Using 1-based indexing.")
    print("Button Clicks = 0.25s")
    print("Test Button = ", end="")
    try:
        # Attempt to configure a test button
        if button_pin is None:
            try:
                # for most CircuitPython boards
                pin = board.D2
            except AttributeError:
                # for RP2040-based boards
                pin = board.GP2
        else:
            pin = button_pin
        button = digitalio.DigitalInOut(pin)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP
        print(pin)
    except AttributeError:
        # Fall back to a VirtualInput if button assignment fails
        button = VirtualInput(value=True)
        print("(Not Assigned)")

    print("Enter command (? for list)")

    while True:

        print(": ", end="")
        cmd = ""

        while not runtime.serial_bytes_available:
            if button.value is False:
                break

        if runtime.serial_bytes_available:
            cmd = input().lower()  # prompt and user input

        if not cmd and last_cmd:  # repeat last command if nothing was entered
            cmd = last_cmd
            print("(", cmd, ")")
        else:
            last_cmd = cmd

        # extract a number from the entered command (0 if no number was entered)
        num = int("0" + "".join(filter(lambda i: i.isdigit(), cmd)))

        # axis functions
        if cmd.startswith("a"):
            if cmd.endswith("t"):
                TestAxes(js)
                continue
            i = ValidateIndex(num, js.num_axes, "axis")
            if i < 0:
                continue
            elif cmd.endswith("u"):
                operation = "UP"
                value = Axis.MAX
                step = 3
            elif cmd.endswith("d"):
                operation = "DOWN"
                value = Axis.MIN
                step = -3
            else:
                print(INVALID_OPERATION)
                continue
            print("> Axis", i + si, operation)
            MoveAxis(i, value, step)

        # button functions
        elif cmd.startswith("b"):
            if cmd.endswith("t"):
                TestButtons(js)
                continue
            i = ValidateIndex(num, js.num_buttons, "button")
            if i < 0:
                continue
            print("> Button", i + si, "CLICK")
            js.update_button((i, True))
            time.sleep(pt)
            js.update_button((i, False))

        # hat functions
        elif cmd.startswith("h"):
            if cmd.endswith("t"):
                TestHats(js)
                continue
            i = ValidateIndex(num, js.num_hats, "hat switch")
            if i < 0:
                continue
            elif "u" in cmd and "l" in cmd:
                operation = "UP+LEFT"
                value = Hat.UL
            elif "u" in cmd and "r" in cmd:
                operation = "UP+RIGHT"
                value = Hat.UR
            elif "d" in cmd and "l" in cmd:
                operation = "DOWN+LEFT"
                value = Hat.DL
            elif "d" in cmd and "r" in cmd:
                operation = "DOWN+RIGHT"
                value = Hat.DR
            elif cmd.endswith("u"):
                operation = "UP"
                value = Hat.U
            elif cmd.endswith("d"):
                operation = "DOWN"
                value = Hat.D
            elif cmd.endswith("l"):
                operation = "LEFT"
                value = Hat.L
            elif cmd.endswith("r"):
                operation = "RIGHT"
                value = Hat.R
            else:
                print(INVALID_OPERATION)
                continue
            print("> Hat Switch", i + si, operation)
            js.update_hat((i, value))
            time.sleep(pt)
            js.update_hat((i, Hat.IDLE))

        # auto-test functions
        elif cmd.startswith("t"):
            if js.num_axes:
                TestAxes(js)
            if js.num_buttons:
                TestButtons(js)
            if js.num_hats:
                TestHats(js)
            print("> All tests completed.")
            pass

        # use 0-based indices
        elif cmd.startswith("0"):
            si = 0
            print("> Using 0-based indexing.")

        # use 1-based indices
        elif cmd.startswith("1"):
            si = 1
            print("> Using 1-based indexing.")

        # set button press time
        elif cmd.startswith("p"):
            pt = num / 100
            print("> Button presses set to", pt, "seconds.")

        # help
        elif cmd.startswith("?"):
            print("  a = axis (ex. `a2u`, `a1d`, `at`)")
            print("  b = button (ex. `b13`, `bt`)")
            print("  h = hat (ex. `h1u`, `h1d`, `h1ul`, `h1dr`, `ht`)")
            print("  t = test all")
            print("  0 = 0-based indexing (button 1 = 0)")
            print("  1 = 1-based indexing (button 1 = 1)")
            print("  p = click time (ex. `p150` = 1.5 seconds")
            print("  q = quit")

        # quit
        elif cmd.startswith("q"):
            break

        # unrecognized command
        else:
            print("> Unrecognized command. (? for list)")
