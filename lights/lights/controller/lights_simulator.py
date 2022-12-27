import adafruit_pixelbuf
import cursor
from sty import bg
import os

class LightsSimulator(adafruit_pixelbuf.PixelBuf):
  def __init__(self, pin, n: int, *, bpp: int = 3, brightness: float = 1.0, auto_write: bool = True, pixel_order: str = None):
    super().__init__(
      n, brightness=brightness, byteorder=pixel_order, auto_write=auto_write
    )
    self.tcols, self.trows = os.get_terminal_size()
    os.system('cls||clear')
    cursor.hide()    

  def show(self):
    num_rows_last_print = (self._pixels + self.tcols - 1) // self.tcols
    print("\033[F" * num_rows_last_print, end="", flush=True)
    buf = list(self._post_brightness_buffer)
    s = ""
    for pixel in self:
      r, g, b = pixel[self._byteorder[0]], pixel[self._byteorder[1]], pixel[self._byteorder[2]]
      s += bg(r, g, b) + " " + bg.rs 

    print(s, end='', flush=True)
    self.tcols, self.trows = os.get_terminal_size()

  # Make _transmit a noop during simulation.
  def _transmit(self, buffer: bytearray):
    pass

  def __del__(self):
    cursor.show()