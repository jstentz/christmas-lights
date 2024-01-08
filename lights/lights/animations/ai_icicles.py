import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation

class IcicleDripAnimation(BaseAnimation):
    """This class represents an animation of icicles dripping to the ground."""

    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 10):
        """
        Initializes the animation parameters.

        Required:
         - frameBuf [np.ndarray]: N x 3 array of RGB color values where N is the number of lights.
         - fps [int | None]: Speed of the animation in frames per second. This value doesn't change.
        """
        super().__init__(frameBuf, fps)
        self.drip_speed = 1  # Speed of the icicles' descent

    def renderNextFrame(self):
        """
        Generates the next animation frame simulating icicles dripping.
        
        IMPORTANT! Operations must modify the frameBuf in place as it's a shared buffer.
        """
        # Define colors representing icicles
        light_blue = (173, 216, 230)  # Light blue color
        white = (255, 255, 255)  # White color

        # Calculate the number of rows (lights) in the frameBuf
        num_lights = self.frameBuf.shape[0]

        # Calculate the number of lights to shift downwards in each frame
        lights_to_shift = int(self.fps / self.drip_speed)

        # Shift the colors down the array to simulate the icicles' descent
        self.frameBuf[lights_to_shift:] = self.frameBuf[:-lights_to_shift]
        
        # Fade the top rows (lights_to_shift) from light blue to white to represent melting icicles
        for i in range(lights_to_shift):
            alpha = i / lights_to_shift
            blended_color = tuple(int((1 - alpha) * light_blue[j] + alpha * white[j]) for j in range(3))
            self.frameBuf[i] = blended_color
