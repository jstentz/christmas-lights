import numpy as np
from typing import Optional
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class BrightnessWave(BaseAnimation):

  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = None, step: float = np.pi / 200):
    super().__init__(frameBuf, fps)
    self.t = 0
    self.step = step

  def renderNextFrame(self):
    # Define an update function for the animation to change colors
    self.t += self.step
    colors = self.frameBuf.astype(float)
    colorin = (np.sin(3 * (POINTS_3D[:, 0] + self.t)) / 1.3) < POINTS_3D[:, 2]
    colors[colorin] = np.array([0, 0, 0])
    colors[np.logical_not(colorin)] = np.array([255, 255, 255])
    self.frameBuf[:] = colors.astype(np.uint8)