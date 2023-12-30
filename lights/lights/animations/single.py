from lights.animations.base import BaseAnimation
from typing import Optional, Collection
from lights.utils.validation import is_valid_rgb_color

class Single(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = None, color: Collection[int] = (230, 80, 255), light: int = 0):
    super().__init__(frameBuf, fps=fps)
    self.frameBuf[:] = 0
    self.frameBuf[light] = color
    
  def renderNextFrame(self):
    pass
        
  @classmethod
  def validate_parameters(cls, parameters):
    super().validate_parameters(parameters)
    full_parameters = {**cls.get_default_parameters(), **parameters}
    color = full_parameters['color']
    light = full_parameters['light']

    if not is_valid_rgb_color(color):
      raise TypeError("color must be a valid rgb color tuple")
    if light < 0 or light >= 500:
      raise TypeError("light must be in the range [0, 500]")