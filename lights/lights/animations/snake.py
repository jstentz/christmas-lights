import random
from lights.animations.base import BaseAnimation

class Snake(BaseAnimation):
  def __init__(self, pixels, fps=None, numFood=5):
    super().__init__(pixels, fps=fps)
    self.numFood = numFood
    self.food = random.sample(range(len(self.pixels)), self.numFood)
    self.body = [random.randint(0, len(self.pixels) - 1)]
    self.empty = set([i for i in range(len(self.pixels))])
    self.empty.remove(self.body[0])
    for f in self.food:
      self.empty.remove(f)
    
  def renderNextFrame(self):
    NUM_PIXELS = len(self.pixels)
  
    # max length snake
    if len(set(self.body)) == NUM_PIXELS:
      self.food = random.sample(range(NUM_PIXELS), self.numFood)
      self.body = [random.randint(0, NUM_PIXELS - 1)]
      self.empty = set([i for i in range(NUM_PIXELS)])
      self.empty.remove(self.body[0])
      for f in self.food:
        self.empty.remove(f)
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

    if newHead in self.empty: 
      self.empty.remove(newHead)

    if newHead in self.food:
      self.food.remove(newHead)
      foodOptions = list(self.empty)
      if foodOptions != []:
        self.food.append(random.choice(list(self.empty)))
    else:
      tail = self.body.pop()
      self.empty.add(tail)

    # update pixels
    for i in range(NUM_PIXELS):
      if i in self.food:
        self.pixels[i] = (255, 0, 0)
      elif i == newHead:
        self.pixels[i] = (0, 255, 0)
      elif i in self.body:
        self.pixels[i] = (0, 255, 0)
      else:
        self.pixels[i] = (0, 0, 0)  