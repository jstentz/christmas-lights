from lights.lights_util import Lights
import random
from lights.constants import NUM_PIXELS, PIN, ORDER

def snake(pixels, numFood=5):
  food = random.sample(range(NUM_PIXELS), numFood)
  body = [random.randint(0, NUM_PIXELS - 1)]
  empty = set([i for i in range(NUM_PIXELS)])
  empty.remove(body[0])
  for f in food:
    empty.remove(f)
  
  while True:
    # max length snake
    if len(set(body)) == NUM_PIXELS:
      food = random.sample(range(NUM_PIXELS), numFood)
      body = [random.randint(0, NUM_PIXELS - 1)]
      empty = set([i for i in range(NUM_PIXELS)])
      empty.remove(body[0])
      for f in food:
        empty.remove(f)
      # reset

    # move the snake
    head = body[0]
    nearestFood = None
    nearestDist = None
    for i in food:
      d = abs(i - head)
      if nearestFood == None or d < nearestDist:
        nearestFood = i
        nearestDist = d

    dir = +1 if nearestFood > head else -1
    newHead = head + dir
    body.insert(0, newHead)

    if newHead in empty: 
      empty.remove(newHead)

    if newHead in food:
      food.remove(newHead)
      foodOptions = list(empty)
      if foodOptions != []:
        food.append(random.choice(list(empty)))
    else:
      tail = body.pop()
      empty.add(tail)

    # update pixels
    for i in range(NUM_PIXELS):
      if i in food:
        pixels[i] = (255, 0, 0)
      elif i == newHead:
        pixels[i] = (0, 255, 0)
      elif i in body:
        pixels[i] = (0, 255, 0)
      else:
        pixels[i] = (0, 0, 0)  
    pixels.show()

if __name__ == '__main__':
  import argparse
  pixels = Lights(PIN, NUM_PIXELS, auto_write=False, pixel_order=ORDER)

