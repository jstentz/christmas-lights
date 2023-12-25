from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from lights.animations.base import BaseAnimation
from typing import Dict, List, Type

ANIMATIONS: List[Type[BaseAnimation]] = []

# adapted from https://julienharbulot.com/python-dynamical-import.html
# iterate through the modules in the current package
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([str(package_dir)]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute) and issubclass(attribute, BaseAnimation):            
            # Add the class to this package's variables
            ANIMATIONS.append(attribute)

NAME_TO_ANIMATION: Dict[str, Type[BaseAnimation]] = {animation.__name__: animation for animation in ANIMATIONS}