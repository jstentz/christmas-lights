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
    self.fig = plt.figure(figsize=(10, 10))#, facecolor=screencolor)
    self.ax = self.fig.add_subplot(111, projection=Axes3D.name)
    # self.ax.set_facecolor(screencolor)
    self.points = POINTS_3D
    self.sizes = 100 * np.ones(n_pixels)
    self.scatter = self.ax.scatter(self.points[:, 0], self.points[:, 1], self.points[:, 2], c=self.frameBuf / 255, s=self.sizes, marker='o', edgecolors=None, alpha=0.4)

  def run(self):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    self.ani = FuncAnimation(self.fig, self.update, interval=self.animation.period * 1000, frames=None, cache_frame_data=False)
    self.ax.set_autoscale_on(True)
    self.fig.set_size_inches(4.2, 3.15)
    self.scatter.set_sizes(20 * np.ones(len(self.points)))
    self.ax.legend('')
    self.fig.tight_layout()
    #self.ax.set_zlim(-1, 1)
    # plt.grid(False)
    #plt.axis('off')
    plt.show()

  def record(self, duration, output):
    from matplotlib.animation import FuncAnimation
    period = self.animation.period if self.animation.period != 0 else 1/60
    self.ani = FuncAnimation(self.fig, self.update, interval=self.animation.period * 1000, frames=int(duration / period), cache_frame_data=False)
    #self.ax.set_autoscale_on(True)
    # self.ax.margins(0.0)
    self.fig.set_size_inches(4.2, 3.15)
    # self.ax.set_xlim(-0.75, 0.75)
    # self.ax.set_ylim(-0.75, 0.75)
    # self.ax.set_zlim(-0.75, 0.75)
    #self.ax.set_box_aspect([np.ptp(coord) for coord in [self.ax.get_xlim(), self.ax.get_ylim(), self.ax.get_zlim()]])
    self.scatter.set_sizes(20 * np.ones(len(self.points)))
    #self.ax.set_zlim(-1, 1)
    self.ax.set_box_aspect(None, zoom=1.5)
    # plt.grid(False)
    # plt.axis('off')
    self.fig.tight_layout()
    self.fig.subplots_adjust(0.0, 0.0, 1.0, 1.0, 0.0, 0.0)
    self.ax.set_position([0, 0, 1, 1])
    self.ani.save(output)

  def update(self, frame):
    self.animation.renderNextFrame()
    self.scatter.set_color(self.frameBuf / 255)
