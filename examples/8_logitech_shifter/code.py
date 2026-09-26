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
"""

import json
import sys
import time

import analogio
import board
import digitalio
from joystick_xl.inputs import Button
from joystick_xl.joystick import Joystick

positions = (
    (56077, 18644),
    (4145, 18196),
    (57678, 33080),
    (3152, 32391),
    (56909, 48667),
    (3584, 48731),
)


NEUTRAL_DISTANCE = 8192

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
    for i in range(6):
        input(f"Shift to {i}")
        positions.append((axis_0.value, axis_1.value))

    sys.stdout.write(json.dumps(positions))


def find_gear():
    position = (axis_0.value, axis_1.value)
    min_distance = 131072
    gear = -1
    for i, pos in enumerate(positions):
        distance = abs(position[0] - pos[0]) + abs(position[1] - pos[1])
        if distance < min_distance:
            min_distance = distance
            gear = i

    if min_distance < NEUTRAL_DISTANCE:
        return gear
    return -1


if not positions:
    calibrate()


gear = -2  # invalid gear

while True:
    new_gear = find_gear()
    if gear != new_gear:
        gear = new_gear
        print(f"Gear {gear}")
        print(f"Reverse {reverse.value}")

        if gear == 5 and reverse.value:
            gear = 6

        for i, button in enumerate(buttons):
            # False is "pressed"
            button.source_value = gear != i

        js.update()

    time.sleep(0.001)
