'''
Not sure if it is worth importing these modules below. You can basically
just treat the 'pixels' variable as a list of (r, g, b) values where r, g, and b
are between 0 - 255. It's actually an object where they redefine the indexing
operation, so you can't actually straight up set it equal to a list, you need
to edit it. Some of the functions I gave below might be useful for that.

'''
import board
import neopixel
import random
import time
import colorsys
import math

random.seed(time.time())

ORDER = neopixel.RGB
NUM_PIXELS = 500
pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS, auto_write=False, pixel_order=ORDER)

def clearLights():
    for i in range(NUM_PIXELS):
        pixels[i] = (0, 0, 0)

def updatePixelsFromList(L):
    for i in range(len(L)):
        pixels[i] = L[i]

# most functions will want to know the time
def yourFunction(t):
    return 42 # lol

# example function
# exp must be an even number >= 2 and freq must be >= 1
def rainbowSine(t, freq=1, exp=10):
    for i in range(NUM_PIXELS):
        c = (i + t) % NUM_PIXELS
        h = math.sin(i * math.pi / NUM_PIXELS)
        s = 1.0
        v = math.sin(c * math.pi * freq / NUM_PIXELS)**exp # change exponent for faster brightness drop off
        pixels[i] = tuple([int(v * 255) for v in colorsys.hsv_to_rgb(h, s, v)])

# general framwork
t = 0
while True:
    # insert function call here!
    yourFunction(t)
    pixels.show()
    # add a time.sleep(seconds) here if its too fast!
    t += 1