import numpy as np
from lights.animations import NAME_TO_ANIMATION
from typing import Dict
import signal
import numpy as np
import time

# A controller is responsible for pushing frames to display, whether that display be a terminal, gui, or leds.
class BaseController:
  
  def __init__(self, animation: str, animation_kwargs: Dict, n_pixels: int):
    self.n_pixels = n_pixels
    if animation not in NAME_TO_ANIMATION:
      raise TypeError(f"Animation {animation} not found.")
    self.animation_class = NAME_TO_ANIMATION[animation]
    self.animation_class.validate_parameters(animation_kwargs)
    self.frameBuf = np.zeros((n_pixels, 3), dtype='float')
    self.animation = self.animation_class(self.frameBuf, **animation_kwargs)
    self.running = False
    signal.signal(signal.SIGTERM, self._handle_sigterm)
    signal.signal(signal.SIGINT, self._handle_sigint)

  def run(self):
    # Render first frame immediately. This ensures snappy transitions between animations
    # using different frame rates.
    self.running = True
    self.animation.renderNextFrame()
    self.display(self.frameBuf)

    while self.running:
      start = time.time()
      self.animation.renderNextFrame()
      end = time.time()
      wait = max(0, self.animation.period - (end - start))
      time.sleep(wait)
      # push frame to lights.
      self.display(self.frameBuf)
    
    self.frameBuf[:] = 0
    self.display(self.frameBuf)
    self.shutdown()

  def display(self, frame: np.ndarray):
    pass

  def shutdown(self):
    pass

  def _handle_sigterm(self, *args):
    self.animation.shutdown()
    self.running = False

  def _handle_sigint(self, *args):
    self.animation.shutdown()
    self.running = False