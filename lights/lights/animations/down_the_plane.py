import numpy as np
from typing import Optional
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class DownThePlane(BaseAnimation):

  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = None, step: float = np.pi / 64, epsilon: float = 0.1, decay: float = 0.95):
    super().__init__(frameBuf, fps)
    self.angle = 0
    self.step = step
    self.epsilon = epsilon
    self.decay = decay

  def renderNextFrame(self):
    # Define an update function for the animation to change colors
    self.frameBuf *= self.decay
    self.angle += self.step
    plane1 = np.array([np.sin(self.angle), np.cos(self.angle), 0])
    plane2 = np.array([np.sin(self.angle - np.pi/2), np.cos(self.angle - np.pi/2), 0])

    dots1 = POINTS_3D @ plane1.reshape((-1, 1))
    dots2 = POINTS_3D @ plane2.reshape((-1, 1))
    self.frameBuf[(np.abs(dots1) < self.epsilon).reshape((-1,))] = (255, 0, 0)
    self.frameBuf[(np.abs(dots2) < self.epsilon).reshape((-1,))] = (0, 255, 0)