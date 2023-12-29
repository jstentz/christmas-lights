import numpy as np
import random
import math
from typing import Optional
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class FastFire(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = None, brightness : int = 255, speed : float = 0.2, radius_sq : float = 0.1, particles : int = 50):
    super().__init__(frameBuf, fps)
    self.min_alt = np.min(POINTS_3D[:, 2])
    self.max_alt = np.max(POINTS_3D[:, 2])

    # Max brightness  (0 - 255)
    self.max_brightness = brightness

    # how quickly the flames animate
    self.speed = speed

    # size of negative-flame particles
    self.radius_sq = radius_sq

    # number of negative-flame particles
    self.num_particles = particles

    # Create the particles
    # stores x, y, and dx
    self.particles = np.random.rand(self.num_particles, 3)
    # scale the dimensions as the other guy does
    self.particles[:, 0] *= 2.0 * np.pi
    self.particles[:, 1] = 2.0 * self.particles[:, 1] - 0.5 
    self.particles[:, 2] = (self.particles[:, 2] - 0.5) * 0.1

  def renderNextFrame(self):
    for i in range(len(POINTS_3D)):
      coord = POINTS_3D[i]
      color = self.get_colour_3d(coord[0], coord[1], coord[2])

      # convert to rgb from grb
      self.frameBuf[i] = np.array([color[1], color[0], color[2]])

    # do get_colour_3d but on all them at once
    # colors = 

    self.step_particles()

  def get_colour(self, x, y):
    result = y*0.5
    # do value_at for all the particles at once
    # values = np.copy(self.particles)
    scale = self.particles[:, 1] + 1.0

    dxs = (self.particles[:, 0] + np.pi - x) % (2.0 * np.pi) - np.pi
    dys = self.particles[:, 1] - y
    f = (dxs * dxs + dys * dys) / (self.radius_sq * scale * scale)

    test = f < 1.0
    nottest = np.logical_not(test)
    f[test] = (1.0 - f[test]**2) * self.particles[test, 1]
    f[nottest] = 0.0

    result += np.sum(f)
    brightness = 1.0 - min(max(result-0.2, 0.0), 1.0)

    # try basing the hue on brightness value? eh that's kinda hard

    if brightness > 0.95:
      return [self.max_brightness, self.max_brightness, (brightness-0.95)*self.max_brightness/0.05]
    elif brightness > 0.85:
      return [(brightness-0.85)*self.max_brightness/0.1, self.max_brightness, 0.0]
    else:
      return [0.0, brightness*self.max_brightness/0.85, 0.0]
    
  def get_colour_3d(self, x, z, y):
    theta = math.atan2(x, z)
    return self.get_colour(theta, (y - self.min_alt)/(self.max_alt - self.min_alt))

  def step_particles(self):
    # move the particles
    self.particles[:, 1] += 0.1 * self.speed
    self.particles[:, 0] += self.particles[:, 2] * self.speed
    self.particles[self.particles[:, 1] > 1.5, 1] -= 2.0
