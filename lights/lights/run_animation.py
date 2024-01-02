import sys
import os
import argparse
import json

# Animation imports.
from lights.animations import NAME_TO_ANIMATION
from lights.animations.base import BaseAnimation

# Controller imports.
from lights.controller import NAME_TO_CONTROLLER

def printExampleUsage(animation: BaseAnimation, controller_name : str):
  print("Example usage:")
  print("python", os.path.basename(__file__), '-c', controller_name, '-a', animation.exampleUsage())

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
                      default='MatplotlibController')
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
  controller = NAME_TO_CONTROLLER[args.controller_name]
  kwargs_start = 2

  if args.i:
    printExampleUsage(animation, args.controller_name)
    exit(-1)

  kwargs = json.loads(args.args)

  # Setup.
  try:
    c = controller(args.animation_name, kwargs, 500)
  except Exception as e:
    printExampleUsage(animation)
    raise e

  c.run()