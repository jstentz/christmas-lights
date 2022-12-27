from lights.animations.base import BaseAnimation
import random
from lights.utils.colors import rainbowFrame, rgb_to_hsv

class ColorSort(BaseAnimation):
  def __init__(self, pixels, *, fps=None):
    super().__init__(pixels, fps=fps)
    self.pixels = pixels
    NUM_PIXELS = len(self.pixels)
    self.sortedIdx = 0
    self.pixels[:] = rainbowFrame(0, NUM_PIXELS)
    for _ in range(NUM_PIXELS):
      self.randomSwap()
    
  def randomSwap(self):
    NUM_PIXELS = len(self.pixels)
    i0 = random.randint(0, NUM_PIXELS - 1)
    i1 = random.randint(0, NUM_PIXELS - 1)
    c0 = self.pixels[i0]
    c1 = self.pixels[i1]
    self.pixels[i0] = c1
    self.pixels[i1] = c0

  # assign random colors, then on each call to the function, run one round of selection sort
  def renderNextFrame(self):
    NUM_PIXELS = len(self.pixels)
    if self.sortedIdx == NUM_PIXELS:
      self.sortedIdx = 0
      self.pixels[:] = rainbowFrame(0, NUM_PIXELS)
      for _ in range(NUM_PIXELS):
        self.randomSwap()
    else:
      minHIdx = None
      minH = None
      for i in range(self.sortedIdx, NUM_PIXELS):
        (h, _, _) = rgb_to_hsv(*self.pixels[i]) # might have to do *tuple(pixels[i])
        if minH == None or h < minH:
          minH = h
          minHIdx = i
      # swap!
      c1 = self.pixels[self.sortedIdx]
      c2 = self.pixels[minHIdx]
      self.pixels[self.sortedIdx] = c2
      self.pixels[minHIdx] = c1
      self.sortedIdx += 1
