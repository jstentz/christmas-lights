from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from lights.controller.base import BaseController
from typing import Dict, List, Type

CONTROLLERS: List[Type[BaseController]] = []

# adapted from https://julienharbulot.com/python-dynamical-import.html
# iterate through the modules in the current package
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([str(package_dir)]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute) and issubclass(attribute, BaseController):            
            # Add the class to this package's variables
            CONTROLLERS.append(attribute)

NAME_TO_CONTROLLER: Dict[str, Type[BaseController]] = {animation.__name__: animation for animation in CONTROLLERS}