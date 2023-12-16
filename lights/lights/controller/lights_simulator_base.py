import adafruit_pixelbuf

class BaseLightsSimulator(adafruit_pixelbuf.PixelBuf):
  # Make _transmit a noop during simulation.
  def _transmit(self, buffer: bytearray):
    pass
