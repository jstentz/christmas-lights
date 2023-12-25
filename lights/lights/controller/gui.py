from numpy import ndarray
from lights.controller.base import BaseController
import math
import signal
import time
import tkinter

from multiprocessing import Process, Queue

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

class GuiController(BaseController):
  def __init__(self, n_pixels):
    super().__init__(n_pixels)
    self.pixelQueue = Queue()
    self.guiProcess = Process(target=TkLightsGui.new, args=(self.pixelQueue, ))
    self.guiProcess.start()

  def display(self, frame: ndarray):
    if not self.guiProcess.is_alive():
      signal.raise_signal(signal.SIGINT)

    self.pixelQueue.put(frame.tolist())
    time.sleep(0.02)
    
  def shutdown(self):
    self.guiProcess.terminate()