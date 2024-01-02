import numpy as np
from matplotlib.colors import hsv_to_rgb
from typing import Optional
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class SweepingWave(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, speed : float = 0.05, drop_off : float = 3.0, margin : float = 1.0):
    super().__init__(frameBuf, fps)

    self.speed = speed
    self.drop_off = drop_off

    # center the points at the mid points
    min_pt = np.min(POINTS_3D, axis=0)
    max_pt = np.max(POINTS_3D, axis=0)
    mid_point = (max_pt + min_pt) / 2

    self.CENTERED_POINTS_3D = POINTS_3D - mid_point

    # possibly add some to this so the band of light starts outside the tree
    self.radius = np.max(np.linalg.norm(self.CENTERED_POINTS_3D, axis=1)) + margin
    self.generateRandomPlane()
  
  # pick a random point along the sphere that circumscribes the points
  def generateRandomPlane(self):
    self.point = np.random.normal(size=3)

    # TODO: this is a bad way to handle this
    if np.all(self.point == 0.0):
      self.generateRandomPlane()
      return
    
    self.point /= np.linalg.norm(self.point)
    self.point *= self.radius

    # make vector pointing towards the center of tree
    self.plane = -self.point / np.linalg.norm(self.point)
    self.hue = np.random.rand()
    

  def renderNextFrame(self):
    # d is distance from origin
    d = np.dot(-self.plane, self.point)
    dists = (np.abs(np.dot(self.CENTERED_POINTS_3D, self.plane) + d) / np.linalg.norm(self.plane))
    dists = np.exp(-dists * self.drop_off)

    hsv = np.empty((len(self.frameBuf), 3)).astype(np.float64)
    hsv[:, 0] = self.hue
    hsv[:, 1] = 1.0
    hsv[:, 2] = dists

    self.frameBuf[:] = hsv_to_rgb(hsv) * 255

    # move the plane (move the point in the direction normal to the plane)
    self.point += self.plane * self.speed

    if np.linalg.norm(self.point) > self.radius:
      self.generateRandomPlane()