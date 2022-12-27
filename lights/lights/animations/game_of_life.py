from lights.animations.base import BaseAnimation
import copy

class GameOfLife(BaseAnimation):
  def __init__(self, pixels, *, fps=None, color=(0, 255, 0)):
    super().__init__(pixels, fps=fps)
    self.state = [True, True] + [False for _ in range(len(self.pixels) - 2)]
    self.color = color

  def renderNextFrame(self):
    NUM_PIXELS = len(self.pixels)
    # update state 
    newState = copy.copy(self.state)
    for i in range(len(self.state)):
      curr = self.state[i]
      prev = self.state[(i - 1) % NUM_PIXELS]
      next = self.state[(i + 1) % NUM_PIXELS]
      if curr and prev and next:
        newState[i] = False
      elif curr and not (prev or next):
        newState[i] = False
      elif not curr and (prev ^ next):
        newState[i] = True

      if newState[i]:
        self.pixels[i] = self.color
      else:
        self.pixels[i] = (0, 0, 0)
    self.state = newState
