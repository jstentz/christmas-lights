import numpy as np
import random
import math
from typing import Optional
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class Particle:
  def __init__(self):
    self.x = random.random() * math.pi*2.0
    self.y = random.random() * 2.0 - 0.5
    self.dx = (random.random() - 0.5) * 0.1

  def step(self, t):
    self.y += 0.1 * t
    self.x += self.dx * t
    if self.y > 1.5:
      self.y -= 2.0

  def dist_sq(self, x, y):
    dx = (self.x + math.pi - x) % (2.0*math.pi) - math.pi
    dy = self.y - y
    return dx*dx + dy*dy

  def value_at(self, x, y, radius_sq):
    scale = self.y + 1.0
    f = self.dist_sq(x, y) / (radius_sq * scale * scale)
    if f < 1.0:
      return (1.0 - f * f) * self.y
    else:
      return 0.0

class Fire(BaseAnimation):
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
    self.particles = [Particle() for _ in range(self.num_particles)]

  def renderNextFrame(self):
    for i in range(len(POINTS_3D)):
      coord = POINTS_3D[i]
      color = self.get_colour_3d(coord[0], coord[1], coord[2])

      # convert to rgb from grb
      self.frameBuf[i] = np.array([color[1], color[0], color[2]])

    self.step_particles()

  def get_colour(self, x, y):
    result = y*0.5
    for p in self.particles:
      result += p.value_at(x, y, self.radius_sq)
    brightness = 1.0 - min(max(result-0.2, 0.0), 1.0)

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
    for p in self.particles:
      p.step(self.speed)
