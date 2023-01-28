from lights.animations.base import BaseAnimation
from typing import Optional, Collection
from lights.utils.validation import is_valid_rgb_color

class SingleColor(BaseAnimation):
  def __init__(self, pixels, *, fps: Optional[int] = None, color: Collection[int] = (255,255,255)):
    super().__init__(pixels, fps=fps)
    self.pixels.fill(color)

  def renderNextFrame(self):
    pass

  @classmethod
  def validate_parameters(cls, parameters):
    super().validate_parameters(parameters)
    full_parameters = {**cls.get_default_parameters(), **parameters}
    color = full_parameters['color']

    if not is_valid_rgb_color(color):
      raise TypeError("color must be a valid rgb color tuple")