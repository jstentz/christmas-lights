from lights.animations.base import BaseAnimation
from lights.utils.colors import decayPixel
import random
from typing import Optional, Collection
from lights.utils.validation import is_valid_rgb_color

class Snowflakes(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = 30, density: float = .005, decayRate: float = .99, color: Collection[int] = (148,231,255)):
    super().__init__(frameBuf, fps=fps)
    self.density = density
    self.decayRate = decayRate
    self.color = color

  def renderNextFrame(self):
    blank = [0, 0, 0]
    for i in range(len(self.frameBuf)):
      self.frameBuf[i] = decayPixel(*self.frameBuf[i], self.decayRate)
      if self.frameBuf[i].tolist() == list(blank):
        n = random.uniform(0, 1)
        if n < self.density:
          self.frameBuf[i] = self.color

  @classmethod
  def validate_parameters(cls, parameters):
    super().validate_parameters(parameters)
    full_parameters = {**cls.get_default_parameters(), **parameters}
    density = full_parameters['density']
    decayRate = full_parameters['decayRate']
    color = full_parameters['color']

    if not is_valid_rgb_color(color):
      raise TypeError("color must be a valid rgb color tuple")
    if density < 0 or density > 1:
      raise TypeError("density must be in the range [0, 1]")
    if decayRate < 0 or decayRate > 1:
      raise TypeError("decayRate must be in the range [0, 1]")