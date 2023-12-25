import sys
import os
import argparse
import json

from lights.execute import Executor

# Animation imports.
from lights.animations import NAME_TO_ANIMATION
from lights.animations.base import BaseAnimation

# Controller imports.
from lights.controller import NAME_TO_CONTROLLER

def printExampleUsage(animation: BaseAnimation):
  print("Example usage:")
  print("python", os.path.basename(__file__), '-a', animation.exampleUsage())

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog="run_animation", 
                                   description="Script for running animations, either on a simulator or actual hardware")
  parser.add_argument('-a', '--animation_name',
                      help='the class name of the animation', 
                      type=str,
                      required='-l' not in sys.argv)
  parser.add_argument('-c', '--controller_name', 
                      help='the class name of the controller', 
                      type=str,
                      default='TerminalController')
  parser.add_argument('-i', 
                      help='show example usage for the selected animation', 
                      action='store_true')
  parser.add_argument('-l',
                      help='list all available animations and controllers',
                      action='store_true')
  parser.add_argument('--args', 
                      help='custom arguments for the selected animation',
                      type=str, 
                      default="{}")
  args = parser.parse_args()

  # Parse command line arguments.

  if args.l:
    print('Available controllers:\n', "\n".join(NAME_TO_CONTROLLER.keys()), sep='')
    print('\nAvailable animations:\n', "\n".join(NAME_TO_ANIMATION.keys()), sep='')
    exit(0)

  animation = NAME_TO_ANIMATION[args.animation_name]
  kwargs_start = 2

  if args.i:
    printExampleUsage(animation)
    exit(-1)

  kwargs = json.loads(args.args)

  # # Setup.
  # if args.r:
  #   #from neopixel import NeoPixel as LightsController
  #   from lights.controller.serial_pixels import SerialPixels as LightsController
  #   from lights.constants import PIN, NUM_PIXELS, ORDER
  # else:
  #   PIN, NUM_PIXELS, ORDER = 0, 500, "RGB"
  #   if args.g:
  #     from lights.controller.lights_simulator_tkinter import TkLightsSimulator
  #     LightsController = TkLightsSimulator
  #   elif args.n:
  #     from lights.controller.lights_simulator_noop import NoopLightsSimulator
  #     LightsController = NoopLightsSimulator
  #   else: # default, simulate in the terminal
  #     from lights.controller.lights_simulator_terminal import TerminalLightsSimulator
  #     LightsController = TerminalLightsSimulator


  # Run animation.
  # pixels = LightsController(PIN, NUM_PIXELS, auto_write=False, pixel_order=ORDER)
  
  try:
    executor = Executor(args.animation_name, args.controller_name, 500, kwargs)
  except Exception as e:
    # printExampleUsage(animation)
    raise e

  executor.run()