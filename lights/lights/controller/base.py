import numpy as np
from lights.animations import BaseAnimation
from typing import Dict, Type
import numpy as np
import time

# A controller is responsible for pushing frames to display, whether that display be a terminal, gui, or leds.
class BaseController:
  
  def __init__(self, animation: Type[BaseAnimation], animation_kwargs: Dict, n_pixels: int):
    self.n_pixels = n_pixels
    self.animation_class = animation
    self.animation_class.validate_parameters(animation_kwargs)
    self.frameBuf = np.zeros((n_pixels, 3), dtype='float')
    self.animation = self.animation_class(self.frameBuf, **animation_kwargs)
    self.exited = False

  def run(self):
    # Render first frame immediately. This ensures snappy transitions between animations
    # using different frame rates.
    self.animation.renderNextFrame()
    self.display(self.frameBuf)

    while not self.exited:
      start = time.time()
      self.animation.renderNextFrame()
      end = time.time()
      wait = max(0, self.animation.period - (end - start))
      time.sleep(wait)
      # push frame to lights.
      self.display(self.frameBuf)
    
    self.frameBuf[:] = 0
    self.display(self.frameBuf)
    self.animation.shutdown()
    self.shutdown()

  def stop(self):
    self.exited = True

  def display(self, frame: np.ndarray):
    pass

  def shutdown(self):
    pass