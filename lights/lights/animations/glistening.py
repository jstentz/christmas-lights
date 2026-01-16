from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D
from typing import Optional
import numpy as np


def make_noise_volume(size=32, smooth_passes=2, seed=0):
    # Create a reproducible random generator
    rng = np.random.default_rng(seed)

    # Create a 3D grid (cube) of random values in [0,1]
    # Shape: (size, size, size)
    #
    # Think of this as a "block of fog" where every point in space
    # has a brightness value. We will sample inside this block later.
    vol = rng.random((size, size, size)).astype(np.float32)

    # Apply cheap smoothing to make the noise less harsh and more organic.
    # Each pass averages every voxel with its neighbors along X/Y/Z.
    for _ in range(smooth_passes):
        vol = (
            np.roll(vol, 1, 0) + vol + np.roll(vol, -1, 0) +
            np.roll(vol, 1, 1) + vol + np.roll(vol, -1, 1) +
            np.roll(vol, 1, 2) + vol + np.roll(vol, -1, 2)
        ) / 9.0

    return vol


def palette_blue_green(v):
    # v is an array of values in [0,1] representing brightness/intensity
    # We map that to a blue→cyan→green palette in a vectorized way.

    r = np.zeros_like(v)  # keep red at 0
    g = (60 + (255-60) * v).astype(np.uint8)
    b = (120 + (255-120) * v).astype(np.uint8)

    # Stack into RGB triplets: shape -> (N, 3)
    return np.stack([r, g, b], axis=1)


class Glistening(BaseAnimation):
    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 60,
                 grid_size=32) -> None:
        super().__init__(frameBuf, fps=fps)

        self.t = 0.0          # animated time parameter
        self.speed = 0.15     # how fast the field drifts
        self.scale = 0.6      # how "zoomed in" the noise appears

        # Size of the 3D noise cube
        self.grid_size = grid_size

        # ---- PRECOMPUTED NOISE VOLUME ----
        # Instead of calling noise per-pixel each frame, we build one
        # 3D grid of values that we will continuously sample from.
        self.vol = make_noise_volume(grid_size)

        # ---- MAP TREE COORDINATES INTO VOLUME SPACE ----
        #
        # POINTS_3D contains your real LED coordinates in tree space
        # (whatever units the model uses).
        #
        # We rescale them so that:
        #   min -> 0.0
        #   max -> 1.0
        #
        # That means the entire tree fits inside the unit cube [0,1]^3,
        # which aligns it with our noise volume coordinates.
        mins = POINTS_3D.min(axis=0)
        maxs = POINTS_3D.max(axis=0)
        rng = (maxs - mins)
        rng[rng == 0] = 1.0   # avoid divide-by-zero if flat on an axis

        # Normalized tree coordinates in "volume space"
        self.norm_points = (POINTS_3D - mins) / rng  # values in [0,1]

    def sample_volume(self, coords):
        """Vectorized trilinear interpolation from self.vol.

        coords is an array of normalized (x,y,z) values in [0,1]^3.
        For each LED, we look up the corresponding point inside the noise cube
        and interpolate smoothly between the 8 surrounding grid cells.
        """

        g = self.grid_size
        vol = self.vol

        # Wrap coordinates so motion loops cleanly.
        # (0.0 and 1.0 map to the same place)
        coords = (coords % 1.0) * (g - 1)

        # Integer cell index (lower corner)
        i0 = np.floor(coords).astype(int)

        # Fractional part inside the cell (0..1)
        f = coords - i0

        # Upper neighbor cell index (clamped to bounds)
        i1 = np.minimum(i0 + 1, g - 1)

        # Split columns for convenience
        x0, y0, z0 = i0.T
        x1, y1, z1 = i1.T
        fx, fy, fz = f.T

        # Fetch the 8 cube corners around each point
        c000 = vol[x0, y0, z0]
        c100 = vol[x1, y0, z0]
        c010 = vol[x0, y1, z0]
        c110 = vol[x1, y1, z0]
        c001 = vol[x0, y0, z1]
        c101 = vol[x1, y0, z1]
        c011 = vol[x0, y1, z1]
        c111 = vol[x1, y1, z1]

        # Interpolate along X
        c00 = c000*(1-fx) + c100*fx
        c10 = c010*(1-fx) + c110*fx
        c01 = c001*(1-fx) + c101*fx
        c11 = c011*(1-fx) + c111*fx

        # Interpolate along Y
        c0 = c00*(1-fy) + c10*fy
        c1 = c01*(1-fy) + c11*fy

        # Interpolate along Z → final value
        return c0*(1-fz) + c1*fz

    def renderNextFrame(self) -> None:
        # Build a drifting offset based on time.
        # This makes the sampling position slide through the noise volume,
        # creating the flowing / glistening motion.
        offset = np.array([
            np.sin(self.t*0.6),   # slow drift on X
            np.cos(self.t*0.4),   # slow drift on Y
            self.t                # steady forward motion in Z
        ], dtype=np.float32)

        # Combine:
        #   normalized LED positions
        #   + scale to zoom in/out of the noise
        #   + animated offset for motion
        coords = self.norm_points * self.scale + offset

        # Sample noise for all LEDs at once
        v = self.sample_volume(coords)

        # Add contrast and clamp to [0,1]
        v = np.clip(v ** 1.4, 0.0, 1.0)

        colors = palette_blue_green(v)
        self.frameBuf[:] = colors
        self.t += self.speed / self.fps