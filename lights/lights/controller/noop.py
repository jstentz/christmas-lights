from numpy import ndarray
from lights.controller.base import BaseController

class NoopController(BaseController):

  # The noop controller does nothing when asked to display.
  def display(self, frame: ndarray):
    pass