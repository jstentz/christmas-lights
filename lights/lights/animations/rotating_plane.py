import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class RotatingPlane(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, rotation_speed : float = 0.05, 
               bandwidth : float = 0.2, color : Collection[int] = (255, 255, 255), decay : float = 0.95):
    super().__init__(frameBuf, fps)

    self.rotation_speed = rotation_speed
    self.bandwidth = bandwidth
    self.decay = decay

    # center the points at the mid points
    min_pt = np.min(POINTS_3D, axis=0)
    max_pt = np.max(POINTS_3D, axis=0)
    mid_point = (max_pt + min_pt) / 2
    self.CENTERED_POINTS_3D = POINTS_3D - mid_point
    self.color = color

    # generate a random initial angle for the plane
    self.plane = RotatingPlane.generateRandomPlane()
    self.target = RotatingPlane.generateRandomPlane()
  
  # pick a random unit vector in 3D space
  @staticmethod
  def generateRandomPlane():
    while np.all((plane := np.random.normal(size=3)) == 0.0):
      pass
    return plane / np.linalg.norm(plane)

  def renderNextFrame(self):
    # decay the pixels
    self.frameBuf[:] *= self.decay

    # light up the lights within the bandwidth
    within = np.abs(np.dot(self.CENTERED_POINTS_3D, self.plane)) < (self.bandwidth / 2)
    self.frameBuf[within] = self.color

    # make progress towards the target plane
    diffs = self.target - self.plane
    diffs /= np.linalg.norm(diffs)
    self.plane += diffs * self.rotation_speed
    self.plane /= np.linalg.norm(self.plane)

    # move the target if we are close to it
    # TODO: make this related to rotation_speed so we don't overstep it 
    epsilon = self.rotation_speed
    if np.linalg.norm(self.plane - self.target) < epsilon:
      self.target = RotatingPlane.generateRandomPlane()