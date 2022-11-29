from pynput.keyboard import Listener
from pynput.mouse import Controller, Button
import time
import mss
import mss.tools
from PIL import Image

mouse = Controller()
break_program = False
region = {"top": 405, "left": 660, "width": 600, "height": 420}


def on_press(key):
    global break_program
    try:
        if key.char == 'q':
            print("Exiting program.")
            break_program = True
            return False
    except AttributeError:
        pass


def start_game():
    start_button = (726, 763)
    mouse.position = start_button
    time.sleep(1)
    for _ in range(2):
        mouse.press(Button.left)
        time.sleep(0.1)
        mouse.release(Button.left)
        time.sleep(0.1)


def take_screenshot():
    sct = mss.mss()
    scr = sct.grab(monitor=region)
    scr = mss.tools.to_png(scr.rgb, scr.size, output="screenshot.png")
    img = Image.open("screenshot.png")
    return img


def get_targets(img):
    result = []
    width, height = img.size
    for x in range(0, width, 5):
        for y in range(0, height, 5):
            r, g, b = img.getpixel((x, y))
            if b == 197:
                result.append((int(x / 2) + 660, int(y / 2) + 405))
    return result


def click_target(target):
    mouse.position = target
    time.sleep(0.005)
    mouse.press(Button.left)
    mouse.release(Button.left)


def same_target(last_target, new_target):
    same_x = False
    same_y = False
    if new_target[0] in range(last_target[0] - 20, last_target[0] + 20):
        same_x = True
    if new_target[1] in range(last_target[1] - 20, last_target[1] + 20):
        same_y = True
    if same_x and same_y:
        return True
    else:
        return False


def clicked_recently(recents, new_target):
    for target in reversed(recents):
        if same_target(target, new_target):
            return True
    return False


def main():
    last_clicked = (0, 0)
    recently_clicked = []

    with Listener(on_press=on_press) as listener:
        start_game()
        time.sleep(0.01)

        while not break_program:
            while len(recently_clicked) > 4:
                recently_clicked.pop(0)

            img = take_screenshot()
            targets = get_targets(img)

            for target in targets:
                if not same_target(last_clicked, target):
                    if not clicked_recently(recently_clicked, target):
                        click_target(target)
                        last_clicked = target
                        recently_clicked.append(target)

        listener.join()


if __name__ == "__main__":
    main()
