import board
import neopixel
import random
import colorsys
from time import sleep


pixels = neopixel.NeoPixel(board.D18, 24)


#pixels.brightness(0.3)

traillen = 16

maxbrightness = 0.3

sparkles = []

def read_color():
    try:
        with open("./color.txt", "r") as f:
            r, g, b, m, o1, o2 = map(int, f.read().strip().split(","))
            return int(r,g,b), m, o1, o2
    except:
        return 2, 2, 10  # default color

def colourpixel(r,g,b):
    nr=int(r*maxbrightness)
    ng=int(g*maxbrightness)
    nb=int(b*maxbrightness)
    return((nr,ng,nb))

pixelclock = 0

while True: #all code gets executed once every update, all lights need to be assigned a value here 
    
    try:
        with open("./check.txt", "r") as f:
            running = f.read().strip() == "1"
    except:
        running = False

    if running:
        red, green, blue, mode, o1, o2= read_color()
        match mode:
            case 0:
                for i in range(len(pixels)):
                    pixels[i] = colourpixel(max(0, red), max(0, green), max(0, blue))

            case 1: #Light Pulse | o1 = overall length of pulse | o2 = max additional brightness in center of pulse !!to prevent overbrightness, same value is decresed from rest!!
                for i in range(len(pixels)):
                    pixels[i] = colourpixel(max(0, red - o2), max(0, green - o2), max(0, blue - o2))
                for spec in range(o1):
                    index = ((spec - (int(o1 / 2))) + pixelclock) % len(pixels)
                    factor = abs(1 - abs(spec - (int(o1 / 2))) / int(o1 / 2))
                    pixels[index] = colourpixel(
                        max(int(factor * o2 + (red - o2)), 0),
                        max(int(factor * o2 + (green - o2)), 0),
                        max(int(factor * o2 + (blue - o2)), 0)
                    )

            case 2: #Sparkle
                if random.random() * 100 < o1:
                    sparkles.insert(0, [int(random.random() * len(pixels)), o2])
                for i in range(len(pixels)):
                    pixels[i] = colourpixel(max(0, red - o2), max(0, green - o2), max(0, blue - o2))
                for sparkle in sparkles:
                    if sparkle[1] <= 0:
                        print(sparkle)
                        sparkles.remove(sparkle)
                        continue
                    pixels[sparkle[0]] = colourpixel(
                        max(0, int(red - o2 + sparkle[1])),
                        max(0, int(green - o2 + sparkle[1])),
                        max(0, int(blue - o2 + sparkle[1]))
                    )
                    sparkle[1] = sparkle[1]-3
                    #print(sparkle)

            case 3: #rng
                for i in range(len(pixels)):
                    pixels[i] = colourpixel(random.random()*255,random.random()*255,random.random()*255)
                
            case 4:  # RGB Rainbow Wave
                for i in range(len(pixels)):
                    hue = (pixelclock + i) / len(pixels)
                    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                    pixels[i] = colourpixel(r * 255, g * 255, b * 255)



                

    else:
        sleep(0.1)

    pixelclock = (pixelclock+1)%len(pixels)


