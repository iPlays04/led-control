import board
import neopixel
import random
import colorsys
import time
from time import sleep

pixels = neopixel.NeoPixel(board.D18, 150)

ambirange1 = (11, 20)
ambirange2 = (41, 50)

maxbrightness = 0.3

sparkles = []
ambibuffer = []

last_check_time = 0
last_color_time = 0
last_ambi_time = 0
config = {}

def read_config():
    global config
    try:
        with open("./color.txt", "r") as f:
            r, g, b, speed, m, o1, o2, o3, isAmbi, brightness = map(int, f.read().strip().split(","))
            config = {
                'r': r, 'g': g, 'b': b, 'speed': speed, 'mode': m,
                'o1': o1, 'o2': o2, 'o3': o3, 'isAmbi': isAmbi, 'brightness': brightness
            }
            return config
    except:
        return {'r': 2, 'g': 2, 'b': 10, 'speed': 2, 'mode': 0, 'o1': 0, 'o2': 0, 'o3': 0, 'isAmbi': 0, 'brightness': 100}

def read_ambiColor(pcname):
    global ambibuffer
    try:
        with open(f"./color_{pcname}.txt", "r") as f:
            rgbvalues = f.read().strip().splitlines()
            result = []
            for value in rgbvalues:
                splitvalues = value.split(",")
                result.append(tuple(int(singlevalue) for singlevalue in splitvalues))
            if result:
                ambibuffer = result
                return result
            else:
                return ambibuffer
    except:
        return ambibuffer

def colourpixel(r, g, b, brightness=maxbrightness):
    nr = int(r * brightness)
    ng = int(g * brightness)
    nb = int(b * brightness)
    return (nr, ng, nb)

pixelclock = 0

def check_file_change(filename):
    global last_check_time, last_color_time, last_ambi_time
    try:
        if filename == "./check.txt":
            current_time = time.time()
            if current_time - last_check_time > 1:
                last_check_time = current_time
                return True
        elif filename == "./color.txt":
            current_time = time.time()
            if current_time - last_color_time > 1:
                last_color_time = current_time
                return True
        else:
            current_time = time.time()
            if current_time - last_ambi_time > 1:
                last_ambi_time = current_time
                return True
        return False
    except:
        return True

running = False
while True:
    try:
        if check_file_change("./check.txt"):
            with open("./check.txt", "r") as f:
                running = f.read().strip() == "1"
    except:
        running = False

    if running:
        if check_file_change("./color.txt"):
            config = read_config()
        red, green, blue, speed, mode, o1, o2, o3, isAmbi, brightness = config.values()
        
        brightness_factor = brightness / 100.0

        if mode == 0:
            color = colourpixel(red, green, blue, brightness_factor)
            for i in range(len(pixels)):
                pixels[i] = color
        elif mode == 1:  # Light Pulse
            o2_adj = o2 * brightness_factor
            for i in range(len(pixels)):
                pixels[i] = colourpixel(max(0, red - o2_adj), max(0, green - o2_adj), max(0, blue - o2_adj), brightness_factor)
            for spec in range(o1):
                index = ((spec - (int(o1 / 2))) + pixelclock) % len(pixels)
                factor = abs(1 - abs(spec - (int(o1 / 2))) / int(o1 / 2))
                pixels[index] = colourpixel(
                    max(int(factor * o2_adj + (red - o2_adj)), 0),
                    max(int(factor * o2_adj + (green - o2_adj)), 0),
                    max(int(factor * o2_adj + (blue - o2_adj)), 0),
                    brightness_factor
                )
        elif mode == 2:  # Sparkle
            o2_adj = o2 * brightness_factor
            if random.random() * 100 < o1:
                sparkles.insert(0, [int(random.random() * len(pixels)), o2_adj])
            for i in range(len(pixels)):
                pixels[i] = colourpixel(max(0, red - o2_adj), max(0, green - o2_adj), max(0, blue - o2_adj), brightness_factor)
            
            sparkles_copy = sparkles[:]
            for sparkle in sparkles_copy:
                if sparkle[1] <= 0:
                    sparkles.remove(sparkle)
                    continue
                pixel_index = sparkle[0]
                sparkle_brightness = sparkle[1]
                pixels[pixel_index] = colourpixel(
                    max(0, int(red - o2_adj + sparkle_brightness)),
                    max(0, int(green - o2_adj + sparkle_brightness)),
                    max(0, int(blue - o2_adj + sparkle_brightness)),
                    brightness_factor
                )
                sparkle[1] -= 1
        elif mode == 3:  # rng
            for i in range(len(pixels)):
                pixels[i] = colourpixel(random.random() * 255, random.random() * 255, random.random() * 255, brightness_factor)
        elif mode == 4:  # RGB Rainbow Wave
            for i in range(len(pixels)):
                hue = (pixelclock + i) / len(pixels)
                r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                pixels[i] = colourpixel(r * 255, g * 255, b * 255, brightness_factor)
        elif mode == 5:  # dynamic 2 colour gradient
            half_length = len(pixels) // 2
            pixelclock_mod = pixelclock % len(pixels)

            for i in range(len(pixels)):
                gradient_factor = ((pixelclock_mod - i) % half_length) / half_length

                if (i > pixelclock_mod and i <= pixelclock_mod + half_length) or (i > pixelclock_mod - len(pixels) and i <= pixelclock_mod - len(pixels) + half_length):
                    pixels[i] = colourpixel(
                        max(0, red + gradient_factor * (o1 - red)),
                        max(0, green + gradient_factor * (o2 - green)),
                        max(0, blue + gradient_factor * (o3 - blue)),
                        brightness_factor
                    )
                else:
                    pixels[i] = colourpixel(
                        max(0, o1 + gradient_factor * (red - o1)),
                        max(0, o2 + gradient_factor * (green - o2)),
                        max(0, o3 + gradient_factor * (blue - o3)),
                        brightness_factor
                    )
        elif mode == 6:  # static 2 colour gradient
            for i in range(len(pixels)):
                pixels[i] = colourpixel(
                    max(0, red + ((i) % (len(pixels)) / (len(pixels))) * (o1 - red)),
                    max(0, green + ((i) % (len(pixels)) / (len(pixels))) * (o2 - green)),
                    max(0, blue + ((i) % (len(pixels)) / (len(pixels))) * (o3 - blue)),
                    brightness_factor
                )

        if isAmbi:
            if check_file_change("./color_testpc.txt"):
                pc1 = read_ambiColor("testpc")
            if pc1:
                pixels[ambirange1[0]:ambirange1[1]] = pc1[0:ambirange1[1]-ambirange1[0]]
                pixels[ambirange2[0]:ambirange2[1]] = pc1[0:ambirange2[1]-ambirange2[0]]

        sleep((251 - speed) / 100)

    else:
        for i in range(len(pixels)):
            pixels[i] = (0, 0, 0)
        sleep(1)

    pixelclock = (pixelclock + 1) % len(pixels)
