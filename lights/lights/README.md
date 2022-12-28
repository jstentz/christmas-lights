# Lights

## Installation
At the root of the repository, create a virtual environment and install the requirements:
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Still in the virtual environment, install the local change to the first `lights` folder and install the local `lights` package:
```shell
cd lights
pip install -e .
```

## Creating an animation

All animations live in their own file in the `animations` subdirectory. Here's the basic structure of an animation:
```python
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
```python
self.pixels[idx] = (0, 128, 255)
```

### Set a range of pixel colors
```python
self.pixels[0:2] = [(0, 0, 255), (255, 255, 0)]
```

### Fill all pixels with a single color
```python
self.pixels.fill((255, 255, 255))
```

Unfortunately there's not a lot you can do as of now, but it should be enough to create some pretty animations :). Of course feel free to extend this basic interface with your own higher-level functions in your animations. We just ask that you consider adding functions you think would be useful to other animators to the `utils` subdirectory if it's not already there. 

## Testing using the simulator

### Simulating an animation
Animators anywhere can test their animations using the simulator. To simulate your animation in a graphics window, run the command:
```shell
python run_animation.py -a AnimationClassName
```

You can also run your animation within the terminal. In a terminal that supports 24-bit color (like vscode's built-in terminal), run the command:
```shell
python run_animation.py -t -a AnimationClassName
```

You can stop the simulation by running sending a SIGINT (`ctrl + c`).

For a list of all animations, use `-l`

```shell
python run_animation.py -l
```

### Passing arguments
If your animation has arguments, you can provide them to the simulator using the `--args` flag

```shell
python run_animation.py -a AnimationClassName --args custom_arg_1='value' color=255,0,0 fps=30
```

Custom arguments are parsed with `ast.literal_eval`, so they can be any valid python expression. More specifically, the left side of the '=' must be a valid python variable name, and the right side a valid expression. One caveat is that tuples cannot have parenthesis, so a tuple typically expressed as `(0, 255, 255)` must be passed as `0,255,255`.

You can also see the optional parameters for a given animation using `-i`

```shell
python run_animation.py -a AnimationClassName -i
```
