import board
import neopixel
import random
import time
import colorsys
import math
import copy

ORDER = neopixel.RGB
NUM_PIXELS = 500
pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS, auto_write=False, pixel_order=ORDER)

def clearLights():
  for i in range(NUM_PIXELS):
    pixels[i] = (0, 0, 0)

def updatePixelsFromList(L):
  for i in range(len(L)):
    pixels[i] = L[i]

def randomColor():
  return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def randomColors():
  for i in range(NUM_PIXELS):
    pixels[i] = randomColor()

def randomGreenRed():
  for i in range(NUM_PIXELS):
    pixels[i] = random.choice(((255, 0, 0), (0, 255, 0)))

def oneColor(color):
  pixels.fill(color)

def breathe(color, t, rate):
  (r, g, b) = color
  for i in range(NUM_PIXELS):
    brightness = (math.sin(t/rate) + 1) / 2
    pixels[i] = (r * brightness, g * brightness, b * brightness)

# density should be between 0 and 1
def snowflakes(density=.005, decayRate=.99):
  snow = (0, 0, 255)
  blank = (0, 0, 0)
  
  for i in range(NUM_PIXELS):
    color = pixels[i]
    pixels[i] = tuple([int(c * decayRate) for c in color])
    if pixels[i] == list(blank):
      n = random.uniform(0, 1)
      if n < density:
        pixels[i] = snow

def downTheLine(color, t, rate=1, decay=0.9):
  for i in range(rate):
    index = t % NUM_PIXELS - (i * NUM_PIXELS // rate)
    pixels[index] = color
  for i in range(NUM_PIXELS):
    color = pixels[i]
    pixels[i] = tuple(int(c * decay) for c in color)

# exp must be an even number >= 2 and freq must be >= 1
def rainbowSine(t, freq=1, exp=10):
  for i in range(NUM_PIXELS):
    c = (i + t) % NUM_PIXELS
    h = math.sin(i * math.pi / NUM_PIXELS)
    s = 1.0
    v = math.sin(c * math.pi * freq / NUM_PIXELS)**exp # change exponent for faster brightness drop off
    pixels[i] = tuple([int(v * 255) for v in colorsys.hsv_to_rgb(h, s, v)])

def colorSine(t, freq=1, exp=2):
  for i in range(NUM_PIXELS):
    c = (i + t) % NUM_PIXELS
    h = math.sin(c * math.pi * freq / NUM_PIXELS)**exp # change exponent for faster brightness drop off
    s = 1.0
    v = 1.0
    pixels[i] = tuple([int(v * 255) for v in colorsys.hsv_to_rgb(h, s, v)])

def movingRainbow(t, freq=1, exp=2):
  for i in range(NUM_PIXELS):
    c = (i + t) % NUM_PIXELS
    h = math.sin(c * math.pi * freq / NUM_PIXELS)**exp # change exponent for faster brightness drop off
    s = 1.0
    v = math.sin(c * math.pi * freq / NUM_PIXELS)**exp
    pixels[i] = tuple([int(v * 255) for v in colorsys.hsv_to_rgb(h, s, v)])


def rainbowFrame(t):
  """
  Generates rgb values for a rainbow gradient at time t.
  """
  return [[int(v * 255) for v in colorsys.hsv_to_rgb((c + t) % NUM_PIXELS / NUM_PIXELS, 1.0, 1.0)] for c in range(NUM_PIXELS)]

def randomSwap():
  i0 = random.randint(0, NUM_PIXELS - 1)
  i1 = random.randint(0, NUM_PIXELS - 1)
  c0 = pixels[i0]
  c1 = pixels[i1]
  pixels[i0] = c1
  pixels[i1] = c0

# assign random colors, then on each call to the function, run one round of selection sort
def colorSort():
  rainbow = rainbowFrame(0)
  updatePixelsFromList(rainbow)
  for _ in range(NUM_PIXELS):
    randomSwap()
  
  sortedIdx = 0
  while True:
    minHIdx = None
    minH = None
    for i in range(sortedIdx, NUM_PIXELS):
      (h, _, _) = colorsys.rgb_to_hsv(*pixels[i]) # might have to do *tuple(pixels[i])
      if minH == None or h < minH:
        minH = h
        minHIdx = i
    # swap!
    c1 = pixels[sortedIdx]
    c2 = pixels[minHIdx]
    pixels[sortedIdx] = c2
    pixels[minHIdx] = c1
    sortedIdx += 1
    if sortedIdx == NUM_PIXELS:
      rainbow = rainbowFrame(0)
      updatePixelsFromList(rainbow)
      for _ in range(NUM_PIXELS):
        randomSwap()
      sortedIdx = 0
    pixels.show()
    time.sleep(0.1)

# make sure not to generate food that is inside of the snakes body
# plays 1D snake!
def snake(numFood=5):
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


def redGreenSwap(t, delay):
  for i in range(NUM_PIXELS):
    if t % 2 == 0:
      if i % 2 == 0:
        pixels[i] = (255, 0, 0)
      else:
        pixels[i] = (0, 255, 0)
    else:
      if i % 2 != 0:
        pixels[i] = (255, 0, 0)
      else:
        pixels[i] = (0, 255, 0)
  time.sleep(delay)

def randomRedGreen():
  for i in range(NUM_PIXELS):
    pixels[i] = random.choice([(255, 0, 0), (0, 255, 0)])
  time.sleep(1)

# this one sucks lol
def binaryCount(t):
  maxVal = 2**500 - 1
  v = t % maxVal
  newPixels = [int(i) for i in list('{0:0b}'.format(v))]
  for i in range(len(newPixels)):
    if newPixels[i]:
      pixels[i] = (255, 0, 0)
    else:
      pixels[i] = (0, 0, 0)


def gameOfLife1D(color, delay=0.1):
  # generate random game state
  # state = [random.choice([True, False]) for _ in range(NUM_PIXELS)]
  state = [True, True] + [False for _ in range(NUM_PIXELS - 2)]
  while True:
    # update state 
    newState = copy.copy(state)
    for i in range(len(state)):
      curr = state[i]
      prev = state[(i - 1) % NUM_PIXELS]
      next = state[(i + 1) % NUM_PIXELS]
      if curr and prev and next:
        newState[i] = False
      elif curr and not (prev or next):
        newState[i] = False
      elif not curr and (prev ^ next):
        newState[i] = True

      if newState[i]:
        pixels[i] = color
      else:
        pixels[i] = (0, 0, 0)
    state = copy.copy(newState)
    pixels.show()
    time.sleep(delay)


clearLights()
pixels.show()
# snake(numFood=5)
# oneColor((255, 255, 255))
# pixels.show()
# colorSort()
gameOfLife1D((0, 255, 0), delay=1)
t = 0
while True:
  # insert function call here!
  # if t % NUM_PIXELS == 0:
  #   color = randomColor()
  # downTheLine(color, t, rate=3, decay=0.99)
  # snowflakes()
  # rainbowSine(t, freq=5, exp=10)
  # redGreenSwap(t, 1)
  # randomRedGreen()
  # binaryCount(t)
  # breathe((255, 0, 0), t, 2)
  # colorSine(t)
  # oneColor((255, 255, 255))
  pixels.show()
  # time.sleep(0.1)
  t += 1
