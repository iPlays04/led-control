import tkinter as tk
import random
from time import sleep
import colorsys
import math

'''

Testenv

'''

pixels = [(0, 0, 0)]*80

root = tk.Tk(screenName="ledtest")
root.title("Basic Tkinter UI")
root.geometry("1600x200")
root.configure(bg="BLACK")
canvas = tk.Canvas(root, width=1600, height=200,bg="BLACK")
canvas.pack()

pixelclock = 0

traillen = 10

sparkles = []

maxbrightness = 1

ambibuffer = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]

def read_color():
    try:
        with open("./color.txt", "r") as f:
            r, g, b, speed, m, o1, o2, o3, isAmbi= map(int, f.read().strip().split(","))
            #print(r, g, b, speed, m, o1, o2, o3)
            return r,g,b, speed, m, o1, o2, o3, isAmbi
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
            if result != []:
                ambibuffer = result
                return result
            else: 
                return ambibuffer
    except:
        return "AAA"

red = 200
green = 0
blue = 0
mode = 0
o1 = 10
o2 = 50
o3 = 255

ambirange1 = (11,20)
ambirange2 = (31,40)

def colourpixel(r,g,b):
    nr=int(r*maxbrightness)
    ng=int(g*maxbrightness)
    nb=int(b*maxbrightness)
    return((nr,ng,nb))

def rgb_to_hex(rgb):
    if not all(0 <= value <= 255 for value in rgb):
        raise ValueError("RGB values must be between 0 and 255")
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def drawLeds(pixels):
    canvas.delete("all")  # Clear the canvas before drawing
    for i, pixel in enumerate(pixels):
        canvas.create_rectangle(i*20, 0, (i*20)+10, 10, fill=rgb_to_hex(pixel))

def update_pixels():
    
    global pixelclock, pixels, red, green, blue, speed, mode, o1, o2, o3, traillen
    red, green, blue, speed, mode, o1, o2, o3, isAmbi= read_color()
    #print(pixels)
    # Update the pixels based on the mode
    
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
                        #print(sparkle)
                        sparkles.remove(sparkle)
                        continue
                    pixels[sparkle[0]] = colourpixel(
                        max(0, int(red - o2 + sparkle[1])),
                        max(0, int(green - o2 + sparkle[1])),
                        max(0, int(blue - o2 + sparkle[1]))
                    )
                    sparkle[1] = sparkle[1]-1
                    #print(sparkle)

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

    drawLeds(pixels)
    pixelclock = (pixelclock + 1) % len(pixels)
    root.after(251-speed, update_pixels)  # Schedule the next update

# Initial drawing
drawLeds(pixels)

# Start the update loop
root.after(100, update_pixels)

# Start the Tkinter event loop
root.mainloop()