import numpy as np
from lights.animations.base import BaseAnimation
from typing import Optional
import random

class Collatz(BaseAnimation):
    def __init__(self, frameBuf, *, fps: Optional[int] = None, start_number: int = 499, decay: float = 0.85):
        super().__init__(frameBuf, fps=fps)
        self.number = random.randint(2, start_number)
        self.start_number = start_number
        self.decay = decay

    def renderNextFrame(self):
        NUM_PIXELS = len(self.frameBuf)
        if self.number == 1:
            self.number = random.randint(2, self.start_number)
        current_number = self.number
        decay = self.decay

        # Apply Collatz conjecture
        if current_number % 2 == 0:
            current_number //= 2
        else:
            current_number = 3 * current_number + 1

        # Map the current number to pixel index
        index = current_number % NUM_PIXELS

        # Turn on the corresponding pixel
        self.frameBuf[NUM_PIXELS - index - 1] = (255, 255, 255)

        # Decay all pixels
        self.frameBuf[:] = self.frameBuf * decay

        # Update the current number for the next frame
        self.number = current_number