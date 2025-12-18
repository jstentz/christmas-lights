imporxtt numpy as np
from typing import *
from lights.animations.base import BaseAnimation


class MarsStripesAnimation(BaseAnimation):

    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, stripe_width: int = 10):
        """
        Required:
         - frameBuf [np.ndarray]: A Nx3 array of RGB color values where N is the number of lights
         - fps [int | None]: The speed of the animation in frames per second

        Optional:
        - stripe_width [int]: Width of each stripe in number of lights. Default is 10.
        """
        super().__init__(frameBuf, fps)
        self.stripe_width = stripe_width
        # Define colors for Mars-like stripes
        self.colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0)]  # Red, Orange, Yellow
        self.color_index = 0
        self.frame_count = 0

    def renderNextFrame(self):
        """
        Produces the next animation frame, creating moving stripes of colors across the frame buffer.
        """
        n_lights = len(self.frameBuf)
        # Calculate which color to start with based on the frame_count
        start_color_index = (self.frame_count // self.stripe_width) % len(self.colors)

        for i in range(n_lights):
            # Calculate color index based on current light's position and the start color index
            color_index = (start_color_index + i // self.stripe_width) % len(self.colors)
            self.frameBuf[i] = self.colors[color_index]

        self.frame_count += 1
