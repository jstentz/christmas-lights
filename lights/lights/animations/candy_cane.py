import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class CandyCane(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, speed : float = 0.02, 
               rotation_speed : float = 0.01, bandwidth : float = 0.8, colors : Collection[Collection[int]] = ((255, 0, 0), (255, 255, 255))):
    super().__init__(frameBuf, fps)

    self.speed = speed
    self.rotation_speed = rotation_speed
    self.bandwidth = bandwidth

    # center the points at the mid points
    min_pt = np.min(POINTS_3D, axis=0)
    max_pt = np.max(POINTS_3D, axis=0)
    mid_point = (max_pt + min_pt) / 2
    self.CENTERED_POINTS_3D = POINTS_3D - mid_point

    # self.colors = np.array([(255, 0, 0), (255, 255, 255), (0, 255, 0), (255, 255, 255)]) # red, white, green, white
    self.colors = np.array([(255, 0, 0), (255, 255, 255)]) # red, white
    # self.colors = np.array([(255, 0, 0), (255, 255, 255), (0, 0, 255), (255, 255, 255)]) # red, white, blue

    self.t = 0

    # generate a random initial angle for the plane
    self.plane = CandyCane.generateRandomPlane()
    self.target = CandyCane.generateRandomPlane()
  
  # pick a random unit vector in 3D space
  @staticmethod
  def generateRandomPlane():
    while np.all((plane := np.random.normal(size=3)) == 0.0):
      pass
    return plane / np.linalg.norm(plane)

  def renderNextFrame(self):
    distances = np.dot(self.CENTERED_POINTS_3D, self.plane) + self.t
    indices = ((distances // self.bandwidth) % len(self.colors)).astype(np.int32)
    colors = self.colors[indices]
    self.frameBuf[:] = colors

    # increment the time by the speed 
    self.t += self.speed

    # make progress towards the target plane
    diffs = self.target - self.plane
    self.plane += diffs * self.rotation_speed
    self.plane /= np.linalg.norm(self.plane)

    # move the target if we are close to it
    # TODO: make this related to rotation_speed so we don't overstep it 
    epsilon = 0.01
    if np.linalg.norm(self.plane - self.target) < epsilon:
      self.target = CandyCane.generateRandomPlane()