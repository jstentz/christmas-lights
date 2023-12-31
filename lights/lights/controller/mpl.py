from typing import Dict
from lights.controller.base import BaseController
import numpy as np
from lights.utils.geometry import POINTS_3D

class MatplotlibController(BaseController):

  def __init__(self, animation: str, animation_kwargs: Dict, n_pixels: int):
    super().__init__(animation, animation_kwargs, n_pixels)
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    screencolor = 'black'
    self.fig = plt.figure(figsize=(10, 10), facecolor=screencolor)
    self.ax = self.fig.add_subplot(111, projection=Axes3D.name)
    self.ax.set_facecolor(screencolor)
    self.points = POINTS_3D
    self.sizes = 100 * np.ones(n_pixels)
    self.scatter = self.ax.scatter(self.points[:, 0], self.points[:, 1], self.points[:, 2], c=self.frameBuf / 255, s=self.sizes, marker='o', edgecolors=None, alpha=0.4)

  def run(self):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    self.ani = FuncAnimation(self.fig, self.update, interval=self.animation.period * 1000, frames=None, cache_frame_data=False)
    plt.grid(False)
    plt.axis('off')
    plt.show()

  def record(self, duration, output):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    period = self.animation.period if self.animation.period != 0 else 1/60
    self.ani = FuncAnimation(self.fig, self.update, interval=self.animation.period * 1000, frames=int(duration / period), cache_frame_data=False)
    self.ax.set_autoscale_on(True)
    self.fig.set_size_inches(4.2, 3.15)
    self.scatter.set_sizes(20 * np.ones(len(self.points)))
    #self.ax.set_zlim(-1, 1)
    self.ax.set_box_aspect((1, 1, 1), zoom=1.5)
    plt.grid(False)
    plt.axis('off')
    self.ani.save(output)

  def update(self, frame):
    self.animation.renderNextFrame()
    self.scatter.set_color(self.frameBuf / 255)
