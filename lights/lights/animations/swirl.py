import numpy as np
from typing import Optional, Collection
from lights.utils.colors import hsv_to_rgb_numpy
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D
from noise import pnoise1

# NOTE: This animation assumes the points are distributed roughly in the shape of the surface of a cone or a cylinder.
class Swirl(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, speed : float = 4.0, colors: Collection[Collection[int]] = [(255, 0, 0), (0, 255, 0), (0, 0, 255)], twist: bool = True, rainbow: bool = False):
    super().__init__(frameBuf, fps)

    self.speed = np.deg2rad(speed)
    self.colors = np.array(colors)
    self.twist = twist
    self.rainbow = rainbow
    self.twistScale = 1.0

    # Leverage the assumption that (0, 0, 0) is the bottom of a cylinder / cone
    self.theta = 0
    self.t = 0
    self.lightThetas = np.arctan2(POINTS_3D[:, 1], POINTS_3D[:, 0]) + np.pi
    self.height = np.max(POINTS_3D) - np.min(POINTS_3D)
    self.thetaOffsets = POINTS_3D[:, 2] / self.height * (2 * np.pi)
    self.thetas = np.mod((self.lightThetas + self.thetaOffsets), 2 * np.pi)

  def renderNextFrame(self):
    if self.twist:
      self.thetaOffsets = POINTS_3D[:, 2] / self.height * (2 * np.pi) * self.twistScale
      self.thetas = np.mod((self.lightThetas + self.thetaOffsets), 2 * np.pi)
      self.twistScale = min(max(self.twistScale + self.speed, 0), 2.5)
      
    alignedThetas = np.mod(self.thetas + self.theta, 2 * np.pi)
    
    if self.rainbow:
      h = alignedThetas / (2 * np.pi)
      s = np.ones(h.shape)
      v = np.ones(h.shape)
      self.frameBuf[:] = 255 * hsv_to_rgb_numpy(np.hstack((h[:, None], s[:, None], v[:, None])))
    else:
      c = np.floor(len(self.colors) * alignedThetas / (2 * np.pi)).astype(int)
      self.frameBuf[:] = self.colors[c]
  
    self.theta = (self.theta + self.speed) % (2 * np.pi)
    self.t += 1