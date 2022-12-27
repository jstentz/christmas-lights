import random
import colorsys

def rainbowFrame(t, NUM_PIXELS):
  """
  Generates rgb values for a rainbow gradient at time t.
  """
  return [[int(v * 255) for v in colorsys.hsv_to_rgb((c + t) % NUM_PIXELS / NUM_PIXELS, 1.0, 1.0)] for c in range(NUM_PIXELS)]

def randomColor():
  h = random.uniform(0, 1)
  s = 1
  v = 1
  return hsv_to_rgb(h, s, v)

def hsv_to_rgb(h, s, v):
  return [int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v)]

def rgb_to_hsv(r, g, b):
  return colorsys.rgb_to_hsv(r/255, g/255, b/255)

def decayPixel(r, g, b, decayRate):
  h, s, v = rgb_to_hsv(r, g, b)
  return hsv_to_rgb(h, s, v * decayRate)
