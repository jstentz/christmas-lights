import adafruit_pixelbuf
import cursor
import math
import os
import signal
import time
try:
  import tkinter
except ImportError:
  pass

from multiprocessing import Process, Queue
from sty import bg

class BaseLightsSimulator(adafruit_pixelbuf.PixelBuf):
  # Make _transmit a noop during simulation.
  def _transmit(self, buffer: bytearray):
    pass

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

class TkLightsGui():
  @staticmethod
  def new(pixelQueue):
    TkLightsGui(pixelQueue).run()

  def __init__(self, pixelQueue):
    self.pixelQueue = pixelQueue
    self.width = self.height = 400

  def run(self):
    root = tkinter.Tk()
    canvas = tkinter.Canvas(root, width=self.width, height=self.height)
    canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    self.step(canvas)
    root.mainloop()

  @staticmethod
  def rgbToHex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

  def draw(self, canvas, pixels):
    rows = cols = math.ceil(math.sqrt(len(pixels)))
    cellWidth, cellHeight = self.width / cols, self.height / rows
    for row in range(rows):
      for col in range(cols):
        rowOffset = col if row % 2 == 0 else cols - col - 1
        index = row * cols + rowOffset
        rgb = pixels[index] if index < len(pixels) else (0, 0, 0)
        cx, cy = cellWidth * col + cellWidth / 2, cellHeight * row + cellHeight / 2
        r = min(cellWidth, cellHeight) / 2 * 0.8
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=self.rgbToHex(*rgb)) 

  def step(self, canvas):
    while not self.pixelQueue.empty():
      pixels = self.pixelQueue.get()
      canvas.delete(tkinter.ALL)
      canvas.create_rectangle(0, 0, self.width, self.height, fill='black', width=0)
      self.draw(canvas, pixels)
    canvas.after(10, self.step, canvas)

class TkLightsSimulator(BaseLightsSimulator):
  def __init__(self, pin, n: int, *, bpp: int = 3, brightness: float = 1.0, auto_write: bool = True, pixel_order: str = None):
    super().__init__(
      n, brightness=brightness, byteorder=pixel_order, auto_write=auto_write
    )
    self.pixelQueue = Queue()
    self.guiProcess = Process(target=TkLightsGui.new, args=(self.pixelQueue, ))
    self.guiProcess.start()

  def show(self):
    if not self.guiProcess.is_alive():
      signal.raise_signal(signal.SIGINT)

    pixels = []
    for pixel in self:
      r, g, b = pixel[self._byteorder[0]], pixel[self._byteorder[1]], pixel[self._byteorder[2]]
      pixels.append((r, g, b))
    self.pixelQueue.put(pixels)
    time.sleep(0.02)

    
  def __del__(self):
    self.guiProcess.terminate()