from lights.animations.base import BaseAnimation

class SingleColor(BaseAnimation):
  def __init__(self, pixels, *, color=(255,255,255), fps=None):
    super().__init__(pixels, fps=fps)
    self.pixels.fill(color)

  def renderNextFrame(self):
    pass