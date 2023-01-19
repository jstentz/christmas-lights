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

    self.streamers = [
                      (
                        random.randint(0, NUM_PIXELS-1), # head location
                        randomColor(),                   # color
                        random.randint(1, 3),            # speed (1 is fastest)
                        random.choice((True, False))     # direction
                      )
                      for _ in range(numStreamers)]
    self.t = 0

  def renderNextFrame(self):
    # move the streamers heads in their specified directions
    for i in range(len(self.streamers)):
      headLoc, color, speed, movingUp = self.streamers[i]
      if self.t % speed == 0:
        newHeadLoc = headLoc + 1 if movingUp else headLoc - 1
        self.streamers[i] = (newHeadLoc, color, speed, movingUp)
    
    
    # update the pixels with brightness frame
    NUM_PIXELS = len(self.pixels)
    self.pixels.fill((0, 0, 0))

    for headLoc, color, _, movingUp in self.streamers:
      frame = brightnessFrame(color, self.streamersLen)
      for i in range(len(frame)):
        if movingUp:
          loc = (headLoc + i) % NUM_PIXELS
        else:
          loc = (headLoc - i) % NUM_PIXELS
        self.pixels[loc] = frame[i]
    self.t += 1
