from pathlib import Path
from importlib import import_module
from lights.controller.base import BaseController
from typing import Dict, Callable
import os
import ast

def get_lazy_loaders() -> Dict[str, Callable[[], BaseController]]:
  name_to_lazy_loader = {}
  module_path = Path(__file__).resolve().parent
  package_name = __name__
  for file_name in os.listdir(module_path):
    if file_name.endswith('.py'):
      with open(os.path.join(module_path, file_name), 'r') as file:
        tree = ast.parse(file.read(), filename=file_name)
      module_name = os.path.splitext(file_name)[0]

      for node in tree.body:
        if isinstance(node, ast.ClassDef):
          for base in node.bases:
            if isinstance(base, ast.Name) and base.id == BaseController.__name__:
              loader = lambda module_name=module_name, node=node: getattr(import_module(package_name + '.' + module_name), node.name)
              name_to_lazy_loader[node.name] = loader
              break
  return name_to_lazy_loader

NAME_TO_CONTROLLER = get_lazy_loaders()
CONTROLLERS = list(NAME_TO_CONTROLLER.keys())