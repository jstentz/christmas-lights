import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D
from noise import pnoise3

class Spotlight(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, color: Collection[int] = (255, 255, 255), speed: float = 5e-3, radius: float = 0.4):
    super().__init__(frameBuf, fps)

    self.color = color
    self.pos = np.zeros(3)
    self.time = np.random.uniform(0, 100, 3)  # Random initial time for Perlin noise
    self.speed = speed
    self.radius = radius
    self.max_pt = np.max(POINTS_3D, axis=0)
    self.min_pt = np.min(POINTS_3D, axis=0)

  def renderNextFrame(self):
    # Compute distances
    distances = np.linalg.norm(POINTS_3D - self.pos, axis=1)

    # Normalize distances to the range [0, 1]
    min_distance = np.min(distances)
    max_distance = np.max(distances)
    normalized_distances = (distances - min_distance) / (max_distance - min_distance)
    self.frameBuf[:] = ((1 - normalized_distances) ** 6)[:, np.newaxis] * self.color

    # Generate Perlin noise for all three axes
    noise_values = np.array([
        pnoise3(self.time[0], 0, 0),
        pnoise3(0, self.time[1], 0),
        pnoise3(0, 0, self.time[2])
    ])

    # Map Perlin noise values to bounding box
    self.pos = self.min_pt + (self.max_pt - self.min_pt) * (noise_values + 1) / 2

    # Increment time vector for Perlin noise evolution
    self.time += self.speed
