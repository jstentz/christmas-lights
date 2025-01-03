import numpy as np
from lights.utils.colors import hsv_to_rgb
from typing import Optional, List
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class SphericalMiracle(BaseAnimation):

  class GrowingSphere:
    def __init__(self, x: float, y: float, z: float, r: float, thickness: float, color: np.ndarray):
      self.center = np.array([x, y, z])
      self.r = r
      self.thickness = thickness
      self.color = color

    # retval: whether the sphere should be deleted
    def step(self, frameBuf: np.ndarray, pts3d: np.ndarray, dr: float) -> bool:
      # compute all point distances to the sphere center
      distances = np.linalg.norm(pts3d - self.center, axis=1)
      insideOut = distances < self.r
      outsideIn = distances > (self.r - self.thickness)
      contained = insideOut & outsideIn
      frameBuf[contained] = self.color
      insideIn = distances < (self.r - self.thickness)
      self.r += dr
      return np.all(insideIn)

  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, sphereFrequency : float = 1.0, maxSpheres: int = 3, startRadius : float = 0.2, thickness : float = 0.2, speed : float = 0.01):
    super().__init__(frameBuf, fps)

    self.fireRate = sphereFrequency / self.fps
    self.startRadius = startRadius
    self.thickness = thickness
    self.speed = speed
    self.colors = np.array([[0, 255, 0], [255, 0, 0], [0, 0, 255]])
    self.maxSpheres = maxSpheres
    self.spheres: List[self.GrowingSphere] = []

    self.mins, self.maxes = np.min(POINTS_3D, axis=0), np.max(POINTS_3D, axis=0)
    self.bbSize = self.maxes - self.mins

  def randomColor(self):
    h = np.random.uniform(0, 1)
    s = 1
    v = 1
    return hsv_to_rgb(h, s, v)

  def createSphere(self):
    c = self.randomColor()
    r = self.startRadius
    x, y, z = np.random.uniform(self.mins - 0.5 * self.bbSize, self.maxes + 0.5 * self.bbSize)
    self.spheres.append(self.GrowingSphere(x, y, z, r, self.thickness, c))

  def renderNextFrame(self):
    self.frameBuf[:] = np.array([0, 0, 0])
    if np.random.rand() < self.fireRate and len(self.spheres) < self.maxSpheres:
      self.createSphere()
    spheres = []
    for sphere in self.spheres:
      if not sphere.step(self.frameBuf, POINTS_3D, self.speed):
        spheres.append(sphere)
    self.spheres = spheres