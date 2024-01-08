import numpy as np 
from typing import Optional, Collection
from lights.animations.base import BaseAnimation

class EvenOddSwapAnimation(BaseAnimation):
    """Animation where even-indexed lights are red and odd-indexed lights are green, 
    with colors swapping every frame."""

    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 1):
        """
        Sets up the animation parameters.
        
        Required:
         - frameBuf [np.ndarray]: A N x 3 array of RGB color values where N is the number of lights  
         - fps [int | None]: The speed of the animation in frames per second 
        """
        super().__init__(frameBuf, fps)
        self.is_even_frame = True  # Toggle to track the frame state (even or odd)

    def renderNextFrame(self):
        """
        Generates the next frame with alternating colors for even and odd lights.
        """
        if self.is_even_frame:
            # Set even lights to red and odd lights to green
            self.frameBuf[::2] = [255, 0, 0]  # Even lights
            self.frameBuf[1::2] = [0, 255, 0]  # Odd lights
        else:
            # Swap colors: Set even lights to green and odd lights to red
            self.frameBuf[::2] = [0, 255, 0]  # Even lights
            self.frameBuf[1::2] = [255, 0, 0]  # Odd lights

        self.is_even_frame = not self.is_even_frame  # Toggle the frame state
