from lights.animations.base import BaseAnimation
from lights.utils.colors import decayPixel
from typing import Optional, Collection
from lights.utils.validation import is_valid_rgb_color
import numpy as np
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

class Snowflakes(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = 30, density: float = .005, decayRate: float = .99, color: Collection[int] = (148,231,255)):
    super().__init__(frameBuf, fps=fps)
    self.density = density
    self.decayRate = decayRate
    self.color = rgb_to_hsv(np.array(color) / 255)
    self.hsvFrame = np.zeros(self.frameBuf.shape)
    self.blankThresh = 1/255

  def renderNextFrame(self):
    # decay all existing snowflakes.
    self.hsvFrame[:, 2] *= self.decayRate
    # randomly spawn new snowflakes.
    rands = np.random.uniform(0, 1, size=len(self.hsvFrame))
    self.hsvFrame[np.logical_and(self.hsvFrame[:, 2] < self.blankThresh, rands < self.density)] = self.color

    # convert to rgb.
    self.frameBuf[:] = hsv_to_rgb(self.hsvFrame) * 255

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