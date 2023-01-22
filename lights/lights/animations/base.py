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
    # Render first frame immediately. This ensures snappy transitions between animations
    # using different frame rates.
    self.renderNextFrame()
    self.pixels.show()

    while self.running:
      start = time.time()
      self.renderNextFrame()
      end = time.time()
      wait = max(0, self.period - (end - start))
      time.sleep(wait)
      # push frame to lights.
      self.pixels.show()
    
    self.pixels.fill((0, 0, 0))

  @classmethod 
  def get_default_parameters(cls):
    return cls.__init__.__kwdefaults__

  @classmethod
  def validate_parameters(cls, parameters):
    default_parameters = cls.get_default_parameters()
    for param, value in parameters.items():
      if param not in default_parameters:
        raise ValueError("Unknown parameter for animation {}: {}".format(cls.__name__, param))
      
      # if not isinstance(value, type(default_parameters[param])):
      #   raise ValueError("Mismatched parameter type for animation {}. Expecting type {}, got {}.".format(cls.__name__, type(default_parameters), type(value)))

  @classmethod
  def exampleUsage(cls):
    kwargs_str = ["{}={}".format(arg, value) for arg, value in cls.get_default_parameters().items()]
    return "{} {}".format(cls.__name__, " ".join(kwargs_str))

  def _handle_sigterm(self, *args):
    self.shutdown()
    self.running = False

  def _handle_sigint(self, *args):
    self.shutdown()
    self.running = False
