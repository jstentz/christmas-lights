from lights.animations.base import BaseAnimation

# An animation for empirically measuring animation fps.

class Benchmark(BaseAnimation):
  def __init__(self, pixels, *, color=(255,0,0), fps=None):
    super().__init__(pixels, fps=fps)
    self.pixels = pixels
    self.color = color
    self.i = 0

  def renderNextFrame(self):
    prev = self.i - 1 if self.i != 0 else len(self.pixels) - 1
    self.pixels[self.i] = self.color
    self.pixels[prev] = (0, 0, 0)
    self.i = (self.i + 1) % len(self.pixels)
