import signal
import time
import json
from typing import get_type_hints, Optional
from typeguard import check_type

class BaseAnimation():
  def __init__(self, pixels, fps: Optional[int] = None):
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
    type_hints = get_type_hints(cls.__init__)

    for param, value in parameters.items():
      if param not in default_parameters:
        raise TypeError("Unknown parameter for animation {}: {}".format(cls.__name__, param))

      t = type_hints.get(param, type(default_parameters[param]))
      
      check_type(param, value, t)
      
  @classmethod
  def serialize_parameters(cls, parameters):
    return {k: json.dumps(v) for k, v in parameters.items()}

  @classmethod
  def deserialize_parameters(cls, parameters):
    return {k: json.loads(v) for k, v in parameters.items()}

  @classmethod
  def exampleUsage(cls):
    return "{} --args '{}'".format(cls.__name__, json.dumps(cls.get_default_parameters()))

  def _handle_sigterm(self, *args):
    self.shutdown()
    self.running = False

  def _handle_sigint(self, *args):
    self.shutdown()
    self.running = False
