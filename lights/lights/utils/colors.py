import random
import colorsys
import numpy as np

def rainbowFrame(t, NUM_PIXELS):
  """
  Generates rgb values for a rainbow gradient at time t.
  """
  return [[int(v * 255) for v in colorsys.hsv_to_rgb((c + t) % NUM_PIXELS / NUM_PIXELS, 1.0, 1.0)] for c in range(NUM_PIXELS)]

def brightnessFrame(color, NUM_PIXELS):
  h, s, _ = rgb_to_hsv(*color)
  return [hsv_to_rgb(h, s, (c+1) / NUM_PIXELS) for c in range(NUM_PIXELS)]

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

def desaturatePixel(r, g, b, desaturationRate):
  h, s, v = rgb_to_hsv(r, g, b)
  return hsv_to_rgb(h, s * desaturationRate, v)

# Below functions taken from https://gist.github.com/PolarNick239/691387158ff1c41ad73c
def rgb_to_hsv_numpy(rgb):
    r, g, b = rgb[:, 0], rgb[:, 1], rgb[:, 2]

    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    v = maxc

    deltac = maxc - minc
    s = deltac / maxc
    deltac[deltac == 0] = 1  # to not divide by zero (those results in any way would be overridden in next lines)
    rc = (maxc - r) / deltac
    gc = (maxc - g) / deltac
    bc = (maxc - b) / deltac

    h = 4.0 + gc - rc
    h[g == maxc] = 2.0 + rc[g == maxc] - bc[g == maxc]
    h[r == maxc] = bc[r == maxc] - gc[r == maxc]
    h[minc == maxc] = 0.0

    h = (h / 6.0) % 1.0
    res = np.dstack([h, s, v])
    return res

def hsv_to_rgb_numpy(hsv):
    h, s, v = hsv[:, 0], hsv[:, 1], hsv[:, 2]

    i = np.int32(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    rgb = np.zeros_like(hsv)
    v, t, p, q = v.reshape(-1, 1), t.reshape(-1, 1), p.reshape(-1, 1), q.reshape(-1, 1)
    rgb[i == 0] = np.hstack([v, t, p])[i == 0]
    rgb[i == 1] = np.hstack([q, v, p])[i == 1]
    rgb[i == 2] = np.hstack([p, v, t])[i == 2]
    rgb[i == 3] = np.hstack([p, q, v])[i == 3]
    rgb[i == 4] = np.hstack([t, p, v])[i == 4]
    rgb[i == 5] = np.hstack([v, p, q])[i == 5]
    rgb[s == 0.0] = np.hstack([v, v, v])[s == 0.0]

    return rgb