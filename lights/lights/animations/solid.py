from lights.animations.base import BaseAnimation
from lights.utils.colors import rgb_to_hsv, hsv_to_rgb

class Solid(BaseAnimation):
  def __init__(self, pixels, *, color=(255, 255, 255), brightness=1, fps=None):
    super().__init__(pixels, fps=fps)
    self.color = color
    self.brightness = brightness
    
  def renderNextFrame(self):
    h, s, _ = rgb_to_hsv(*self.color)
    c = hsv_to_rgb(h, s, self.brightness)
    self.pixels.fill(c)
        