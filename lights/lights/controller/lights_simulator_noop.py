from lights.controller.lights_simulator_base import BaseLightsSimulator


class NoopLightsSimulator(BaseLightsSimulator):
  def __init__(self, pin, n: int, *, bpp: int = 3, brightness: float = 1.0, auto_write: bool = True, pixel_order: str = None):
    super().__init__(
      n, brightness=brightness, byteorder=pixel_order, auto_write=auto_write
    )

  
  def show(self):
    pass
