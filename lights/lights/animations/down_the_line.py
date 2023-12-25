from lights.animations.base import BaseAnimation
from lights.utils.colors import randomColor
from typing import Optional

class DownTheLine(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = None, rate: int = 10, decay: float = 0.9):
    super().__init__(frameBuf, fps=fps)
    self.rate = rate
    self.decay = decay
    self.t = 0
    self.color = randomColor()
    
  def renderNextFrame(self):
    NUM_PIXELS = len(self.frameBuf)
    t = self.t
    rate = self.rate
    decay = self.decay

    if t % NUM_PIXELS == 0:
      self.color = randomColor()

    for i in range(rate):
      index = t % NUM_PIXELS - (i * NUM_PIXELS // rate)
      self.frameBuf[index] = self.color
    for i in range(NUM_PIXELS):
      color = self.frameBuf[i]
      self.frameBuf[i] = tuple(int(c * decay) for c in color)
    self.t += 1

  @classmethod
  def validate_parameters(cls, parameters):
    super().validate_parameters(parameters)
    full_parameters = {**cls.get_default_parameters(), **parameters}
    rate = full_parameters['rate']
    decay = full_parameters['decay']

    if rate <= 0:
      raise TypeError("rate must be > 0")
    if decay < 0 or decay >= 1:
      raise TypeError("decay must be between [0, 1)")
