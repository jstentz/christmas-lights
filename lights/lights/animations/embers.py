# Animation courtesy of Austin Schick :)

from lights.animations.base import BaseAnimation
from lights.utils.colors import desaturatePixel, decayPixel
import random
from perlin_noise import PerlinNoise
from typing import Optional, Collection
from lights.utils.validation import is_valid_rgb_color

desaturatePixel = decayPixel

def lerp(a, b, t):
    return (1 - t) * a + t * b

def normalize(l):
  lMax = max(l)
  lMin = min(l)
  return [(x - lMin) / (lMax - lMin) for x in l]

def generateNoise(pixels, frequency):
  base = random.random()
  noise1 = PerlinNoise(octaves=1)
  noise = []
  for x in range(len(pixels)):
      noiseVal = noise1(base + x / len(pixels) * frequency)
      noise.append(noiseVal)
  noise = normalize(noise)
  return noise

class Embers(BaseAnimation):
  def __init__(self, pixels, *, fps: Optional[int] = 30, color: Collection[int] = (255, 195, 0)):
    super().__init__(pixels, fps=fps)
    # self.color = desaturatePixel(*color, 0.8)
    self.color = color

    # Least active
    # self.frequencies = (8,)
    # self.durations = (2,)

    # More active
    # self.frequencies = (8, 50)
    # self.durations = (2, 0.25)

    # Very active
    # self.frequencies = (8, 50, 90)
    # self.durations = (2, 0.25, 0.15)

    # different settings
    self.frequencies = (100, 150)
    self.durations = (.1, .2)

    self.frames = [0, 0, 0]
    self.durationsInFrames = [int(fps * s) for s in self.durations]

    self.octaves = len(self.frequencies)

    self.noise = [[None]*self.octaves, [None]*self.octaves]
    for octave in range(self.octaves):
      self.shiftNoise(octave)
      self.shiftNoise(octave)

  def shiftNoise(self, octave):
    self.noise[0][octave] = self.noise[1][octave]
    self.noise[1][octave] = generateNoise(self.pixels, self.frequencies[octave])
    self.frames[octave] = 0

  def renderNextFrame(self):
    for octave in range(self.octaves):
      if self.frames[octave] >= self.durationsInFrames[octave]:
        self.shiftNoise(octave)
      self.frames[octave] += 1

    for i in range(len(self.pixels)):
      # Base noise calculation
      t = self.frames[0] / self.durationsInFrames[0]
      desaturationValue = 1 - (lerp(self.noise[0][0][i], self.noise[1][0][i], t) * 0.7)

      #higher octaves
      for j in range(1, self.octaves):
        t = self.frames[j] / self.durationsInFrames[j]
        currOctaveValue = (lerp(self.noise[0][j][i], self.noise[1][j][i], t) - 0.5) * 0.5 ** j
        desaturationValue = max(min(desaturationValue + currOctaveValue, 1), 0)

      self.pixels[i] = desaturatePixel(*self.color, desaturationValue)

  @classmethod
  def validate_parameters(cls, parameters):
    super().validate_parameters(parameters)
    full_parameters = {**cls.get_default_parameters(), **parameters}
    color = full_parameters['color']

    if not is_valid_rgb_color(color):
      raise TypeError("color must be a valid rgb color tuple")
  
