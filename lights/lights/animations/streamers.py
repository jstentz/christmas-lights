import random
from lights.animations.base import BaseAnimation
from lights.utils.colors import randomColor, brightnessFrame

class Streamers(BaseAnimation):
  def __init__(self, pixels, *, fps=None, numStreamers=10, streamersLen=10):
    super().__init__(pixels, fps=fps)
    self.pixels = pixels
    self.numStreamers = numStreamers
    self.streamersLen = streamersLen
    
    NUM_PIXELS = len(pixels)

    # for now, let's make every other streamer move in opposite directions
    # maybe I could differ the speeds in the future
    # I also don't want them to spawn overlapping at some point
    # stored as (headLoc, color, movingUp)
    # streamers = random.sample([i for i in range(NUM_PIXELS)], numStreamers)

    self.streamers = [(random.randint(0, NUM_PIXELS-1), randomColor(), random.choice((True, False))) for _ in range(numStreamers)]

  def renderNextFrame(self):
    # move the streamers heads in their specified directions
    for i in range(len(self.streamers)):
      headLoc, color, movingUp = self.streamers[i]
      newHeadLoc = headLoc + 1 if movingUp else headLoc - 1
      self.streamers[i] = (newHeadLoc, color, movingUp)
    
    
    # update the pixels with brightness frame
    NUM_PIXELS = len(self.pixels)
    for i in range(NUM_PIXELS):
      self.pixels[i] = (0, 0, 0)

    for (headLoc, color, movingUp) in self.streamers:
      frame = brightnessFrame(color, self.streamersLen)
      for i in range(len(frame)):
        if movingUp:
          loc = (headLoc + i) % NUM_PIXELS
        else:
          loc = (headLoc - i) % NUM_PIXELS
        self.pixels[loc] = frame[i]

