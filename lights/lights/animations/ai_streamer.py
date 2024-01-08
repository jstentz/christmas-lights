import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation

class RainbowStreamersAnimation(BaseAnimation):
    """Animation that creates rainbow streamers along a string of lights."""

    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 5):
        """
        Sets up the rainbow streamers animation parameters.
        
        Required:
         - frameBuf [np.ndarray]: A N x 3 array of RGB color values where N is the number of lights  
         - fps [int | None]: The speed of the animation in frames per second 
        """
        super().__init__(frameBuf, fps)
        self.rainbow_colors = [
            [255, 0, 0],    # Red
            [255, 127, 0],  # Orange
            [255, 255, 0],  # Yellow
            [0, 255, 0],    # Green
            [0, 0, 255],    # Blue
            [75, 0, 130],   # Indigo
            [148, 0, 211]   # Violet
        ]
        self.color_index = 0

    def renderNextFrame(self):
        """
        Updates the streamers to show a flowing rainbow effect.
        """
        # Move the rainbow streamer
        self.color_index = (self.color_index + 1) % len(self.rainbow_colors)

        # Update frameBuf with the rainbow colors
        for i in range(len(self.frameBuf)):
            color = self.rainbow_colors[(self.color_index + i) % len(self.rainbow_colors)]
            self.frameBuf[i] = color
