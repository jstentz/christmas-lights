from lights.controller.lights_simulator_base import BaseLightsSimulator
import cursor
import os

from sty import bg

class TerminalLightsSimulator(BaseLightsSimulator):
  def __init__(self, pin, n: int, *, bpp: int = 3, brightness: float = 1.0, auto_write: bool = True, pixel_order: str = None):
    super().__init__(
      n, brightness=brightness, byteorder=pixel_order, auto_write=auto_write
    )
    self.tcols, _ = os.get_terminal_size()
    os.system('cls||clear')
    cursor.hide()    

  def show(self):
    self.tcols, _ = os.get_terminal_size()
    num_rows_last_print = self._pixels // self.tcols
    s = ""
    for pixel in self:
      r, g, b = pixel[self._byteorder[0]], pixel[self._byteorder[1]], pixel[self._byteorder[2]]
      s += bg(r, g, b) + " " 

    # Push frame.
    print("\033[F" * num_rows_last_print, end="")
    print(s, end='', flush=True)

  def __del__(self):
    cursor.show()
