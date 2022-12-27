# Lights

## Installation
At the root of the repository, create a virtual environment and install the requirements:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Still in the virtual environment, install the local change to the first `lights` folder and install the local `lights` package:
```
cd lights
pip install -e .
```

## Creating an animation

All animations live in their own file in the `animations` subdirectory. Here's the basic structure of an animation:
```
from lights.animations.base import BaseAnimation

class NewAnimation(BaseAnimation): # all animations inherit from BaseAnimation
  # Unpack custom argument and initialize state (if using) in the initializer.
  def __init__(pixels, *, fps=None, custom_arg1="default_value_1", custom_arg2="default_value_2"):
    super().__init__(pixels, fps=fps)
    self.custom_arg_1 = custom_arg_1
    self.custom_arg_2 = custom_arg_2
    self.state = {}

  # You can write the core logic of your animation in this function.
  # It's called at the specified frame rate (every 1/fps seconds).
  def renderNextFrame(self):
    # Set the first light to red. See below for more info about the self.pixels object.
    self.pixels[0] = (255, 0, 0) # RGB.

  # Perform any cleanup work here.
  def shutdown(self):
    pass
```

The `self.pixels` object is the actual interface to the lights. Here's what you can do with it:

### Set an individual pixels color
```
self.pixels[idx] = (0, 128, 255)
```

### Set a range of pixel colors
```
self.pixels[0:2] = [(0, 0, 255), (255, 255, 0)]
```

### Fill all pixels with a single color
```
self.pixels.fill((255, 255, 255))
```

Unfortunately there's not a lot you can do as of now, but it should be enough to create some pretty animations :). Of course feel free to extend this basic interface with your own higher-level functions in your animations. We just ask that you consider adding functions you think would be useful to other animators to the `utils` subdirectory if it's not already there. 

## Registering an animation



### Testing using the simulator

Animators anywhere can test their animations using the simulator