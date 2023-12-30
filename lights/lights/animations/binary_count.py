from numpy import ndarray
from lights.animations.base import BaseAnimation
from typing import Optional, Collection

class BinaryCount(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = None, color: Collection[int] = (0,255,0)):
    super().__init__(frameBuf, fps=fps)
    self.color = color
    self.t = 0

  def renderNextFrame(self):
    NUM_PIXELS = len(self.frameBuf)
    maxVal = 2**NUM_PIXELS - 1
    v = self.t % maxVal
    newPixels = [int(i) for i in '{0:0b}'.format(v)]
    for i in range(len(newPixels)):
      if newPixels[i]:
        self.frameBuf[i] = self.color
      else:
        self.frameBuf[i] = (0, 0, 0)
    self.t += 1
