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
    self.pixels.fill((0, 0, 0))

  @classmethod
  def exampleUsage(cls):
    kwargs_str = ["{}={}".format(arg, value) for arg, value in cls.__init__.__kwdefaults__.items()]
    return "{} {}".format(cls.__name__, " ".join(kwargs_str))

  def _handle_sigterm(self, *args):
    self.shutdown()
    self.running = False

  def _handle_sigint(self, *args):
    self.shutdown()
    self.running = False
