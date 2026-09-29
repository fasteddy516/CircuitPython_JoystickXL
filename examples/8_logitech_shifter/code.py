"""
Logitech Driving Force Shifter to USB joystick.

The Driving Force Shifter is an analog joystick with a DE-9 connector. Six
positions represent the gears 1-6. Reverse is indicated by pressing the reverse
button while moving the selector to position 6.

Calibrate by moving the shifter to each position and pressing <Enter> on the
serial connection; then copy values into positions = () array and save.

This code works by finding the closest of 6 calibrated positions to the current
position as long as it's less than NEUTRAL_DISTANCE, so it doesn't matter which
axis is connected to X or Y.

Wiring::

DE-9 - Board

1 - NC

2 - reverse

3 - reverse_power (or VCC)

4 - axis_1

5 - NC

6 - GND

7 - NC (connected internally to 9)

8 - axis_0

9 - VCC

Special thanks to https://github.com/dmadison/Sim-Racing-Arduino/ 's documentation.
"""

import json
import time

import analogio
import board
import digitalio
from joystick_xl.inputs import Button
from joystick_xl.joystick import Joystick

positions = [
    [54349, 20949],
    [4289, 21013],
    [55789, 32952],
    [4369, 32776],
    [55309, 46267],
    [4865, 46059],
]

# So there's no position where we oscillate between gears
ENTER_GEAR_DISTANCE = 8192
EXIT_GEAR_DISTANCE = ENTER_GEAR_DISTANCE + 512

js = Joystick()

# 1-6 + reverse
buttons = [Button() for _ in range(7)]
js.add_input(*buttons)

axis_0 = analogio.AnalogIn(board.A0)
axis_1 = analogio.AnalogIn(board.A1)

# used to power the reverse switch instead of connecting +3v3
reverse_power = digitalio.DigitalInOut(board.D2)
reverse_power.switch_to_output()
reverse_power.value = True

reverse = digitalio.DigitalInOut(board.D3)
reverse.switch_to_input()


def calibrate():
    input("Press <Enter> to begin calibration.")
    for i in range(6):
        input(f"Shift to {i} then press <Enter>")
        positions.append((axis_0.value, axis_1.value))

    print(json.dumps(positions))


def find_gear(gear):
    position = (axis_0.value, axis_1.value)
    min_distance = 131072

    for i, pos in enumerate(positions):
        distance = abs(position[0] - pos[0]) + abs(position[1] - pos[1])
        if distance < min_distance:
            min_distance = distance
            gear = i

    if min_distance < ENTER_GEAR_DISTANCE:
        if gear == 5 and reverse.value:
            gear = 6
        return gear

    if min_distance >= EXIT_GEAR_DISTANCE:
        return -1

    return gear


if not positions:
    calibrate()


gear = -2  # invalid gear

while True:
    new_gear = find_gear(gear)
    if gear != new_gear:
        gear = new_gear
        print(f"Gear {gear}")
        print(f"Reverse {reverse.value}")
        print("Position", (axis_0.value, axis_1.value))

        for i, button in enumerate(buttons):
            # False is "pressed"
            button.source_value = gear != i

        js.update()

    time.sleep(0.001)
