import os
import board
import random
import neopixel
from time import sleep
import tkinter as tk
import colorsys

colorfile = "./color.txt"
lastUpdateTime = os.path.getmtime(colorfile)
activefile = "./check.txt"
lastActiveUpdateTime = os.path.getmtime(activefile)
defaultbrightness = 0.2
pixelclock = 0 # Pixelclock indexes through every one LED each tick ! NOT for updating all LEDs, rather for moving effects
sparkles = [] # List to save all Sparkling pixels

#Strip init
pixels = neopixel.NeoPixel(board.D18, n=150, brightness=defaultbrightness, auto_write=False)

#Initialization sequence - 5x Flashing green
for x in range(10):
    for i in range(len(pixels)):
        if(x%2 == 0):
            pixels[i]=(0,255,0)
        else:
            pixels[i]=(0,0,0)
            
    pixels.show()        
    if(x%2 == 0):
        sleep(0.1)
    else:
        sleep(0.4)

def read_color():
    global lastUpdateTime #To be able to modify it
    currentUpdateTime = os.path.getmtime(colorfile)
    if lastUpdateTime != currentUpdateTime:#If the actual modify date on the file does not match the last recorded modification, there has been an update.
        lastUpdateTime = currentUpdateTime #That time is now the new last recorded update
        try:
            with open(colorfile, "r") as f:
                values = list(map(int, f.read().strip().split(",")))
                color_data = {
                    "r": values[0],
                    "g": values[1],
                    "b": values[2],
                    "speed": values[3],
                    "mode": values[4],
                    "o1": values[5],
                    "o2": values[6],
                    "o3": values[7],
                    "isAmbi": values[8],
                    "brightness": values[9]
                }
                pixels.brightness = defaultbrightness * min((color_data.brightness/100),1) #sets the strip objects own brightness value from 0 to the default brightness to avoid too much power draw
                return color_data
        except:
            print("No color-file found")
            return {"r": 20, "g": 0, "b": 0,"speed": 0, "m": 0,"o1": 0, "o2": 0, "o3": 0,"isAmbi": 0, "brightness": 100}

def read_active():
    global lastActiveUpdateTime #To be able to modify it
    currentActiveUpdateTime = os.path.getmtime(colorfile)
    if lastActiveUpdateTime != currentActiveUpdateTime:#If the actual modify date on the file does not match the last recorded modification, there has been an update.
        lastActiveUpdateTime = currentActiveUpdateTime #That time is now the new last recorded update
        try:
            return open(activefile, "r").read()
        except:
            print("No activation-file found")
            return 0
        
#Main loop:
while True:
    if(read_active()==1):

        settings = read_color()

        match settings["mode"]:

            case 0:
                for i in range(len(pixels)):#Flat, single colour throughout the strip
                    pixels[i] = (settings["r"],settings["g"],settings["b"])

            case 1: #Light Pulse | o1 = overall length of pulse | o2 = max additional brightness in center of pulse !!to prevent overbrightness, same value is decresed from rest!!
                for i in range(len(pixels)):
                    pixels[i] = (max(0, settings["r"] - settings["o2"]), max(0, settings["g"] - settings["o2"]), max(0, settings["b"] - settings["o2"]))
                for spec in range(settings["o1"]):
                    index = ((spec - (int(settings["o1"] / 2))) + pixelclock) % len(pixels)
                    factor = abs(1 - abs(spec - (int(settings["o1"] / 2))) / int(settings["o1"] / 2))
                    pixels[index] = (
                        max(int(factor * settings["o2"] + (settings["r"] - settings["o2"])), 0),
                        max(int(factor * settings["o2"] + (settings["g"] - settings["o2"])), 0),
                        max(int(factor * settings["o2"] + (settings["b"] - settings["o2"])), 0)
                    )

            case 2: #Sparkle
                if random.random() * 100 < settings["o1"]:
                    sparkles.insert(0, [int(random.random() * len(pixels)), settings["o2"]])
                for i in range(len(pixels)):
                    pixels[i] = (max(0, settings["r"] - settings["o2"]), max(0, settings["g"] - settings["o2"]), max(0, settings["b"] - settings["o2"]))
                for sparkle in sparkles:
                    if sparkle[1] <= 0:
                        sparkles.remove(sparkle)
                        continue
                    sparkle[1] = sparkle[1]-1
                    pixels[sparkle[0]] = (
                        max(0, int(settings["r"] - settings["o2"] + sparkle[1])),
                        max(0, int(settings["g"] - settings["o2"] + sparkle[1])),
                        max(0, int(settings["b"] - settings["o2"] + sparkle[1]))
                    )
                    
            case 3: #rng
                for i in range(len(pixels)):
                    pixels[i] = (0,0,0)
                    pixels[pixelclock] = (settings["r"], settings["g"], settings["b"])
                    pixels[(pixelclock-1)/len(pixels)] = (int(settings["r"]/2), int(settings["g"]/2), int(settings["b"]/2))
                    pixels[(pixelclock-2)/len(pixels)] = (int(settings["r"]/3), int(settings["g"]/3), int(settings["b"]/3))

            case 4:  # RGB Rainbow Wave
                for i in range(len(pixels)):
                    hue = (pixelclock + i) / len(pixels)
                    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                    pixels[i] = (r * 255, g * 255, b * 255)

            case 5: #dynamic 2 colour gradient
                half_length = len(pixels) // 2
                pixelclock_mod = pixelclock % len(pixels)

                for i in range(len(pixels)):
                    gradient_factor = ((pixelclock_mod - i) % half_length) / half_length

                    if (i > pixelclock_mod and i <= pixelclock_mod + half_length) or (i > pixelclock_mod - len(pixels) and i <= pixelclock_mod - len(pixels) + half_length):
                        pixels[i] = (
                            max(0, settings["r"] + gradient_factor * (settings["o1"] - settings["r"])),
                            max(0, settings["g"] + gradient_factor * (settings["o2"] - settings["g"])),
                            max(0, settings["b"] + gradient_factor * (settings["o3"] - settings["b"]))
                        )
                    else:
                        pixels[i] = (
                            max(0, settings["o1"]  + gradient_factor * (settings["r"] - settings["o1"])),
                            max(0, settings["o2"]  + gradient_factor * (settings["g"] - settings["o2"])),
                            max(0, settings["o3"]  + gradient_factor * (settings["b"] - settings["o3"]))
                        )

            case 6: #static 2 colour gradient
                for i in range(len(pixels)):
                    pixels[i] = (max(0, settings["r"] + ((i)%(len(pixels))/(len(pixels))) * (settings["o1"]-settings["r"])), max(0,  settings["g"] + ((i)%(len(pixels))/(len(pixels))) * (settings["o2"]-settings["g"])), max(0,  settings["b"] + ((i)%(len(pixels))/(len(pixels))) * (settings["o3"]-settings["b"])))
    
        pixelclock = (pixelclock+1)%len(pixels) # Pixelclock indexes through every one LED each tick ! NOT for updating all LEDs, rather for moving effects
        pixels.show()
        #end of IF

    sleep(0.25)
    #end of while true