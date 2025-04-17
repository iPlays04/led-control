import board
import neopixel
from time import sleep

pixels = neopixel.NeoPixel(board.D18, 24)

traillen = 16

def read_color():
    try:
        with open("./color.txt", "r") as f:
            r, g, b = map(int, f.read().strip().split(","))
            return r, g, b
    except:
        return 2, 2, 10  # default color

while True:
    try:
        with open("./check.txt", "r") as f:
            running = f.read().strip() == "1"
    except:
        running = False

    if running:
        red, green, blue = read_color()
        for active in range(len(pixels)):
            for pixel in range(len(pixels)):
                try:
                    with open("./check.txt", "r") as f:
                        if f.read().strip() != "1":
                            break
                except:
                    break
                localred = max(int(red * ((traillen-pixel)/traillen)), 0)
                localgreen = max(int(green * ((traillen-pixel)/traillen)), 0)
                localblue = max(int(blue * ((traillen-pixel)/traillen)), 0)
                pixels[(pixel - active) % 24] = (localred, localgreen, localblue)
            sleep(0.1)
    else:
        sleep(0.1)
