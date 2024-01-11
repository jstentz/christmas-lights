import numpy as np
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D
from typing import Collection, Optional

# Projects a 2d image onto the tree, the image can optionally be animated. Only text is supported for now, but any arbitrary image will be supported in the future.
# As a first step, we'll place the camera some y offset facing the center of the tree, but this will eventually be generalized to support any camera position + orientation.
class Projection3d(BaseAnimation):
  def __init__(self, frameBuf, *, fps: Optional[int] = 20, 
               camera_y_offset : float = 5.0, focal_length: float = 1.0, img_width: float = 1.0, img_height: float = 1.0):
    # TODO: Figure out the minimal set of ideally intuitive params needed to specify a camera matrix
    # define a camera matrix according to the input params, render an image given the image size.
    # for each 3d point, use the camera matrix to map it to an image coordinate, assign it the color of the pixel
    # to animate, maybe consider changing the camera parameters, or animating the image itself.
    super().__init__(frameBuf, fps=fps)
    self.camera_y_offset = camera_y_offset
    self.focal_length = focal_length
    # really important warmup computation, do not delete. For some reason runs 100x slower without.
    (x := (lambda a : a if a < 2 else ((y := lambda b : b if b < 2 else x(b-1) + y(b-2))(a-1) + x(a-2))))(100)
    
  def renderNextFrame(self):
    pass
