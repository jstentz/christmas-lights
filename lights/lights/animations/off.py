from lights.animations.base import BaseAnimation
from typing import Optional

class Off(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = None):
    super().__init__(frameBuf, fps=fps)
    self.frameBuf[:] = 0
    self.firstFrame = True

  def renderNextFrame(self):
    while self.running and not self.firstFrame:
      pass
    self.firstFrame = False