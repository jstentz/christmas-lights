import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation

# Assumptions: The animation mimics twinkling stars using a light array. 
# Interpretation: Random lights will brighten and dim to resemble stars twinkling in the night sky.

class TwinklingStarsAnimation(BaseAnimation):
    """
    An animation class that simulates twinkling stars.
    """

    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 25, twinkling_intensity: int = 100):
        """
        Sets up the twinkling stars animation parameters.

        Required:
        - frameBuf [np.ndarray]: A N x 3 array of RGB color values where N is the number of lights
        - fps [int | None]: The speed of the animation in frames per second

        Optional:
        - twinkling_intensity [int]: The intensity of the twinkling effect. Higher values mean more twinkling.
        """
        super().__init__(frameBuf, fps)
        self.twinkling_intensity = twinkling_intensity

    def renderNextFrame(self):
        """
        Generates the next frame of the twinkling stars animation.
        """
        for i in range(len(self.frameBuf)):
            # Randomly adjust brightness to simulate twinkling
            adjustment = np.random.randint(-self.twinkling_intensity, self.twinkling_intensity)
            new_color = np.clip(self.frameBuf[i] + adjustment, 0, 255)
            self.frameBuf[i] = new_color

# Example usage
# frameBuf = np.zeros((100, 3), dtype=int)  # Assuming 100 lights
# animation = TwinklingStarsAnimation(frameBuf, fps=30)
# while True:
#     animation.renderNextFrame()
#     # Add code to display frameBuf here
