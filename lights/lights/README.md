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
import numpy as np

class NewAnimation(BaseAnimation): # all animations inherit from BaseAnimation
  # Unpack custom argument and initialize state (if using) in the initializer.
  def __init__(self, frameBuf, *, fps=None, custom_arg1="default_value_1", custom_arg2="default_value_2"):
    super().__init__(frameBuf, fps=fps)
    self.custom_arg_1 = custom_arg_1
    self.custom_arg_2 = custom_arg_2
    self.state = {}

  # You can write the core logic of your animation in this function.
  # It's called at the specified frame rate (every 1/fps seconds).
  def renderNextFrame(self):
    # Set the zeroth light to be red.
    self.frameBuf[0] = np.array([255, 0, 0]) # RGB.

  # Perform any cleanup work here.
  def shutdown(self):
    pass
```

The `__init__` method is called initially, and `renderNextFrame` is called at the frequency defined by the `fps` parameter. If `fps=None`, the method is called as often as possible.

Any given frame is defined by `self.frameBuf`, a `(500, 3)`-shaped numpy array which stores the RGB values of each light on the tree. There are many operations that can be done on such arrays, but here are some examples:

### Set an individual pixels color
```python
self.frameBuf[idx] = np.array([0, 128, 255]) 
```

### Set a range of pixel colors
```python
self.frameBuf[0:2] = np.array([[0, 0, 255], [255, 255, 0]])
```

### Fill all pixels with a single color
```python
self.frameBuf[:] = np.array([255, 255, 255])
```

### Important note

Since the numpy array pointed to by `self.frameBuf` is used to update the lights, it is critical that all changes made to `self.frameBuf` are done in place. Here is an example of what not to do:

```python
# Attempting to make all the lights blue.
def renderNextFrame(self):
  # Create a blue frame.
  blueFrame = np.zeros((len(self.frameBuf), 3))
  blueFrame[:, 2] = 255

  # The following line breaks the alias!
  self.frameBuf = blueFrame
```

To fix the last line, we should instead do
```python
self.frameBuf[:] = blueFrame
```
to make the operation in-place.

### 3D animations

To support animations that rely on the spatial location of the lights on the tree, we provide another `(500, 3)`-shaped array of the points locations. Each row corresponds to a single (x, y, z) location. The points have been centered around their mean and scaled such that all coordinates are within the range [-1, +1]. Each row in the array of points maps directly to the same row in `self.frameBuf`. To access these points, use the following import line:

```python
from lights.utils.geometry import POINTS_3D
```

### Efficiency

Since the animations are currently being run on a Raspberry Pi, efficiency is imperative. Please take advantage of numpy's vectorized operations as much as humanly possible. Generally, avoiding significant looping within Python is the most important.

Here is an example of converting slow, unvectorized code into fast, vectorized code.

Animation that sets all pixels above z = 0 to red, and all points below z = 0 to be green:

```python
# Slow python looping.
def renderNextFrame(self):
  for i in range(len(self.frameBuf)):
    if POINTS_3D[i, 2] > 0:
      self.frameBuf[i] = np.array([255, 0, 0]) # Red.
    else:
      self.frameBuf[i] = np.array([0, 255, 0]) # Green.
```

```python
# Fast vectorized numpy operations.
def renderNextFrame(self):
  above = POINTS_3D[:, 2] > 0
  self.frameBuf[above] = np.array([255, 0, 0]) # Red.
  self.frameBuf[np.logical_not(above)] = np.array([0, 255, 0]) # Green.
```

## Testing using the simulator

### Simulating an animation
Animators anywhere can test their animations using controllers. To list all available animations and controllers, run the command:

```shell
python run_animation.py -l
```

To simulate your animation as seen on the tree, run the command:
```shell
python run_animation.py -c MatplotlibController -a AnimationClassName
```

To simulate your animation in a graphics window, run the command:
```shell
python run_animation.py -c GuiController -a AnimationClassName
```

You can also run your animation within the terminal. In a terminal that supports 24-bit color (like vscode's built-in terminal), run the command:
```shell
python run_animation.py -c TerminalController -a AnimationClassName
```

You can stop the simulation by closing the graphics window or sending a SIGINT (`ctrl + c`).

### Passing arguments
If your animation has arguments, you can provide them to the simulator using the `--args` flag

```shell
python run_animation.py -c ControllerName -a AnimationClassName --args custom_arg_1='value' color=255,0,0 fps=30
```

Custom arguments are parsed with `ast.literal_eval`, so they can be any valid python expression. More specifically, the left side of the '=' must be a valid python variable name, and the right side a valid expression. One caveat is that tuples cannot have parenthesis, so a tuple typically expressed as `(0, 255, 255)` must be passed as `0,255,255`.

You can also see the optional parameters for a given animation using `-i`
```shell
python run_animation.py -a AnimationClassName -i
```