from lights.animations.snake import Snake
from lights.animations.snowflakes import Snowflakes
from lights.animations.down_the_line import DownTheLine
from lights.animations.rainbow_sine import RainbowSine
from lights.animations.base import BaseAnimation
import ast

import sys
from typing import Dict

ANIMATIONS: BaseAnimation = [Snake, Snowflakes, DownTheLine, RainbowSine]
NAME_TO_ANIMATION: Dict[str, BaseAnimation] = {animation.__name__: animation for animation in ANIMATIONS}

SIMULATE = True
if not SIMULATE:
  from lights.controller.lights import Lights
  from lights.constants import PIN, NUM_PIXELS, ORDER
else:
  PIN, NUM_PIXELS, ORDER = 0, 500, "RGB"
  from lights.controller.lights_simulator import LightsSimulator
  Lights = LightsSimulator

# Parse command line arguments.
animation_name = sys.argv[1]
kwargs_list = [arg.split('=') for arg in sys.argv[2:]]
kwargs = dict([(arg[0], ast.literal_eval(arg[1]))for arg in kwargs_list])

# Run animation.
pixels = Lights(PIN, NUM_PIXELS, auto_write=False, pixel_order=ORDER)
animation = NAME_TO_ANIMATION[animation_name]
a = animation(pixels, **kwargs)
a.run()