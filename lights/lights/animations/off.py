from lights.animations.base import BaseAnimation
from typing import Optional

class Off(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = None):
    super().__init__(frameBuf, fps=fps)
    self.frameBuf[:] = 0

  def renderNextFrame(self):
    pass