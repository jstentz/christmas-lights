import signal

class BaseAnimation():
  def __init__(self, pixels):
    self.pixels = pixels
    signal.signal(signal.SIGTERM, self._handle_sigterm)
    signal.signal(signal.SIGINT, self._handle_sigint)

  def shutdown(self):
    pass

  def renderFrame(self, t):
    pass

  def run(self):
    pass

  def _handle_sigterm(self, *args):
    self.shutdown()
    exit(0)

  def _handle_sigint(self, *args):
    self.shutdown()
    exit(0)

if __name__ == '__main__':
  import time
  snake = Snake(None, None)
  snake.run()