from lights.animations.base import BaseAnimation
from lights.utils.colors import rgb_to_hsv, hsv_to_rgb
from typing import Optional, Collection
from lights.utils.validation import is_valid_rgb_color

class Solid(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = None, color: Collection[int] = (255, 255, 255), brightness: float = 1):
    super().__init__(frameBuf, fps=fps)
    self.color = color
    self.brightness = brightness
    
  def renderNextFrame(self):
    h, s, _ = rgb_to_hsv(*self.color)
    c = hsv_to_rgb(h, s, self.brightness)
    self.frameBuf[:] = c
        
  @classmethod
  def validate_parameters(cls, parameters):
    super().validate_parameters(parameters)
    full_parameters = {**cls.get_default_parameters(), **parameters}
    color = full_parameters['color']
    brightness = full_parameters['brightness']

    if not is_valid_rgb_color(color):
      raise TypeError("color must be a valid rgb color tuple")
    if brightness < 0 or brightness > 1:
      raise TypeError("brightness must be in the range [0, 1]")