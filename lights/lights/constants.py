try:
  import neopixel
  import board
  PIN = board.D18
  ORDER = neopixel.RGB
except NotImplementedError:
  PIN = None
  ORDER = "RGB"

NUM_PIXELS = 500