from lights.animations.base import BaseAnimation
from typing import Optional, Collection

class SingleColor(BaseAnimation):
  def __init__(self, pixels, *, fps: Optional[int] = None, color: Collection[int] = (255,255,255)):
    super().__init__(pixels, fps=fps)
    self.pixels.fill(color)

  def renderNextFrame(self):
    pass