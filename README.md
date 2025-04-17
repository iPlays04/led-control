# led-control
For controlling Neopixel LEDs using a Raspberry Pi 3 via Webserver

server.py hosts the Webserver on port 8080 of the local IP-Adress and writes into color and check files

client.py controls the colours of the LEDs using the PIs pin (GPIO18)

color.txt saves the colour values set on the website and lets the client application read them

check.txt saves the state of the LED 0 - off | 1 - on
