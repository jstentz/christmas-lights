"""
Given a user-supplied prompt, generate a python file with code that produces a light animation that adheres to template displayed below. 

Follow these steps when generating the code:
Step 1 - Think about assumptions that must be made about the prompt. Then write down a one sentence summary of the assumptions as a comment in the top of the python file.
Step 2 - Write a one sentence interpretation of what the animation should do as a comment in the top of the generated python file.
Step 3 - Use the interpretation, assumptions, and ambiguities from the previous steps to write the python code to create the animation that matches the prompt. 
         The python code should match the template below. You cannot use any variables or attributes in the code that you have not declared.
"""


import numpy as np 
from typing import Optional, Collection
from lights.animations.base import BaseAnimation # this is the class that all animations should inherit from

# This is an example of an animation class that sets all of the lights in the array to the input color.
class UniformColorLights(BaseAnimation): # All animations should inherit from the parent class 'BaseAnimation'
  """This is an example class for the light animation where all of the lights in the input frameBuf 
  will be set to red."""

  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = None, color: Collection[int] = (255, 0, 0)):
    """
    Sets up the specific animation parameters. 

    Required:
    These parameters must be present in the __init__ function for all aniimation classes.
     - frameBuf [np.ndarray]: A N x 3 array of RGB color values where N is the number of lights  
     - fps [int | None]: The speed of the animation in frames per second 

    Optional:
    These parameters always follow the required parameters and are specific to this animation. Be creative and add these parameters to further customize the animation.
    - color [tuple[int]]: Desired color for the lights as RGB. The default is red.
    """
    super().__init__(frameBuf, fps) # A call to the parent's __init__ function must be present here
    self.color = color # initialize the input color value

  def renderNextFrame(self):
    """
    This function should generate the next animation frame and store in the class's frameBuf attribute. 

    IMPORTANT! The frameBuf is a shared buffer, so all modifications must be in place. Operations that create a copy of the frameBuf will not work. 
    """
    self.frameBuf[:] = self.color # this sets every color value in the frameBuf to the input color