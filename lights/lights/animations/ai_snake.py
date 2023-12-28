import numpy as np
import random
from typing import Optional, Collection
from lights.animations.base import BaseAnimation

class SnakeGameAnimation(BaseAnimation):
    """Animation of the classic 'Snake' game along a string of lights."""

    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = None):
        """
        Sets up the Snake game animation parameters.
        
        Required:
         - frameBuf [np.ndarray]: A N x 3 array of RGB color values where N is the number of lights  
         - fps [int | None]: The speed of the animation in frames per second 
        """
        super().__init__(frameBuf, fps)
        self.snake = [0]  # Start with a snake of length 1
        self.food = self._generate_food(10)  # Initially place 10 food items
        self.snake_color = [0, 255, 0]  # Green color for snake
        self.food_color = [255, 0, 0]  # Red color for food
        self.blank_color = [0, 0, 0]  # Blank color

    def _generate_food(self, count):
        """Generates 'count' number of food positions randomly."""
        all_positions = set(range(len(self.frameBuf)))
        snake_set = set(self.snake)
        available = list(all_positions - snake_set)
        return random.sample(available, count)

    def _reset_game(self):
        """Resets the game when the snake length reaches 30."""
        self.snake = [0]
        self.food = self._generate_food(10)

    def renderNextFrame(self):
        """
        Updates the Snake game state for each frame.
        """
        # Move the snake
        head = self.snake[-1] + 1
        if head == len(self.frameBuf):
            head = 0

        # Check for food collision
        if head in self.food:
            self.food.remove(head)
            self.food.extend(self._generate_food(1))  # Add new food
        else:
            self.snake.pop(0)  # Remove tail

        # Grow the snake
        self.snake.append(head)

        # Check for reset condition
        if len(self.snake) > 30:
            self._reset_game()

        # Update frameBuf
        self.frameBuf[:] = self.blank_color
        for pos in self.snake:
            self.frameBuf[pos] = self.snake_color
        for pos in self.food:
            self.frameBuf[pos] = self.food_color
