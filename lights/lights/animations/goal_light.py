import numpy as np
from lights.utils.colors import hsv_to_rgb_numpy, rgb_to_hsv
from typing import Optional, Collection
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

# NOTE: This animation assumes the points are distributed roughly in the shape of the surface of a cone or a cylinder.
class GoalLight(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, speed : float = 15.0, sliceWidth: float = 90.0, backgroundColor: Collection[int] = (255, 0, 0), minSaturation: float = 0.8):
    super().__init__(frameBuf, fps)

    self.speed = np.deg2rad(speed)
    self.sliceWidth = np.deg2rad(sliceWidth)
    self.backgroundColor = backgroundColor
    self.backgroundColorHSV = rgb_to_hsv(backgroundColor[0], backgroundColor[1], backgroundColor[2])
    self.minSaturation = minSaturation

    # Leverage the assumption that (0, 0, 0) is the bottom of a cylinder / cone
    self.theta = 0
    self.lightThetas = np.arctan2(POINTS_3D[:, 1], POINTS_3D[:, 0]) + np.pi

  def renderNextFrame(self):
    self.frameBuf[:] = self.backgroundColor
    alignedThetas = (self.lightThetas + self.theta) % (2 * np.pi)
    inBeam = alignedThetas < self.sliceWidth
    # decay the saturation towards the center of the beam
    s = (self.backgroundColorHSV[1] - self.minSaturation) * (2 * np.abs(alignedThetas[inBeam] - self.sliceWidth / 2) / self.sliceWidth) + self.minSaturation
    h = np.ones(s.shape) * self.backgroundColorHSV[0]
    v = np.ones(s.shape)
    hsv = np.hstack((h[:, None], s[:, None], v[:, None]))
    self.frameBuf[inBeam] = hsv_to_rgb_numpy(hsv) * 255

    self.theta = (self.theta + self.speed) % (2 * np.pi)