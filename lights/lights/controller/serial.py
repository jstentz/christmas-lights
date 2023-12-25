from numpy import ndarray
from lights.controller.base import BaseController
import serial
import threading

class SerialController(BaseController):
  def __init__(self, n_pixels, port='/dev/ttyACM0'):
    super().__init__(n_pixels)
    self.usb_serial = serial.Serial(port)
    self.display_buffer = None
    self.transmit_thread: threading.Thread = None

  def display(self, frame: ndarray):
    # assumes frame has dtype 'uint8'
    self._transmit(frame.tobytes())

  def _transmit(self, buffer: bytes):
    if self.transmit_thread is not None:
      self.transmit_thread.join()
    self.display_buffer = buffer
    self.transmit_thread = threading.Thread(target=self._send_data)
    self.transmit_thread.start()

  def _send_data(self):
    # print(len(self.display_buffer))
    self.usb_serial.write(self.display_buffer)
    self.usb_serial.flush()
