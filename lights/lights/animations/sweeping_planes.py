import numpy as np
from typing import Optional
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class SweepingPlanes(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, speed : float = 0.05, bandwidth : float = 0.2):
    super().__init__(frameBuf, fps)

    self.speed = speed
    self.bandwidth = bandwidth

    # center the points at the mid points
    min_pt = np.min(POINTS_3D, axis=0)
    max_pt = np.max(POINTS_3D, axis=0)
    mid_point = (max_pt + min_pt) / 2

    self.CENTERED_POINTS_3D = POINTS_3D - mid_point

    # possibly add some to this so the band of light starts outside the tree
    self.radius = np.max(np.linalg.norm(self.CENTERED_POINTS_3D, axis=1))
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
    self.color = (np.random.rand(3) * 255).astype(np.int8)
    

  def renderNextFrame(self):
    # d is distance from origin
    d = np.dot(-self.plane, self.point)
    distances = np.abs(np.dot(self.CENTERED_POINTS_3D, self.plane) + d) / np.linalg.norm(self.plane)
    within = distances < self.bandwidth
    self.frameBuf[within] = self.color
    self.frameBuf[np.logical_not(within)] = np.zeros(3)

    # move the plane (move the point in the direction normal to the plane)
    self.point += self.plane * self.speed

    if np.linalg.norm(self.point) > self.radius:
      self.generateRandomPlane()

    

'''
find a points perpendicular distance to a plane in 3d space (dot product?)
then set its brightness based on the square distance to the line
generate another plane

a plane in 3d space is defined by 

pick a point on the plane r0, and a normal vector to the plane n
points on the plane r satisfy

n * (r - r0) = 0


'''