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

    # this can all be done in preprocessing
    self.xs = POINTS_3D[:, 0]
    self.zs = POINTS_3D[:, 1]
    self.ys = POINTS_3D[:, 2]
    self.thetas = np.arctan2(self.xs, self.zs)

    self.new_xs = np.repeat(np.expand_dims(self.thetas, -1).T, self.num_particles, axis=0)
    self.new_ys = np.repeat(np.expand_dims((self.ys - self.min_alt) / (self.max_alt - self.min_alt), -1).T, self.num_particles, axis=0)

  def renderNextFrame(self):
    

    # these need to be repeated for all of the lights, so it should be 500 x 50

    # need to create the brightness array, which is 500 x 1 (or just 500,)

    # the result needs to be a 500 x 3 array

    # up until here

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
    brightness = 1.0 - np.clip(result - 0.2, 0.0, 1.0)
    condition1 = brightness > 0.95
    condition2 = np.logical_and(brightness <= 0.95, brightness > 0.85)
    condition3 = brightness <= 0.85
    # self.frameBuf[condition1] = np.array([self.max_brightness, self.max_brightness, (brightness[condition1]-0.95)*self.max_brightness/0.05])
    self.frameBuf[condition1, 0] = self.max_brightness
    self.frameBuf[condition1, 1] = self.max_brightness
    self.frameBuf[condition1, 2] = (brightness[condition1]-0.95)*self.max_brightness/0.05
    
    self.frameBuf[condition2, 0] = (brightness[condition2]-0.85)*self.max_brightness/0.1
    self.frameBuf[condition2, 1] = self.max_brightness
    self.frameBuf[condition2, 2] = 0.0

    self.frameBuf[condition3, 0] = 0.0
    self.frameBuf[condition3, 1] = brightness[condition3]*self.max_brightness/0.85
    self.frameBuf[condition3, 2] = 0.0

    # self.frameBuf[condition2] = np.array([(brightness[condition2]-0.85)*self.max_brightness/0.1, self.max_brightness, 0.0])
    # self.frameBuf[condition3] = np.array([0.0, brightness[condition3]*self.max_brightness/0.85, 0.0])
    self.step_particles()

  # def get_colour(self, x, y):
  #   result = y*0.5
  #   scale = self.particles[:, 1] + 1.0
  #   dxs = (self.particles[:, 0] + np.pi - x) % (2.0 * np.pi) - np.pi
  #   dys = self.particles[:, 1] - y
  #   f = (dxs * dxs + dys * dys) / (self.radius_sq * scale * scale)

  #   test = f < 1.0
  #   nottest = np.logical_not(test)
  #   f[test] = (1.0 - f[test]**2) * self.particles[test, 1]
  #   f[nottest] = 0.0

  #   result += np.sum(f)
  #   brightness = 1.0 - min(max(result-0.2, 0.0), 1.0)

  #   # try basing the hue on brightness value? eh that's kinda hard

  #   if brightness > 0.95:
  #     return [self.max_brightness, self.max_brightness, (brightness-0.95)*self.max_brightness/0.05]
  #   elif brightness > 0.85:
  #     return [(brightness-0.85)*self.max_brightness/0.1, self.max_brightness, 0.0]
  #   else:
  #     return [0.0, brightness*self.max_brightness/0.85, 0.0]
    
  # def get_colour_3d(self, x, z, y):
  #   theta = math.atan2(x, z)
  #   return self.get_colour(theta, (y - self.min_alt)/(self.max_alt - self.min_alt))

  def step_particles(self):
    # move the particles
    self.particles[:, 1] += 0.1 * self.speed
    self.particles[:, 0] += self.particles[:, 2] * self.speed
    self.particles[self.particles[:, 1] > 1.5, 1] -= 2.0
