import time

from joystick_xl.joystick import Joystick

if __name__ == "__main__":
    js = Joystick()

    while True:

        for i in range(1, js.num_buttons + 1):
            js.press_buttons(i)
            time.sleep(0.05)
            js.release_buttons(i)
            time.sleep(0.05)

        for a in range(js.num_axes):
            for i in range(0, -128, -1):
                js.move_axes((a, i))
            for i in range(-127, 128):
                js.move_axes((a, i))
            for i in range(127, -1, -1):
                js.move_axes((a, i))

        for h in range(js.num_hats):
            for i in range(0, 9):
                js.move_hats((h, i))
                time.sleep(0.25)
