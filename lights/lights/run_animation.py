from lights.animations.snake import Snake
from lights.animations.snowflakes import Snowflakes
from lights.animations.base import BaseAnimation

import sys
from typing import Dict

def init_lights():
  try:
    from lights.lights_util import Lights
    from lights.constants import PIN, NUM_PIXELS, ORDER
    return Lights(PIN, NUM_PIXELS, auto_write=False, pixel_order=ORDER)
  except NotImplementedError:
    from unittest.mock import MagicMock
    PIN, NUM_PIXELS, ORDER = 0, 500, 0
    lights = MagicMock()
    lights.__len__.return_value = NUM_PIXELS
    return lights

ANIMATIONS: BaseAnimation = [Snake, Snowflakes]

NAME_TO_ANIMATION: Dict[str, BaseAnimation] = {animation.__name__: animation for animation in ANIMATIONS}

# Parse command line arguments.
animation_name = sys.argv[1]
kwargs = dict(arg.split('=') for arg in sys.argv[2:])

# Run animation.
pixels = init_lights()
animation = NAME_TO_ANIMATION[animation_name]
a = animation(pixels, **kwargs)
a.run()