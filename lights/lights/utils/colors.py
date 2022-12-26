import random
import colorsys

def randomColor():
  return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def hsv_to_rgb(h, s, v):
  return (int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))

def rgb_to_hsv(r, g, b):
  return colorsys.rgb_to_hsv(r, g, b)
