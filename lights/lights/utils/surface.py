import numpy as np
import os

R1, R2, H = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'points/cone.npy'))


def draw_image(img: np.ndarray, frameBuf: np.ndarray, undistort: bool = False):
  """
  Draws a 2d image along the appoximate cone-like surface the tree.

  Parameters
  ----------
  img: (N, ?)
  frameBuf: (N, 3)
  undistort: bool
  """
  pass