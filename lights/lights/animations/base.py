import json
from typing import get_type_hints, Optional
from typeguard import check_type

import numpy as np

class BaseAnimation():
  def __init__(self, frameBuf: np.ndarray, fps: Optional[int] = None):
    self.frameBuf = frameBuf
    self.fps = fps
    self.period = 1/fps if fps is not None else 0

  def shutdown(self):
    pass

  def renderNextFrame(self):
    pass

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
      
      check_type(value, t)

    full_parameters = {**default_parameters, **parameters}
    if full_parameters['fps'] is not None and full_parameters['fps'] <= 0:
      raise TypeError("fps must be either None or a positive integer")
      
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
