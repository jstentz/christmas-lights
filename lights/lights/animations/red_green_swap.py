from lights.animations.base import BaseAnimation

class RedGreenSwap(BaseAnimation):
  def __init__(self, pixels, *, fps=1):
    super().__init__(pixels, fps=fps)
    self.t = 0

  def renderNextFrame(self):
    for i in range(len(self.pixels)):
      if self.t % 2 == 0:
        if i % 2 == 0:
          self.pixels[i] = (255, 0, 0)
        else:
          self.pixels[i] = (0, 255, 0)
      else:
        if i % 2 != 0:
          self.pixels[i] = (255, 0, 0)
        else:
          self.pixels[i] = (0, 255, 0)
    self.t += 1
