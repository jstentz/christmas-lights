import numpy as np
from lights.controller.base import BaseController
import serial
import threading

class SerialController(BaseController):
  def __init__(self, animation, animation_kwargs, n_pixels: int, port='/dev/ttyACM0'):
    super().__init__(animation, animation_kwargs, n_pixels)
    self.usb_serial = serial.Serial(port)
    self.display_buffer = None
    self.transmit_thread: threading.Thread = None

  def display(self, frame: np.ndarray):
    self._transmit(frame.astype(np.uint8).tobytes())

  def _transmit(self, buffer: bytes):
    if self.transmit_thread is not None:
      self.transmit_thread.join()
    self.display_buffer = buffer
    self.transmit_thread = threading.Thread(target=self._send_data)
    self.transmit_thread.start()

  def _send_data(self):
    self.usb_serial.write(self.display_buffer)
    self.usb_serial.flush()
