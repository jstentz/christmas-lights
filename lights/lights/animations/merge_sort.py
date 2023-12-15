from lights.animations.base import BaseAnimation
from lights.utils.colors import hsv_to_rgb
from lights.utils.validation import is_valid_rgb_color, is_valid_inclusive_range
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
      self.init = False
      self.aux = [(0, 0, 0)] * (r - l)
      self.brightnessAux = [0] * (r - l)

    @classmethod
    def fromMergers(cls, merger1: "MergeSort.Merger", merger2: "MergeSort.Merger"):
      assert merger1.r == merger2.l
      return MergeSort.Merger(merger1.l, merger1.r, merger2.r)
    
    def step(self, brightnesses, pixels, focusColor) -> bool:
      if self.li >= self.m and self.ri >= self.r:
        return True
      
      if not self.init:
        if self.li < self.m:
          pixels[self.li], self.lColor = focusColor, pixels[self.li]
        if self.ri < self.r:
          pixels[self.ri], self.rColor = focusColor, pixels[self.ri]
        self.init = True
      
      if self.li >= self.m:
        self._advance_right(brightnesses, pixels, focusColor)
        return False
      if self.ri >= self.r:
        self._advance_left(brightnesses, pixels, focusColor)
        return False

      if brightnesses[self.li] <= brightnesses[self.ri]:
        self._advance_left(brightnesses, pixels, focusColor)
      else:
        self._advance_right(brightnesses, pixels, focusColor)

      return False

    def finish(self, brightnesses, pixels, focusColor):
      if self.fi >= len(self.aux):
        pixels[self.l + self.fi - 1] = self.aux[self.fi - 1]
        brightnesses[self.l + self.fi - 1] = self.brightnessAux[self.fi - 1]
        return True
      
      pixels[self.l + self.fi] = focusColor
      pixels[self.l + self.fi - 1] = self.aux[self.fi - 1]
      brightnesses[self.l + self.fi - 1] = self.brightnessAux[self.fi - 1]
      self.fi += 1
      return False

    def _advance_left(self, brightnesses, pixels, focusColor):
      self.aux[self.li - self.l + self.ri - self.m] = self.lColor
      self.brightnessAux[self.li - self.l + self.ri - self.m] = brightnesses[self.li]
      pixels[self.li] = self.lColor
      self.li += 1
      if self.li < self.m:
        pixels[self.li], self.lColor = focusColor, pixels[self.li]

    def _advance_right(self, brightnesses, pixels, focusColor):
      self.aux[self.li - self.l + self.ri - self.m] = self.rColor
      self.brightnessAux[self.li - self.l + self.ri - self.m] = brightnesses[self.ri]
      pixels[self.ri] = self.rColor
      self.ri += 1
      if self.ri < self.r:
        pixels[self.ri], self.rColor = focusColor, pixels[self.ri]

  def __init__(self, pixels, *, 
               fps: Optional[int] = 60, 
               hue: int = 170, 
               brightnessRange: Collection[int] = (0, 255), 
               focusColor: Collection[int] = (255, 0, 0), 
               finishColor: Collection[int] = (255, 255, 255), 
               parallel: bool = False,
               finishWaitTime: float = 3):
    super().__init__(pixels, fps)
    self.hue = hue
    self.brightnessRange = brightnessRange
    self.focusColor = focusColor
    self.finishColor = finishColor
    self.parallel = parallel
    self.finishFrames = int(self.fps * finishWaitTime) if self.fps is not None else 60 * finishWaitTime
    self.t = 0
    self.sortedColors = [(hue / 255, 1.0, b) for b in np.linspace(brightnessRange[0] / 255, brightnessRange[1] / 255, len(self.pixels))]
    if self.parallel:
      self.renderNextFrame = self.renderParallel
    else:
      self.mergerIdx = 0
      self.renderNextFrame = self.renderSequential
    self.reset()

  def reset(self):
    self.phase = "merge"
    self.mergers: Collection[MergeSort.Merger] = [MergeSort.Merger(l, l+1, l+2) for l in range(0, len(self.pixels), 2)]
    random.shuffle(self.sortedColors)
    self.pixels[:] = [tuple(hsv_to_rgb(*hsv)) for hsv in self.sortedColors]
    self.brightnesses = [hsv[2] for hsv in self.sortedColors]
    
  def renderParallel(self):
    if self.phase == "merge":
      finished = True
      for merger in self.mergers:
        finished &= merger.step(self.brightnesses, self.pixels, self.focusColor)
      if finished:
        self.phase = "present"
    elif self.phase == "present":
      finished = True
      for merger in self.mergers:
        finished &= merger.finish(self.brightnesses, self.pixels, self.finishColor)
      if finished:
        if self._generate_next_mergers():
          self.t = 0
          self.phase = "finished"
        else:
          self.phase = "merge"
    elif self.phase == "finished":
      self.t += 1
      if self.t >= self.finishFrames:
        self.reset()

  def renderSequential(self):
    if self.phase == "merge":
      if self.mergers[self.mergerIdx].step(self.brightnesses, self.pixels, self.focusColor):
        self.phase = "present"
    elif self.phase == "present":
      if self.mergers[self.mergerIdx].finish(self.brightnesses, self.pixels, self.finishColor):
        self.mergerIdx += 1
        self.phase = "merge"
      if self.mergerIdx >= len(self.mergers):
        self.mergerIdx = 0
        if self._generate_next_mergers():
          self.t = 0
          self.phase = "finished"
        else:
          self.phase = "merge"
    elif self.phase == "finished":
      self.t += 1
      if self.t >= self.finishFrames:
        self.reset()

  def _generate_next_mergers(self):
    if len(self.mergers) == 1:
      return True
    newMergers = [MergeSort.Merger.fromMergers(self.mergers[i], self.mergers[i+1]) for i in range(0, len(self.mergers) // 2 * 2, 2)]
    if len(self.mergers) % 2 != 0:
      newMergers.append(self.mergers[-1])
    self.mergers = newMergers
    return False

  @classmethod
  def validate_parameters(cls, parameters):
    super().validate_parameters(parameters)
    full_parameters = {**cls.get_default_parameters(), **parameters}
    hue = full_parameters['hue']
    brightnessRange = full_parameters['brightnessRange']
    focusColor = full_parameters['focusColor']
    finishColor = full_parameters['finishColor']
    # no need to validate parallel since it's already confirmed a boolean
    finishWaitTime = full_parameters['finishWaitTime']

    if hue < 0 or hue > 255:
      raise TypeError("hue must be a value in [0, 255]")
    if not is_valid_inclusive_range(brightnessRange, 0, 255):
      raise TypeError("brightnessRange must be a valid range tuple")
    if not is_valid_rgb_color(focusColor):
      raise TypeError("focusColor must be a valid rgb color")
    if not is_valid_rgb_color(finishColor):
      raise TypeError("finishColor must be a valid rgb color")
    if not (0 <= finishWaitTime <= 10):
      raise TypeError("finishWaitTime must be in [0, 10]")
