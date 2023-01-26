from lights.animations.base import BaseAnimation
from typing import Optional

class Off(BaseAnimation):
  def __init__(self, pixels, *, fps: Optional[int] = None):
    super().__init__(pixels, fps=fps)
    self.pixels.fill((0, 0, 0))
    self.firstFrame = True

  def renderNextFrame(self):
    while self.running and not self.firstFrame:
      pass
    self.firstFrame = False