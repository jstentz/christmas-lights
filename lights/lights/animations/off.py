from lights.animations.base import BaseAnimation

class Off(BaseAnimation):
  def __init__(self, pixels, *, color=(0,255,0), fps=None):
    super().__init__(pixels, fps=fps)
    self.pixels.fill((0, 0, 0))

  def renderNextFrame(self):
    pass