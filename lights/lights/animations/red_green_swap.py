from lights.animations.base import BaseAnimation
from typing import Optional

class RedGreenSwap(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = 1):
    super().__init__(frameBuf, fps=fps)
    self.t = 0

  def renderNextFrame(self):
    for i in range(len(self.frameBuf)):
      if self.t % 2 == 0:
        if i % 2 == 0:
          self.frameBuf[i] = (255, 0, 0)
        else:
          self.frameBuf[i] = (0, 255, 0)
      else:
        if i % 2 != 0:
          self.frameBuf[i] = (255, 0, 0)
        else:
          self.frameBuf[i] = (0, 255, 0)
    self.t += 1
