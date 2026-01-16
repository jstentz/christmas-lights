from lights.animations.base import BaseAnimation
from typing import Optional
import numpy as np
from lights.utils.geometry import POINTS_3D

'''
Hi Tara! Happy Holidays & New Years-- thank u for all your videos!
below is my candy cane animation :D
'''

class CompCandyCane(BaseAnimation):
    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60, twist: float = 2.0, rotation_speed: float = 0.067, fall_speed: float = 0.05, ring_thickness: float = 0.005, decay: float = 0.9, flash_frames: int = 20) -> None:
        super().__init__(frameBuf, fps=fps)

        # geom
        min_pt = np.min(POINTS_3D, axis=0)
        max_pt = np.max(POINTS_3D, axis=0)
        center = (min_pt + max_pt) / 2
        pts = POINTS_3D - center

        self.x = pts[:, 0]
        self.y = pts[:, 1]
        self.z = pts[:, 2]

        self.y_min = self.y.min()
        self.y_max = self.y.max()
        self.y_norm = (self.y - self.y_min) / (self.y_max - self.y_min)

        self.radius = np.sqrt(self.x**2 + self.z**2)
        self.max_radius = np.max(self.radius)
        self.angle = np.arctan2(self.z, self.x)

        # params
        self.twist = twist
        self.rotation_speed = rotation_speed
        self.decay = decay
        self.flash_frames = flash_frames

        self.fall_speed = fall_speed * (self.y_max - self.y_min)
        self.ring_thickness = ring_thickness * (self.y_max - self.y_min)

        # states
        self.phase = 0 # 0 = build, 1 = flash, 2 = spin
        self.build_front_y = self.y_max
        self.flash_count = 0
        self.t = 0.0

        # colors
        self.red = np.array([255, 0, 0])
        self.white = np.array([255, 255, 255])


    def candy_cane_colors(self, phase):
        stripe = np.sign(np.sin(phase))
        colors = np.zeros((len(stripe), 3))
        colors[stripe > 0] = self.red
        colors[stripe <= 0] = self.white
        return colors

    def renderNextFrame(self) -> None:
        """
        Called every frame. Update self.frameBuf with RGB values (0-255).
        frameBuf is a numpy array of shape (NUM_PIXELS, 3).
        """
        self.frameBuf[:] = self.frameBuf.astype(np.float64) * self.decay

        # true cone coords
        safe_radius = np.maximum(self.radius, 0.05 * self.max_radius)
        cone_angle = self.angle * (self.max_radius / safe_radius)

        base_phase = (
            cone_angle
            + self.y_norm * self.twist * 2 * np.pi
        )

        colors = self.candy_cane_colors(base_phase)

        # 0. fading render
        if self.phase == 0:
            settled = self.y <= self.build_front_y
            self.frameBuf[settled] = colors[settled]

            ring = np.abs(self.y - self.build_front_y) < self.ring_thickness
            self.frameBuf[ring] = colors[ring]

            self.build_front_y -= self.fall_speed

            if self.build_front_y <= self.y_min:
                self.phase = 1
                self.flash_count = 0

        # 2. flash!
        elif self.phase == 1:
            self.frameBuf[:] = self.white if (self.flash_count // 5) % 2 == 0 else self.red
            self.flash_count += 1
            if self.flash_count >= self.flash_frames:
                self.phase = 2

        # 3. candy cane spin
        else:
            phase = base_phase + self.t
            self.frameBuf[:] = self.candy_cane_colors(phase)
            self.t += self.rotation_speed