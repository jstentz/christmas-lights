import serial
import adafruit_pixelbuf
import threading

class SerialPixels(adafruit_pixelbuf.PixelBuf):
  def __init__(self, pin, n: int, *, bpp: int = 3, brightness: float = 1.0, auto_write: bool = True, pixel_order: str = None, port='/dev/ttyACM0'):
    super().__init__(
      n, brightness=brightness, byteorder=pixel_order, auto_write=auto_write
    )
    self.num_leds = n
    self.usb_serial = serial.Serial(port)
    self.display_buffer = None
    self.transmit_thread: threading.Thread = None

  def _transmit(self, buffer: bytearray):
    if self.transmit_thread is not None:
      self.transmit_thread.join()
    self.display_buffer = buffer.copy()
    self.transmit_thread = threading.Thread(target=self._send_data)
    self.transmit_thread.start()

  def _send_data(self):
    # print(len(self.display_buffer))
    self.usb_serial.write(self.display_buffer)
    self.usb_serial.flush()
