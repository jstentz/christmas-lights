import numpy as np
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D
from typing import Collection, Optional

class Streamers3D(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = 20, 
               num_streamers : int = 5, decay : float = 0.9, color : Collection[int] = (0, 255, 0), move_rad : float = 0.2):
    super().__init__(frameBuf, fps=fps)
    # None will mean pick random colors
    self.NUM_PIXELS = len(frameBuf)
    self.num_streamers = num_streamers
    self.decay = decay
    self.color = color

    # build up a nearest neighbors mapping (find all points within a radius)
    self.neighbor_dict = {}
    for i in range(self.NUM_PIXELS):
      # get distances from this point
      distances = np.linalg.norm(POINTS_3D - POINTS_3D[i, np.newaxis], axis=1)
      
      # find all points in the sphere that aren't myself
      # but only include 4 neighbors for now
      self.neighbor_dict[i] = np.where((distances < move_rad) & (np.arange(self.NUM_PIXELS) != i))[0][:4]

    # create the streamers
    self.streamers = np.random.choice(self.NUM_PIXELS, num_streamers, replace=False)

    
  def renderNextFrame(self):
    # decay all the pixels
    self.frameBuf[:] = (self.frameBuf * self.decay).astype(np.uint8)

    # move the streamers
    for i in range(len(self.streamers)):
      neighbors = self.neighbor_dict[self.streamers[i]]
      values = self.frameBuf[neighbors]
      valid_neighbors = neighbors[np.all(values == np.array([0, 0, 0]), axis=1)]
      self.streamers[i] = np.random.choice(valid_neighbors) if len(valid_neighbors) else np.random.choice(self.NUM_PIXELS)
      # brightnesses = np.linalg.norm(self.frameBuf[neighbors], axis=1)
      # if not np.sum(brightnesses):
      #   self.streamers[i] = np.random.choice(neighbors)
      # else:
      #   probabilities = (np.max(brightnesses) - brightnesses) / np.sum(np.max(brightnesses) - brightnesses)
      #   self.streamers[i] = np.random.choice(neighbors, p=probabilities)

    # light up the new head locations
    self.frameBuf[self.streamers] = np.array(self.color)
