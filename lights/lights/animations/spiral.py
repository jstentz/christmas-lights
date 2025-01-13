import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D


class Spiral(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60):
    super().__init__(frameBuf, fps)
    self.t = 0


  def renderNextFrame(self):
    CENTERED_POINTS_3D = POINTS_3D - np.mean(POINTS_3D, axis=0)
    self.mags = np.linalg.norm(CENTERED_POINTS_3D[:, [0, 1]], axis=1)
    self.thetas = np.arctan2(CENTERED_POINTS_3D[:, 1], CENTERED_POINTS_3D[:, 0]) + np.pi + self.t

    a = 0.15
    colors = np.array([[255, 0, 0], [255, 255, 255], [0, 0, 255]])
    threshold = np.max(self.mags) / (len(colors) + 1)
    threshold /= 2
    indices = ((np.abs(self.mags - a * self.thetas) // threshold) % len(colors)).astype(np.int32)

    self.frameBuf[:] = colors[indices]
    self.t += 0.05