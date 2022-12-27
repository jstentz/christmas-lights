import signal
import time

class BaseAnimation():
  def __init__(self, pixels, fps=None):
    self.pixels = pixels
    self.fps = fps
    self.period = 1/fps if fps is not None else 0
    self.running = True
    signal.signal(signal.SIGTERM, self._handle_sigterm)
    signal.signal(signal.SIGINT, self._handle_sigint)

  def shutdown(self):
    pass

  def renderNextFrame(self):
    pass

  def run(self):
    while self.running:
      start = time.time()
      self.renderNextFrame()
      # push frame to lights.
      self.pixels.show()
      end = time.time()
      wait = max(0, self.period - (end - start))
      time.sleep(wait)
    self.pixels.clear()

  def _handle_sigterm(self, *args):
    print("Got SIGTERM, shutting down...")
    self.shutdown()
    self.running = False

  def _handle_sigint(self, *args):
    print("Got SIGINT, shutting down...")
    self.shutdown()
    self.running = False