"""
JoystickXL Example #3 - Button Operations (2 axes, 2 buttons).

This example demonstrates the use of button `bypass`, `is_pressed`, `is_released`,
`was_pressed` and `was_released` attributes.

Tested on an Adafruit ItsyBitsy M4 Express, but should work on other CircuitPython
boards with a sufficient quantity/type of pins.

* Buttons are on pins D9 and D10
* Axes are on pins A2 and A3
* A "safety switch" is connected to pin D11
* An LED and current-limiting resistor are connected to pin D12
* The on-board LED connected to pin D13 is used as well

Don't forget to copy boot.py from the example folder to your CIRCUITPY drive.
"""

import board  # type: ignore (this is a CircuitPython built-in)
import digitalio  # type: ignore (this is a CircuitPython built-in)
from joystick_xl.inputs import Axis, Button
from joystick_xl.joystick import Joystick

joystick = Joystick()

joystick.add_input(
    Button(board.D9),  # primary fire
    Button(board.D10),  # secondary fire
    Axis(board.A2),  # x-axis
    Axis(board.A3),  # y-axis
)

# The safety switch will be used to lock out the first two buttons, which - on a typical
# flight stick - are the fire buttons for primary and secondary weapons systems.
safety_switch = digitalio.DigitalInOut(board.D11)
safety_switch.direction = digitalio.Direction.INPUT
safety_switch.pull = digitalio.Pull.UP

# This will be used to demonstrate the `is_pressed` attribute - it will stay lit while
# button 1 is pressed.
b1_led = digitalio.DigitalInOut(board.D12)
b1_led.direction = digitalio.Direction.OUTPUT

# This will be used to demonstrate the `is_released` attribute - it will stay lit while
# button 2 is released.
b2_led = digitalio.DigitalInOut(board.D13)
b2_led.direction = digitalio.Direction.OUTPUT


while True:

    # Set the bypass value of the first two buttons based on the safety switch value.
    for b in range(2):
        joystick.button[b].bypass = safety_switch.value

    # Axes and hat switches can also be bypassed:
    #   joystick.axis[0].bypass = True
    #   joystick.hat[2] = True

    # Hat switch buttons can also be individually bypassed like so:
    #   joystick.hat[1].up.bypass = True
    #   joystick.hat[1].right.bypass = True

    # Update the leds using `is_pressed` and `is_released`.  Don't forget the list of
    # buttons is zero-based, so button 1 is joystick.button[0]!
    b1_led.value = joystick.button[0].is_pressed
    b2_led.value = joystick.button[1].is_released

    # Notice that the `*_pressed` and `*_released` events are not affected by the
    # `bypass` attribute - `bypass` only affects the state of the button that is sent
    # to the host device via USB.  If you need to stop local button-related functions
    # (such as the LED controls above), you can wrap it in an if statement like the
    # following (You'll need to be connected via serial console to see the output of
    # the print statement):

    if joystick.button[1].bypass is False:
        if joystick.button[1].is_pressed:
            print("Button 2 is pressed and is not bypassed.")

    # If you want events to occur only on the rising/falling edge of button presses,
    # you can use the `was_pressed` and `was_released` attributes. (You'll need to be
    # connected via serial console to see the output of these print statements.)
    if joystick.button[0].was_pressed:
        print("Button 1 was just pressed.")

    if joystick.button[0].was_released:
        print("Button 1 was just released.")

    # Update all of the joystick inputs.
    joystick.update()
