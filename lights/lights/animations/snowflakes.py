from lights.animations.base import BaseAnimation
from lights.utils.colors import decayPixel
import random
from typing import Optional, Collection

class Snowflakes(BaseAnimation):
  def __init__(self, pixels, *, fps: Optional[int] = 30, density: float = .005, decayRate: float = .99, color: Collection[int] = (148,231,255)):
    super().__init__(pixels, fps=fps)
    self.density = density
    self.decayRate = decayRate
    self.color = color

  def renderNextFrame(self):
    blank = [0, 0, 0]
    for i in range(len(self.pixels)):
      self.pixels[i] = decayPixel(*self.pixels[i], self.decayRate)
      if self.pixels[i] == list(blank):
        n = random.uniform(0, 1)
        if n < self.density:
          self.pixels[i] = self.color