from numpy import ndarray
from lights.animations.base import BaseAnimation
from lights.utils.validation import is_valid_rgb_color
from typing import Collection, Optional

# An animation for empirically measuring animation fps.

class Benchmark(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = None, color: Collection[int] = (255,0,0)):
    super().__init__(frameBuf, fps=fps)
    self.color = color
    self.i = 0

  def renderNextFrame(self):
    prev = self.i - 1 if self.i != 0 else len(self.frameBuf) - 1
    self.frameBuf[self.i] = self.color
    self.frameBuf[prev] = (0, 0, 0)
    self.i = (self.i + 1) % len(self.frameBuf)

  @classmethod
  def validate_parameters(cls, parameters):
    super().validate_parameters(parameters)
    full_parameters = {**cls.get_default_parameters(), **parameters}
    if not is_valid_rgb_color(full_parameters['color']):
      raise TypeError("color must be a valid rgb color tuple")
