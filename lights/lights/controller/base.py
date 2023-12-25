import numpy as np

# A controller is responsible for pushing frames to display, whether that display be a terminal, gui, or leds.
class BaseController:
  
  def __init__(self, n_pixels):
    self.n_pixels = n_pixels

  def display(self, frame: np.ndarray):
    pass

  def shutdown(self):
    pass