import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation

class AmericanFlagAnimation(BaseAnimation):
    """Animation that creates an America-themed display with red, white, and blue colors."""

    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = None):
        """
        Sets up the America-themed animation parameters.
        
        Required:
         - frameBuf [np.ndarray]: A N x 3 array of RGB color values where N is the number of lights  
         - fps [int | None]: The speed of the animation in frames per second 
        """
        super().__init__(frameBuf, fps)
        self.colors = [
            [255, 0, 0],    # Red
            [255, 255, 255],# White
            [0, 0, 255]     # Blue
        ]
        self.color_index = 0

    def renderNextFrame(self):
        """
        Updates the frame to display a dynamic American flag theme.
        """
        # Update the color pattern
        self.color_index = (self.color_index + 1) % len(self.colors)

        # Apply the colors in a repeating pattern
        for i in range(len(self.frameBuf)):
            self.frameBuf[i] = self.colors[(i + self.color_index) % len(self.colors)]
