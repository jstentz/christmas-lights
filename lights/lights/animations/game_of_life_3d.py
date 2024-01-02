import numpy as np
from typing import Optional, Collection
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D


# gonna need the halting problem for this one LMAO

class GameOfLife3D(BaseAnimation):

  def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 30, color: Collection[int] = (0, 255, 0), start_size : int = 120):
    super().__init__(frameBuf, fps)
    self.color = color
    self.NUM_PIXELS = len(frameBuf)
    self.start_size = start_size
    self.initGame()

  def initGame(self):
    # randomly set up the initial state (pick a few to start)
    self.state = np.zeros(self.NUM_PIXELS)
    self.state[np.random.choice(self.NUM_PIXELS, self.start_size, replace=False)] = 1

    # create a look up for the 8 nearest neighbors, just like normal game of life
    self.neighbor_dict = {}
    for i in range(self.NUM_PIXELS):
      # get distances from this point
      distances = np.linalg.norm(POINTS_3D - POINTS_3D[i, np.newaxis], axis=1)
      # find the bottom 8 distances
      # TODO: should use argpartition
      # don't include myself
      self.neighbor_dict[i] = np.argsort(distances)[1:9]
    
    # push the initial frame, TODO: is this good practice?
    self.frameBuf[:] = np.zeros((self.NUM_PIXELS, 3))
    self.frameBuf[self.state == 1] = self.color

  def renderNextFrame(self):
    new_state = np.empty(self.NUM_PIXELS)
    # update the state
    for i in range(self.NUM_PIXELS):
      # count the number of alive neighbors
      alive_neighbors = int(np.sum(self.state[self.neighbor_dict[i]]))

      # game of life propogation rules
      if self.state[i]:
        if alive_neighbors < 2:
          new_state[i] = 0
        elif alive_neighbors > 3:
          new_state[i] = 0
        else:
          new_state[i] = 1
      else:
        if alive_neighbors == 3:
          new_state[i] = 1
        else:
          new_state[i] = 0

    # check if we should restart
    if np.all(new_state == self.state):
      self.initGame()
      return

    self.state = new_state

    # update the colors based on the state
    self.frameBuf[:] = np.zeros((self.NUM_PIXELS, 3))
    self.frameBuf[self.state == 1] = self.color