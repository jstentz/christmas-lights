from lights.animations.base import BaseAnimation
from lights.utils.colors import hsv_to_rgb
import math
from typing import Optional

class ColorSine(BaseAnimation):
  # exp must be an even number >= 2 and freq must be >= 1
  def __init__(self, pixels, *, fps: Optional[int] = None, freq: float = 1, exp: float = 2):
    super().__init__(pixels, fps=fps)
    self.freq = freq
    self.exp = exp
    self.t = 0
    
  def renderNextFrame(self):
    NUM_PIXELS = len(self.pixels)
    for i in range(NUM_PIXELS):
      c = (i + self.t) % NUM_PIXELS
      h = math.sin(c * math.pi * self.freq / NUM_PIXELS)**self.exp # change exponent for faster brightness drop off
      s = 1.0
      v = 1.0
      self.pixels[i] = hsv_to_rgb(h, s, v)
    self.t += 1
        
        