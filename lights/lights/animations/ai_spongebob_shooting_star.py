import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation

# Assumptions: The animation represents a Spongebob-themed shooting star moving across a light array.
# Interpretation: A yellow star (representing Spongebob) will move across the lights, leaving a brief trail.

class SpongebobShootingStarAnimation(BaseAnimation):
    """
    An animation class that simulates a Spongebob-themed shooting star.
    """

    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = None, star_size: int = 5, trail_length: int = 10):
        """
        Sets up the Spongebob shooting star animation parameters.

        Required:
        - frameBuf [np.ndarray]: A N x 3 array of RGB color values where N is the number of lights
        - fps [int | None]: The speed of the animation in frames per second

        Optional:
        - star_size [int]: The size of the star (number of lights).
        - trail_length [int]: The length of the star's trail.
        """
        super().__init__(frameBuf, fps)
        self.star_size = star_size
        self.trail_length = trail_length
        self.star_position = -self.star_size  # Start off-screen

    def renderNextFrame(self):
        """
        Generates the next frame of the Spongebob shooting star animation.
        """
        self.frameBuf[:] = (0, 0, 0)  # Reset frame to black (space)

        # Draw the star
        start = self.star_position
        end = start + self.star_size
        self.frameBuf[start:end] = (255, 255, 0)  # Spongebob yellow

        # Draw the trail
        for i in range(1, self.trail_length + 1):
            if start - i >= 0:
                fade_factor = (self.trail_length - i + 1) / self.trail_length
                self.frameBuf[start - i] = (255 * fade_factor, 255 * fade_factor, 0)

        # Update the star position for the next frame
        self.star_position += 1
        if self.star_position > len(self.frameBuf):
            self.star_position = -self.star_size  # Reset to start position

# Example usage
# frameBuf = np.zeros((100, 3), dtype=int)  # Assuming 100 lights
# animation = SpongebobShootingStarAnimation(frameBuf, fps=30)
# while True:
#     animation.renderNextFrame()
#     # Add code to display frameBuf here
