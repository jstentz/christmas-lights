from numpy import ndarray
from lights.controller.base import BaseController
import cursor
import os

from sty import bg
import numpy as np

class TerminalController(BaseController):
  def __init__(self, n_pixels):
    super().__init__(n_pixels)
    self.bg = np.vectorize(bg)
    self.tcols, _ = os.get_terminal_size()
    os.system('cls||clear')
    cursor.hide()    
  
  def display(self, frame: ndarray):
    self.tcols, _ = os.get_terminal_size()
    num_rows_last_print = self.n_pixels // self.tcols

    s = self.bg(frame[:, 0], frame[:, 1], frame[:, 2])

    # Push frame.
    print("\033[F" * num_rows_last_print, end="")
    print(' '.join(s), end='', flush=True)
  
  def shutdown(self):
    os.system('tput init')
    cursor.show()
