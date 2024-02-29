import sys
import os
import argparse
import json
import threading
import signal
from lights.constants import NUM_PIXELS
from typing import Type
import importlib.util
from inspect import isclass

# Animation imports.
from lights.animations import NAME_TO_ANIMATION, BaseAnimation

# Controller imports.
from lights.controller import NAME_TO_CONTROLLER, BaseController

# Starts running the animation in a separate thread. Note you must call stop() before attempting to join() to avoid hanging.
class ThreadedAnimationRunner(threading.Thread):
  def __init__(self, animation_class: Type[BaseAnimation], controller_class: Type[BaseController], parameters: str) -> None:
    super().__init__()
    self.ar = AnimationRunner(animation_class, controller_class, parameters)
  
  @classmethod
  def from_names(cls, animation_name: str, controller_name: str, parameters: str):
    if animation_name not in NAME_TO_ANIMATION:
      raise ValueError(f"Animation '{animation_name}' was not found in the animations folder.")
    if controller_name not in NAME_TO_CONTROLLER:
      raise ValueError(f"Controller '{controller_name}' was not found in the controller folder.")
    animation_class = NAME_TO_ANIMATION[animation_name]()
    controller_class = NAME_TO_CONTROLLER[controller_name]()
    return cls(animation_class, controller_class, parameters)

  def run(self) -> None:
    self.ar.run()

  def stop(self):
    self.ar.stop()


class AnimationRunner():
  def __init__(self, animation_class: Type[BaseAnimation], controller_class: Type[BaseController], parameters: str, validate_parameters=True) -> None:
    self.animation_class = animation_class
    self.controller_class = controller_class
    kwargs = json.loads(parameters)

    self.c = self.controller_class(self.animation_class, kwargs, NUM_PIXELS, validate_parameters=validate_parameters)

  def run(self):
    self.c.run()

  def stop(self):
    self.c.stop()


def print_example_usage(animation_name: str, controller_name: str):
  animation = NAME_TO_ANIMATION[animation_name]()
  print("Example usage:")
  print("python", os.path.basename(__file__), '-c', controller_name, '-a', animation.exampleUsage())

def load_animation_from_file(path: str) -> Type[BaseAnimation]:
  modname = os.path.splitext(os.path.basename(path))[0]
  spec = importlib.util.spec_from_file_location(modname, path)
  if spec is None:
    raise ValueError(f'Could not import {path}')
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  for attribute_name in dir(module):
    attribute = getattr(module, attribute_name)
    if isclass(attribute) and issubclass(attribute, BaseAnimation) and attribute is not BaseAnimation:            
      return attribute
  return None

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog="run_animation", 
                                   description="Script for running animations, either on a simulator or actual hardware")
  parser.add_argument('-a', '--animation_name',
                      help='the class name of the animation', 
                      type=str,
                      required='-l' not in sys.argv and '--file' not in sys.argv)
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
  parser.add_argument('--no_validation',
                      help='skips validating the supplied args list against the selected animation',
                      action='store_true')
  parser.add_argument('--file',
                      help='runs an animation from a file',
                      type=str)
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
    if args.animation_name:
      animation_class = NAME_TO_ANIMATION[args.animation_name]()
    else:
      animation_class = load_animation_from_file(args.file)
    controller_class = NAME_TO_CONTROLLER[args.controller_name]()
    print(animation_class, controller_class)
    ar = AnimationRunner(animation_class, controller_class, args.args, validate_parameters=not args.no_validation)
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