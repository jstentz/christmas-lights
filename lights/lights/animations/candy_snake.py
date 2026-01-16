"""
Template animation file.
Replace this with your own animation class, or use --sample to run a sample animation.
"""
import random
from lights.animations.base import BaseAnimation
from typing import Optional
import numpy as np

# Write your animation here!

class CandySnake(BaseAnimation):
    lightNumber = 500
    backgroundColour = [0, 0, 0]
    def __init__(self, frameBuf, *, fps: Optional[int] = 20):
        super().__init__(frameBuf, fps=fps)
        self.t = 0
        self.snake = Snake(self.lightNumber-1)
        self.apple = Apple((self.lightNumber-1, 0))

    def renderNextFrame(self):
        # Update self.frameBuf with RGB values (0-255)
        # frameBuf is a numpy array of shape (NUM_PIXELS, 3)
        if self.snake.isFull():
            self.reset()
        snakeRange = self.snake.getRange()

        if self.snake.getFront() == self.apple.position:
            self.snake.eat()
            self.apple.spawn(self.snake.getRange(), self.snake.forward)

        for i in range(len(self.frameBuf)):
            # Your animation logic here
            if i <= snakeRange[0] and i >= snakeRange[1]:
                self.frameBuf[i] = self.snake.getColour(i)
            elif i == self.apple.position:
                self.frameBuf[self.apple.position] = self.apple.getColour()
            else:
                self.frameBuf[i] = self.backgroundColour
        self.snake.move()
        self.t += 1
    def reset(self):
        self.t = 0
        self.snake = Snake(self.lightNumber-1)
        self.apple = Apple((self.lightNumber-1, 0))

class Snake:
    colours = [[255, 0, 0], [255, 255, 255]]
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.position = maxLength//2
        self.length = 0
        self.forward = True
    
    def isFull(self) -> bool:
        if self.length == self.maxLength:
            return True
        return False
    
    def eat(self):
        self.length += 1
        self.forward = not self.forward
    
    def move(self):
        if self.forward:
            if self.position + 1 > self.maxLength:
                self.forward = not self.forward
                return
            self.position += 1
            return
        
        if self.position - 1 < 0:
            self.forward = not self.forward
            return
        self.position -= 1
    
    def getRange(self):
        return (self.position, self.position - self.length)
    
    def getFront(self):
        if self.forward:
            return self.position
        return self.position - self.length
    
    def getColour(self, position):
        if (self.position - position) % 3 == 0:
            return self.colours[0]
        return self.colours[1]

class Apple:
    colours = [[255, 0, 0], [255, 255, 255]]
    def __init__(self, spawnRange):
        self.spawnRange = spawnRange
        self.eaten = 0
        self.spawn((spawnRange[0]//2, spawnRange[0]//2), True)
    
    def spawn(self, snakeRange, snakeForward):
        self.eaten += 1
        if snakeForward:
            self.position = random.randint(snakeRange[0], self.spawnRange[0])
            return
        self.position = random.randint(self.spawnRange[1], snakeRange[1])

    def getColour(self):
        if self.eaten % 3 == 0:
            return self.colours[0]
        return self.colours[1]