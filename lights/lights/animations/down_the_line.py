from lights.animations.base import BaseAnimation
from lights.utils.colors import randomColor

class DownTheLine(BaseAnimation):
  def __init__(self, pixels, *, rate=1, decay=0.9, fps=None):
    super().__init__(pixels, fps=fps)
    self.rate = rate
    self.decay = decay
    self.t = 0
    self.color = randomColor()
    
  def renderNextFrame(self):
    NUM_PIXELS = len(self.pixels)
    t = self.t
    rate = self.rate
    decay = self.decay

    if t % NUM_PIXELS == 0:
      self.color = randomColor()

    for i in range(rate):
      index = t % NUM_PIXELS - (i * NUM_PIXELS // rate)
      self.pixels[index] = self.color
    for i in range(NUM_PIXELS):
      color = self.pixels[i]
      self.pixels[i] = tuple(int(c * decay) for c in color)
    self.t += 1