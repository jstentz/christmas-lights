from lights.animations.base import BaseAnimation

class DownTheLine(BaseAnimation):
  def __init__(self, pixels, rate=1, decay=0.9, fps=None):
    super().__init__(pixels, fps=fps)
    self.rate = rate
    self.decay = decay
    self.t = 0
    
  def renderNextFrame(self):
    NUM_PIXELS = len(self.pixels)
    t = self.t
    rate = self.rate
    decay = self.decay
    for i in range(rate):
      index = t % NUM_PIXELS - (i * NUM_PIXELS // rate)
      self.pixels[index] = color
    for i in range(NUM_PIXELS):
      color = self.pixels[i]
      self.pixels[i] = tuple(int(c * decay) for c in color)
    self.t += 1