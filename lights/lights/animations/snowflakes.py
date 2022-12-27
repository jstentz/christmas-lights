from lights.animations.base import BaseAnimation
import random

class Snowflakes(BaseAnimation):
  def __init__(self, pixels, fps=30, density=.005, decayRate=.99):
    super().__init__(pixels, fps=fps)
    self.density = density
    self.decayRate = decayRate

  def renderNextFrame(self):
    snow = (0, 0, 255)
    blank = (0, 0, 0)
    
    for i in range(len(self.pixels)):
      color = self.pixels[i]
      self.pixels[i] = tuple([int(c * self.decayRate) for c in color])
      if self.pixels[i] == list(blank):
        n = random.uniform(0, 1)
        if n < self.density:
          self.pixels[i] = snow