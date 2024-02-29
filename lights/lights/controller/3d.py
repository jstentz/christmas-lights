from typing import Dict
from lights.controller.base import BaseController
import numpy as np
from lights.utils.geometry import POINTS_3D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class MatplotlibController(BaseController):

  def __init__(self, animation: str, animation_kwargs: Dict, n_pixels: int, validate_parameters=True):
    super().__init__(animation, animation_kwargs, n_pixels, validate_parameters=validate_parameters)
    screencolor = 'black'
    self.fig = plt.figure(figsize=(10, 10), facecolor=screencolor)
    self.ax = self.fig.add_subplot(111, projection='3d')
    self.ax.set_facecolor(screencolor)
    self.points = POINTS_3D
    self.sizes = 100 * np.ones(n_pixels)
    self.scatter = self.ax.scatter(self.points[:, 0], self.points[:, 1], self.points[:, 2], c=self.frameBuf / 255, s=self.sizes, marker='o', edgecolors=None, alpha=0.4)

  def run(self):
    self.ani = FuncAnimation(self.fig, self.update, interval=self.animation.period * 1000, frames=None, cache_frame_data=False)
    plt.grid(False)
    plt.axis('off')
    plt.show()

  def update(self, frame):
    self.animation.renderNextFrame()
    self.scatter.set_color(self.frameBuf / 255)
