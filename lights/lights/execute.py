from lights.animations import NAME_TO_ANIMATION
from lights.controller import NAME_TO_CONTROLLER
import numpy as np
import time
import signal
from typing import Dict

class Executor:

  def __init__(self, animation: str, controller: str, n_pixels: int, animation_kwargs: Dict):
    if animation not in NAME_TO_ANIMATION:
      raise TypeError(f"Animation {animation} not found.")
    self.animation_class = NAME_TO_ANIMATION[animation]
    if controller not in NAME_TO_CONTROLLER:
      raise TypeError(f"Controller {controller} not found.")
    self.controller_class = NAME_TO_CONTROLLER[controller]
    self.animation_class.validate_parameters(animation_kwargs)
    self.frameBuf = np.zeros((n_pixels, 3), dtype='uint8')
    self.animation = self.animation_class(self.frameBuf, **animation_kwargs)
    self.controller = self.controller_class(n_pixels)
    self.running = False
    signal.signal(signal.SIGTERM, self._handle_sigterm)
    signal.signal(signal.SIGINT, self._handle_sigint)

  def run(self):
    # Render first frame immediately. This ensures snappy transitions between animations
    # using different frame rates.
    self.running = True
    self.animation.renderNextFrame()
    self.controller.display(self.frameBuf)

    while self.running:
      start = time.time()
      self.animation.renderNextFrame()
      end = time.time()
      wait = max(0, self.animation.period - (end - start))
      time.sleep(wait)
      # push frame to lights.
      self.controller.display(self.frameBuf)
    
    self.frameBuf[:] = 0
    self.controller.display(self.frameBuf)
    self.controller.shutdown()
  
  def _handle_sigterm(self, *args):
    self.animation.shutdown()
    self.running = False

  def _handle_sigint(self, *args):
    self.animation.shutdown()
    self.running = False