import random
from lights.animations.base import BaseAnimation
from lights.utils.colors import rainbowFrame, brightnessFrame
from typing import Optional, Collection

class Snake(BaseAnimation):
  def __init__(self, pixels, *, fps: Optional[int] = None, numFood: int = 10, snakeColor: Collection[int] = (0,255,0), foodColor: Collection[int] = (255,0,0), isRainbow: bool = False):
    super().__init__(pixels, fps=fps)
    self.numFood = numFood
    self.isRainbow = isRainbow
    self.foodColor = foodColor
    self.snakeColor = snakeColor
    self.food = random.sample(range(len(self.pixels)), self.numFood)
    self.body = [random.randint(0, len(self.pixels) - 1)]
    self.S = set([i for i in range(len(pixels))]) # set of all indices
    
  def renderNextFrame(self):
    NUM_PIXELS = len(self.pixels)
  
    # max length snake
    if len(set(self.body)) == NUM_PIXELS:
      self.food = random.sample(range(NUM_PIXELS), self.numFood)
      self.body = [random.randint(0, NUM_PIXELS - 1)]
      # reset

    # move the snake
    head = self.body[0]
    nearestFood = None
    nearestDist = None
    for i in self.food:
      d = abs(i - head)
      if nearestFood == None or d < nearestDist:
        nearestFood = i
        nearestDist = d

    dir = +1 if nearestFood > head else -1
    newHead = head + dir
    self.body.insert(0, newHead)

    if newHead in self.food:
      self.food.remove(newHead)
      foodOptions = list(self.S - set(self.food) - set(self.body))
      if foodOptions != []:
        self.food.append(random.choice(foodOptions))
    else:
      self.body.pop()

    # update pixels
    uniqueBodyList = []
    for idx in self.body:
      if idx not in uniqueBodyList:
        uniqueBodyList.append(idx)

    if self.isRainbow:
      snakeFrame = rainbowFrame(0, len(uniqueBodyList))[::-1]
    else:
      snakeFrame = brightnessFrame(self.snakeColor, len(uniqueBodyList))[::-1]

    for i in range(NUM_PIXELS):
      if i in self.food:
        self.pixels[i] = self.foodColor
      else:
        self.pixels[i] = (0, 0, 0)

    for i in range(len(uniqueBodyList)):
      pixelIdx = uniqueBodyList[i]
      self.pixels[pixelIdx] = snakeFrame[i]

      
