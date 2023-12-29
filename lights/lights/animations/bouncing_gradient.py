import numpy as np
from matplotlib.colors import hsv_to_rgb
from typing import Optional
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class BouncingGradient(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = None, speed : float = 0.05):
    super().__init__(frameBuf, fps)
    # create the bounding box
    self.mins = np.min(POINTS_3D, axis=0)
    self.maxs = np.max(POINTS_3D, axis=0)
    self.loc = np.array([0, 0, 0]).astype(np.float64)
    self.color = np.array([255, 255, 255])
    
    # pick random unit vector and scale by speed
    self.dir = np.random.rand(3) - 0.5
    self.dir /= np.linalg.norm(self.dir)
    self.dir *= speed

  def renderNextFrame(self):
    # move the ball
    self.loc += self.dir

    # find the dims where we are out of bounds
    dims_min = self.loc < self.mins
    dims_max = self.loc > self.maxs

    # snap ball to min / max
    self.loc[dims_min] = self.mins[dims_min]
    self.loc[dims_max] = self.maxs[dims_max]

    # change the direction where we collide
    self.dir[np.logical_or(dims_min, dims_max)] *= -1

    # light up lights based on distances
    distances = np.linalg.norm(POINTS_3D - np.expand_dims(self.loc, 0), axis=1)

    hsv = np.ones((len(self.frameBuf), 3))
    hsv[:, 0] = (np.max(distances) - distances) / np.max(distances)

    self.frameBuf[:] = hsv_to_rgb(hsv) * 255