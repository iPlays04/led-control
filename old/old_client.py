import board
import neopixel
import random
import colorsys
from time import sleep


pixels = neopixel.NeoPixel(board.D18, 150)


#pixels.brightness(0.3)

ambirange1 = (11,20)
ambirange2 = (41,50)

traillen = 16

maxbrightness = 0.3

sparkles = []
ambibuffer = []

def read_color():
    try:
        with open("./color.txt", "r") as f:
            r, g, b, speed, m, o1, o2, o3, isAmbi, brightness = map(int, f.read().strip().split(","))
            return r,g,b, speed, m, o1, o2, o3, isAmbi, brightness
    except:
        return 2, 2, 10  # default color

def read_ambiColor(pcname):
    global ambibuffer
    try:
        with open(f"./color_{pcname}.txt", "r") as f:
            rgbvalues = f.read().strip().splitlines()
            result = []
            for value in rgbvalues:
                splitvalues = value.split(",")
                result.append(tuple(int(singlevalue) for singlevalue in splitvalues))
            print(result)
            if result != []:
                ambibuffer = result
                return result
            else: 
                return ambibuffer
    except:
        return "AAA"

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
        red, green, blue, speed, mode, o1, o2, o3, isAmbi, brightness= read_color()
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
                            sparkles.remove(sparkle)
                            continue
                        pixels[sparkle[0]] = colourpixel(
                            max(0, int(red - o2 + sparkle[1])),
                            max(0, int(green - o2 + sparkle[1])),
                            max(0, int(blue - o2 + sparkle[1]))
                        )
                        sparkle[1] = sparkle[1]-1

                case 3: #rng
                    for i in range(len(pixels)):
                        pixels[i] = colourpixel(random.random()*255,random.random()*255,random.random()*255)
                    
                case 4:  # RGB Rainbow Wave
                    for i in range(len(pixels)):
                        hue = (pixelclock + i) / len(pixels)
                        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                        pixels[i] = colourpixel(r * 255, g * 255, b * 255)

                case 5: #dynamic 2 colour gradient
                    half_length = len(pixels) // 2
                    pixelclock_mod = pixelclock % len(pixels)

                    for i in range(len(pixels)):
                        gradient_factor = ((pixelclock_mod - i) % half_length) / half_length

                        if (i > pixelclock_mod and i <= pixelclock_mod + half_length) or (i > pixelclock_mod - len(pixels) and i <= pixelclock_mod - len(pixels) + half_length):
                            pixels[i] = colourpixel(
                                max(0, red + gradient_factor * (o1 - red)),
                                max(0, green + gradient_factor * (o2 - green)),
                                max(0, blue + gradient_factor * (o3 - blue))
                            )
                        else:
                            pixels[i] = colourpixel(
                                max(0, o1 + gradient_factor * (red - o1)),
                                max(0, o2 + gradient_factor * (green - o2)),
                                max(0, o3 + gradient_factor * (blue - o3))
                            )

                case 6: #static 2 colour gradient
                    for i in range(len(pixels)):
                        pixels[i] = colourpixel(max(0, red + ((i)%(len(pixels))/(len(pixels))) * (o1-red)), max(0,  green + ((i)%(len(pixels))/(len(pixels))) * (o2-green)), max(0,  blue + ((i)%(len(pixels))/(len(pixels))) * (o3-blue)))

        if isAmbi:
            i = ambirange1[0]
            pc1 = read_ambiColor("testpc")
            
            while(i<ambirange1[1]):
                pixels[i]=pc1[i-ambirange1[0]]
                i+=1
            i = ambirange2[0]
            pc2 = read_ambiColor("testpc")
            while(i<ambirange2[1]):
                pixels[i]=pc2[i-ambirange2[0]]
                i+=1

        for i in range(len(pixels)):
            pixels[i] = (int(pixels[i][0]*(brightness/100)),int(pixels[i][1]*(brightness/100)),int(pixels[i][2]*(brightness/100)))

        sleep((251-speed)/100)
        

    else:
        for i in range(len(pixels)):
            pixels[i] = colourpixel(0,0,0)
        sleep(1)

    pixelclock = (pixelclock+1)%len(pixels)


