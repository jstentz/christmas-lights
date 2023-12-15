from lights.animations.base import BaseAnimation
from lights.utils.colors import hsv_to_rgb
from typing import Optional, Collection
import numpy as np
import random

class MergeSort(BaseAnimation):

  class Merger:
    def __init__(self, l, m, r):
      self.l = l
      self.m = m
      self.r = r
      self.li = self.l
      self.ri = self.m
      self.fi = 1
      self.lColor = None
      self.rColor = None
      self.aux = [(0, 0, 0)] * (r - l)
      # print(self.l, self.m, self.r, self.li, self.ri)

    @classmethod
    def fromMergers(cls, merger1: "MergeSort.Merger", merger2: "MergeSort.Merger"):
      assert merger1.r == merger2.l
      return MergeSort.Merger(merger1.l, merger1.r, merger2.r)
    
    def step(self, pixels, focusColor) -> bool:
      if self.li >= self.m and self.ri >= self.r:
        return True

      # focus current indices and save the old color.
      if setlMarker := self.lColor is None and self.li < self.m:
        pixels[self.li], self.lColor = focusColor, pixels[self.li]
      if setrMarker := self.rColor is None and self.ri < self.r:
        pixels[self.ri], self.rColor = focusColor, pixels[self.ri]
      if setlMarker or setrMarker:
        return False
      
      if self.li >= self.m:
        self._advance_right(pixels)
        return False
      if self.ri >= self.r:
        self._advance_left(pixels)
        return False

      # pixels are assumed hsv tuples
      if self.lColor[-1] <= self.rColor[-1]:
        self._advance_left(pixels)
      else:
        self._advance_right(pixels)

      return False

    def finish(self, pixels, focusColor):
      if self.fi >= len(self.aux):
        pixels[self.l + self.fi - 1] = self.aux[self.fi - 1]
        return True
      
      pixels[self.l + self.fi] = focusColor
      pixels[self.l + self.fi - 1] = self.aux[self.fi - 1]
      self.fi += 1
      return False

    def _advance_left(self, pixels):
      self.aux[self.li - self.l + self.ri - self.m] = self.lColor
      pixels[self.li] = self.lColor
      self.li += 1
      self.lColor = None

    def _advance_right(self, pixels):
      self.aux[self.li - self.l + self.ri - self.m] = self.rColor
      pixels[self.ri] = self.rColor
      self.ri += 1
      self.rColor = None

  def __init__(self, pixels, *, fps: Optional[int] = None, hue: int = 25, brightnessRange: Collection[int] = (50, 255), focusColor: Collection[int] = (0, 255, 255)):
    super().__init__(pixels, fps)
    self.hue = hue
    self.brightnessRange = brightnessRange
    self.focusColor = (focusColor[0] / 255, focusColor[1] / 255, focusColor[2] / 255)
    self.sortedColors = [(hue / 255, 1.0, b) for b in np.linspace(brightnessRange[0] / 255, brightnessRange[1] / 255, len(self.pixels))]
    self.reset()
    self.rgbColors = [tuple(hsv_to_rgb(*hsv)) for hsv in self.sortedColors]
    self.pixels[:] = self.rgbColors

  def reset(self):
    self.phase = "merge"
    self.mergers: Collection[MergeSort.Merger] = [MergeSort.Merger(l, l+1, l+2) for l in range(0, len(self.pixels), 2)]
    random.shuffle(self.sortedColors)
    
  def renderNextFrame(self):
    if self.phase == "merge":
      finished = True
      for merger in self.mergers:
        finished &= merger.step(self.sortedColors, self.focusColor)
      if finished:
        self.phase = "present"
    elif self.phase == "present":
      finished = True
      for merger in self.mergers:
        finished &= merger.finish(self.sortedColors, self.focusColor)
      if finished:
        if len(self.mergers) == 1:
          self.reset()
        else:
          newMergers = [MergeSort.Merger.fromMergers(self.mergers[i], self.mergers[i+1]) for i in range(0, len(self.mergers) // 2 * 2, 2)]
          if len(self.mergers) % 2 != 0:
            newMergers.append(self.mergers[-1])
          self.mergers = newMergers
          self.phase = "merge"

    self.pixels[:] = [tuple(hsv_to_rgb(*hsv)) for hsv in self.sortedColors]
    
  @classmethod
  def validate_parameters(cls, parameters):
    super().validate_parameters(parameters)
    full_parameters = {**cls.get_default_parameters(), **parameters}
    hue = full_parameters['hue']
    brightnessRange = full_parameters['brightnessRange']

    if hue < 0 or hue > 255:
      raise TypeError("hue must be a value in [0, 255]")
    if len(brightnessRange) != 2 or brightnessRange[0] >= brightnessRange[1]:
      raise TypeError("brightnessRange must be a valid range tuple")
