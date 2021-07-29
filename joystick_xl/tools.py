"""Tools to assist in the development and general use of JoystickXL."""

import time

from joystick_xl import __version__
from joystick_xl.inputs import Axis, Hat
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


def TestConsole():
    """Run JoystickXL's REPL-based, built-in test console."""
    INVALID_OPERATION = "> Invalid operation."

    js = Joystick()
    last_cmd = ""
    si = 1  # start index

    def ValidateIndex(i: int, limit: int, name: str) -> int:
        if not limit:
            print("> No", name, "inputs configured! (check boot.py)")
            return -1
        if i < si or i > limit - (1 - si):
            print("> Invalid", name, "specified.")
            return -1
        else:
            return i - si

    print("\nJoystickXL", __version__, "- Test Console\n")
    print("Using 1-based indexing.")
    print("Enter command (? for list)")

    while True:

        cmd = input(": ").lower()  # prompt and user input

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
            elif cmd.endswith("+"):
                operation = "MAX"
                value = Axis.MAX
            elif cmd.endswith("-"):
                operation = "MIN"
                value = Axis.MIN
            else:
                print(INVALID_OPERATION)
                continue
            print("> Axis", i + si, operation)
            js.update_axis((i, value))
            time.sleep(1)
            js.update_axis((i, Axis.IDLE))

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
            time.sleep(1)
            js.update_button((i, False))

        # hat functions
        elif cmd.startswith("h"):
            if cmd.endswith("t"):
                TestHats(js)
                continue
            i = ValidateIndex(num, js.num_hats, "hat switch")
            if i < 0:
                continue
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
            time.sleep(1)
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

        # help
        elif cmd.startswith("?"):
            print("  a = axis (ex. `a2+`, `a1-`, `at`)")
            print("  b = button (ex. `b13`, `bt`)")
            print("  h = hat (ex. `h1u`, `h1d`, `h1l`, `h1r`, `ht`)")
            print("  t = test all")
            print("  0 = 0-based indexing (button 1 = 0)")
            print("  1 = 1-based indexing (button 1 = 1)")
            print("  q = quit")

        # quit
        elif cmd.startswith("q"):
            break

        # unrecognized command
        else:
            print("> Unrecognized command. (? for list)")
