import numpy as np
from lights.utils.colors import hsv_to_rgb
from typing import Optional
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class SweepingPlanes(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, speed : float = 0.05, bandwidth : float = 0.2, decay : float = 0.85):
    super().__init__(frameBuf, fps)

    self.speed = speed
    self.bandwidth = bandwidth
    self.decay = decay

    # center the points at the mid points
    min_pt = np.min(POINTS_3D, axis=0)
    max_pt = np.max(POINTS_3D, axis=0)
    mid_point = (max_pt + min_pt) / 2

    self.CENTERED_POINTS_3D = POINTS_3D - mid_point

    # possibly add some to this so the band of light starts outside the tree
    self.radius = np.max(np.linalg.norm(self.CENTERED_POINTS_3D, axis=1)) + bandwidth
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
    self.color = np.array(hsv_to_rgb(np.random.rand(), 1.0, 1.0))
    

  def renderNextFrame(self):
    # d is distance from origin
    d = np.dot(-self.plane, self.point)
    distances = np.abs(np.dot(self.CENTERED_POINTS_3D, self.plane) + d) / np.linalg.norm(self.plane)
    within = distances < self.bandwidth
    self.frameBuf[within] = self.color
    self.frameBuf[np.logical_not(within)] = self.frameBuf[np.logical_not(within)].astype(np.float64) * self.decay

    # move the plane (move the point in the direction normal to the plane)
    self.point += self.plane * self.speed

    if np.linalg.norm(self.point) > self.radius:
      self.generateRandomPlane()