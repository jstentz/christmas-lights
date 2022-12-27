import ast
import sys
import os
import argparse

# Animation imports.
from lights.animations import NAME_TO_ANIMATION
from lights.animations.base import BaseAnimation

def printExampleUsage(animation: BaseAnimation):
  print("Example usage: python", os.path.basename(__file__), animation.exampleUsage())

def parseExtraArgs(args):
  return {k: ast.literal_eval(v) for arg in args for k, v in [arg.split('=')]}

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog="run_animation", 
                                   description="Script for running animations, either on a simulator or actual hardware")
  parser.add_argument('-a', '--animation_name',
                      help='the class name of the animation', 
                      type=str,
                      required='-l' not in sys.argv)
  parser.add_argument('-r', 
                      help='run on hardware', 
                      action='store_true')
  parser.add_argument('-i', 
                      help='show example usage for the selected animation', 
                      action='store_true')
  parser.add_argument('-l',
                      help='list all available animations',
                      action='store_true')
  parser.add_argument('--args', 
                      help='custom arguments for the selected animation', 
                      nargs=argparse.REMAINDER, 
                      type=str, 
                      default=[])
  args = parser.parse_args()

  # Parse command line arguments.

  if args.l:
    print('Available animations:\n', "\n".join(NAME_TO_ANIMATION.keys()))
    exit(0)

  animation = NAME_TO_ANIMATION[args.animation_name]
  kwargs_start = 2

  if args.i:
    printExampleUsage(animation)
    exit(-1)
  
  kwargs = parseExtraArgs(args.args)

  # Setup.
  if args.r:
    from neopixel import NeoPixel as LightsController
    from lights.constants import PIN, NUM_PIXELS, ORDER
  else:
    PIN, NUM_PIXELS, ORDER = 0, 500, "RGB"
    from lights.controller.lights_simulator import LightsSimulator
    LightsController = LightsSimulator

  # Run animation.
  pixels = LightsController(PIN, NUM_PIXELS, auto_write=False, pixel_order=ORDER)
  
  try:
    a = animation(pixels, **kwargs)
  except Exception as e:
    printExampleUsage(animation)
    raise e

  a.run()