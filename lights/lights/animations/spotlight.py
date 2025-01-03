import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class Spotlight(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, color : Collection[int] = (255, 255, 255), speed: float = 0.05):
    super().__init__(frameBuf, fps)

    self.color = color
    self.pos = np.zeros(3)
    self.dir = np.random.uniform(-1, 1, 3) * speed
    self.max_pt = np.max(POINTS_3D, axis=0)
    self.min_pt = np.min(POINTS_3D, axis=0)

  def renderNextFrame(self):
    # get distances
    distances = np.linalg.norm(POINTS_3D - self.pos, axis=1)

    # normalize distances to the range [0, 1]
    min_distance = np.min(distances)
    max_distance = np.max(distances)
    normalized_distances = (distances - min_distance) / (max_distance - min_distance)
    self.frameBuf[:] = ((1 - normalized_distances) ** 4)[:, np.newaxis] * self.color

    # move the ball and see if we're out of bounds now
    self.pos += self.dir

    out_of_min_bound = self.pos < self.min_pt
    out_of_max_bound = self.pos > self.max_pt

    # reverse velocity where the point is out of bounds
    self.dir[out_of_min_bound | out_of_max_bound] *= -1

    # snap the point back to the boundary
    self.pos = np.maximum(self.pos, self.min_pt)
    self.pos = np.minimum(self.pos, self.max_pt)