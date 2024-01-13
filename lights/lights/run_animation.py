import sys
import os
import argparse
import json
import threading
import signal
from lights.constants import NUM_PIXELS

# Animation imports.
from lights.animations import NAME_TO_ANIMATION
from lights.animations.base import BaseAnimation

# Controller imports.
from lights.controller import NAME_TO_CONTROLLER

# Starts running the animation in a separate thread. Note you must call stop() before attempting to join() to avoid hanging.
class ThreadedAnimationRunner(threading.Thread):
  def __init__(self, animation_name: str, controller_name: str, parameters: str) -> None:
    super().__init__()
    self.ar = AnimationRunner(animation_name, controller_name, parameters)

  def run(self) -> None:
    self.ar.run()

  def stop(self):
    self.ar.stop()


class AnimationRunner():
  def __init__(self, animation_name: str, controller_name: str, parameters: str) -> None:
    self.animation_class = NAME_TO_ANIMATION[animation_name]
    self.controller_class = NAME_TO_CONTROLLER[controller_name]
    kwargs = json.loads(parameters)

    self.c = self.controller_class(animation_name, kwargs, NUM_PIXELS)

  def run(self):
    self.c.run()

  def stop(self):
    self.c.stop()


def print_example_usage(animation_name: str, controller_name : str):
  animation = NAME_TO_ANIMATION[animation_name]
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
  
  if args.i:
    print_example_usage(args.animation_name, args.controller_name)
    exit(-1)
  
  try:
    ar = AnimationRunner(args.animation_name, args.controller_name, args.args)
  except Exception as e:
    print_example_usage(args.animation_name, args.controller_name)
    raise e

  def _handle_sigterm(*args):
    ar.stop()

  def _handle_sigint(*args):
    ar.stop()

  signal.signal(signal.SIGTERM, _handle_sigterm)
  signal.signal(signal.SIGINT, _handle_sigint)
  ar.run()