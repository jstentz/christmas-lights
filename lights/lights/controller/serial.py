import numpy as np
from lights.controller.base import BaseController
import serial
import threading

class SerialController(BaseController):
  def __init__(self, animation, animation_kwargs, n_pixels: int, validate_parameters=True, port='/dev/ttyACM0'):
    super().__init__(animation, animation_kwargs, n_pixels, validate_parameters=validate_parameters)
    self.usb_serial = serial.Serial(port)
    self.display_buffer = None
    self.transmit_thread: threading.Thread = None

  def display(self, frame: np.ndarray):
    self._transmit(frame.astype(np.uint8).tobytes())

  def shutdown(self):
    if self.transmit_thread is not None:
      self.transmit_thread.join()
    self.usb_serial.close()

  def _transmit(self, buffer: bytes):
    if self.transmit_thread is not None:
      self.transmit_thread.join()
    self.display_buffer = buffer
    self.transmit_thread = threading.Thread(target=self._send_data)
    self.transmit_thread.start()

  def _send_data(self):
    self.usb_serial.write(self.display_buffer)
    self.usb_serial.flush()
