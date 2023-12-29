import numpy as np
from typing import Optional
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class Fire(BaseAnimation):
  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, brightness : int = 255, speed : float = 0.2, radius_sq : float = 0.06, particles : int = 20):
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

    # this can all be done in preprocessing
    self.xs = POINTS_3D[:, 0]
    self.zs = POINTS_3D[:, 1]
    self.ys = POINTS_3D[:, 2]
    self.thetas = np.arctan2(self.xs, self.zs)

    self.new_xs = np.repeat(np.expand_dims(self.thetas, -1).T, self.num_particles, axis=0)
    self.new_ys = np.repeat(np.expand_dims((self.ys - self.min_alt) / (self.max_alt - self.min_alt), -1).T, self.num_particles, axis=0)

  def renderNextFrame(self):
    result = (self.ys - self.min_alt) / (self.max_alt - self.min_alt)*0.5
    scale = self.particles[:, 1] + 1.0
    dxs = (np.expand_dims(self.particles[:, 0], -1) + np.pi - self.new_xs) % (2.0 * np.pi) - np.pi
    dys = np.expand_dims(self.particles[:, 1], -1) - self.new_ys
    f = (dxs * dxs + dys * dys) / np.expand_dims((self.radius_sq * scale * scale), -1)

    test = f < 1.0
    nottest = np.logical_not(test)
    f[test] = (1.0 - f[test]**2) * self.new_ys[test]
    f[nottest] = 0.0

    result += np.sum(f, axis=0)
    brightness = 1.0 - np.clip(result - 0.2, 0.2, 1.0)

    thresh1 = 0.85
    thresh2 = 0.65

    condition1 = brightness > thresh1
    condition2 = np.logical_and(brightness <= thresh1, brightness > thresh2)
    condition3 = brightness <= thresh2

    self.frameBuf[condition1, 1] = self.max_brightness
    self.frameBuf[condition1, 0] = self.max_brightness
    self.frameBuf[condition1, 2] = (brightness[condition1]-thresh1)*self.max_brightness/(1 - thresh1)
    
    self.frameBuf[condition2, 1] = (brightness[condition2]-thresh2)*self.max_brightness/(1 - thresh2)
    self.frameBuf[condition2, 0] = self.max_brightness
    self.frameBuf[condition2, 2] = 0.0

    self.frameBuf[condition3, 1] = 0.0
    self.frameBuf[condition3, 0] = brightness[condition3]*self.max_brightness/thresh2
    self.frameBuf[condition3, 2] = 0.0
    self.step_particles()


  def step_particles(self):
    # move the particles
    self.particles[:, 1] += 0.1 * self.speed
    self.particles[:, 0] += self.particles[:, 2] * self.speed
    self.particles[self.particles[:, 1] > 1.5, 1] -= 2.0
