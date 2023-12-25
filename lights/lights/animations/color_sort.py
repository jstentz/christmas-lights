from lights.animations.base import BaseAnimation
import random
from lights.utils.colors import rainbowFrame, rgb_to_hsv
from typing import Optional

class ColorSort(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = None):
    super().__init__(frameBuf, fps=fps)
    NUM_PIXELS = len(self.frameBuf)
    self.sortedIdx = 0
    self.frameBuf[:] = rainbowFrame(0, NUM_PIXELS)
    for _ in range(NUM_PIXELS):
      self.randomSwap()
    
  def randomSwap(self):
    NUM_PIXELS = len(self.frameBuf)
    i0 = random.randint(0, NUM_PIXELS - 1)
    i1 = random.randint(0, NUM_PIXELS - 1)
    c0 = self.frameBuf[i0]
    c1 = self.frameBuf[i1]
    self.frameBuf[i0] = c1
    self.frameBuf[i1] = c0

  # assign random colors, then on each call to the function, run one round of selection sort
  def renderNextFrame(self):
    NUM_PIXELS = len(self.frameBuf)
    if self.sortedIdx == NUM_PIXELS:
      self.sortedIdx = 0
      self.frameBuf[:] = rainbowFrame(0, NUM_PIXELS)
      for _ in range(NUM_PIXELS):
        self.randomSwap()
    else:
      minHIdx = None
      minH = None
      for i in range(self.sortedIdx, NUM_PIXELS):
        (h, _, _) = rgb_to_hsv(*self.frameBuf[i]) # might have to do *tuple(pixels[i])
        if minH == None or h < minH:
          minH = h
          minHIdx = i
      # swap!
      self.frameBuf[[self.sortedIdx, minHIdx]] = self.frameBuf[[minHIdx, self.sortedIdx]]
      self.sortedIdx += 1
