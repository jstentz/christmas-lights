from lights.animations.base import BaseAnimation
from lights.utils.colors import hsv_to_rgb
import math
from typing import Optional

class RainbowSine(BaseAnimation):
  # exp must be an even number >= 2 and freq must be >= 1
  def __init__(self, frameBuf, *, fps: Optional[int] = None, freq: float = 1, exp: float = 10):
    super().__init__(frameBuf, fps=fps)
    self.freq = freq
    self.exp = exp
    self.t = 0
    
  def renderNextFrame(self):
    NUM_PIXELS = len(self.frameBuf)
    t = self.t
    freq = self.freq
    exp = self.exp
    for i in range(NUM_PIXELS):
      c = (i + t) % NUM_PIXELS
      h = math.sin(i * math.pi / NUM_PIXELS)
      s = 1.0
      v = math.sin(c * math.pi * freq / NUM_PIXELS)**exp # change exponent for faster brightness drop off
      self.frameBuf[i] = hsv_to_rgb(h, s, v)
    self.t += 1
        
  @classmethod
  def validate_parameters(cls, parameters):
    super().validate_parameters(parameters)
    full_parameters = {**cls.get_default_parameters(), **parameters}
    freq = full_parameters['freq']
    exp = full_parameters['exp']

    if freq < 1:
      raise TypeError("freq must be >= 1")
    if exp < 2:
      raise TypeError("exp must be >= 2")