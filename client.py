import board
import neopixel
import random
from time import sleep

pixels = neopixel.NeoPixel(board.D18, 24)

#pixels.brightness(0.3)

traillen = 16

maxbrightness = 0.3

def read_color():
    try:
        with open("./color.txt", "r") as f:
            r, g, b, m, o1, o2 = map(int, f.read().strip().split(","))
            return int((r/100)*255*maxbrightness), int((g/100)*255*maxbrightness), int((b/100)*255*maxbrightness), m, o1, o2
    except:
        return 2, 2, 10  # default color

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
            case 1: #Light Pulse | o1 = overall length of pulse | o2 = max additional brightness in center of pulse !!to prevent overbrightness, same value is decresed from rest!!
                for pixel in pixels: #goes through every LED to assign a value
                    pixel=(red-o2,green-o2,blue-o2)
                for spec in range(o1): #goes through all the LEDs to assing values for those effected by special effect
                    pixels[((spec-(int(o1/2)))+pixelclock)%len(pixelclock)] = (int(abs(1-abs(spec-(int(o1/2)))/int(o1/2))*o2+(red-o2)),int(abs(1-abs(spec-(int(o1/2)))/int(o1/2))*o2+(green-o2)),int(abs(1-abs(spec-(int(o1/2)))/int(o1/2))*o2+(blue-o2)))

            case 2: #Sparkle
                sparkles = []
                if(random()*100<o1):
                    sparkles.insert(0,(int(random()*len(pixels)),o2*(random*5)))
                for pixel in pixels: #goes through every LED to assign a value
                    pixel=(red-o2,green-o2,blue-o2)
                for sparkle in range(len(sparkles)):
                    if(sparkles[sparkle][1]<=0):
                        sparkles.pop(sparkle)
                        continue
                    pixels[sparkles[sparkle][0]]=(red-(sparkles[sparkle][1]),green-(sparkles[sparkle][1]),blue-(sparkles[sparkle][1]))
                    sparkles[sparkle][1]=sparkles[sparkle][1]-1


                

    else:
        sleep(0.1)

    pixelclock = (pixelclock+1)%len(pixels)
