import random
import colorsys

def randomColor():
  h = random.uniform(0, 1)
  s = 1
  v = 1
  return hsv_to_rgb(h, s, v)

def hsv_to_rgb(h, s, v):
  return [int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v)]

def rgb_to_hsv(r, g, b):
  return colorsys.rgb_to_hsv(r, g, b)
