import tkinter as tk
import random
from time import sleep
import colorsys
import math

'''

Testenv

'''

pixels = [(0, 0, 0)]*150

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
            r, g, b, speed, m, o1, o2, o3, isAmbi, brightness= map(int, f.read().strip().split(","))
            #print(r, g, b, speed, m, o1, o2, o3)
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
        canvas.create_rectangle(i*10, 0, (i*10)+10, 10, fill=rgb_to_hex(pixel))

def update_pixels():
    
    global pixelclock, pixels, red, green, blue, speed, mode, o1, o2, o3, traillen
    red, green, blue, speed, mode, o1, o2, o3, isAmbi, brightness= read_color()
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
                    pixels[i] = (0,0,0)
                    pixels[(pixelclock+1)%len(pixels)] = (int(red/4), int(green/4), int(blue/4))
                    pixels[pixelclock] = (red, green, blue)
                    pixels[(pixelclock-1)%len(pixels)] = (int(red/2), int(green/2), int(blue/2))
                    pixels[(pixelclock-2)%len(pixels)] = (int(red/3), int(green/3), int(blue/3))
                
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
            
            case 10: # Fire/Candle Flicker
                # Base color for fire (e.g., orange-red)
                base_hue = (o3 / 360.0) + (15 / 360.0) # Start around orange (15-30 degrees)
                base_saturation = 1.0
                base_value = 1.0 # Max brightness for calculation

                for i in range(len(pixels)):
                    # Introduce randomness for flicker
                    # o2 controls how often pixels change (higher o2 means more frequent changes)
                    if random.random() < (o2 / 10.0): # Adjust probability based on o2
                        # Random brightness variation based on o1
                        brightness_variation = (random.random() * (o1 / 100.0))
                        current_value = max(0.1, base_value - brightness_variation) # Ensure it doesn't go completely dark

                        # Slight random hue shift for more natural fire look
                        hue_shift = (random.random() - 0.5) * (o3 / 1000.0) # Small shift around base_hue
                        current_hue = (base_hue + hue_shift) % 1.0

                        r, g, b = colorsys.hsv_to_rgb(current_hue, base_saturation, current_value)
                        pixels[i] = colourpixel(int(r * 255), int(g * 255), int(b * 255))
                    # If not changing, keep the previous color (or slowly fade, more complex)
                    # For simplicity, this version only updates a subset of pixels each tick
                    # A more advanced version would store pixel states and fade them.

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

    drawLeds(pixels)
    pixelclock = (pixelclock + 1) % len(pixels)
    root.after(251-speed, update_pixels)  # Schedule the next update

# Initial drawing
drawLeds(pixels)

# Start the update loop

root.after(100, update_pixels)

# Start the Tkinter event loop
root.mainloop()