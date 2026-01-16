# animation.py
from __future__ import annotations

import numpy as np
from typing import Optional, Dict, Any, List

from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D
from lights.utils.colors import hsv_to_rgb


def clamp255(x: np.ndarray) -> np.ndarray:
    return np.clip(x, 0.0, 255.0)


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    # Smooth interpolation from 0 to 1 as x goes edge0->edge1
    t = np.clip((x - edge0) / (edge1 - edge0 + 1e-9), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def exp_falloff(x: np.ndarray, k: float) -> np.ndarray:
    return np.exp(-k * np.clip(x, 0.0, None))


def tonemap_reinhard(rgb: np.ndarray) -> np.ndarray:
    """
    Very lightweight tonemapping to reduce harsh clipping while
    preserving bright pops.
    Assumes rgb is in linear-ish space (0..inf), returns 0..1-ish.
    """
    return rgb / (1.0 + rgb)


class Fireworks(BaseAnimation):
    """
    Firework Tree (Launch + Explosion)

    Each burst:
      1) Launch: a bright "rocket" travels upward with a trailing tail
      2) Explosion: expanding shell ring with twinkling sparks

    Parameters are tuned to look good on a real tree (avoid over-saturation
    and keep motion readable).
    """

    def __init__(
        self,
        frameBuf,
        *,
        fps: Optional[int] = 30,
        burst_rate: float = 0.9,          # bursts per second
        brightness: float = 1.6,          # overall gain after tonemap
        launch_seconds: float = 0.70,     # rocket travel time
        explode_seconds: float = 1.30,    # shell visible time
        shell_speed: float = 1.15,        # radius expansion per second (tree units)
        shell_thickness: float = 0.08,    # ring thickness (tree units)
        trail_length: float = 0.28,       # trail length (tree units)
        trail_softness: float = 0.10,     # makes trail bloom softer
        twinkle_strength: float = 0.65,   # sparkle modulation depth
        twinkle_rate: float = 10.0,       # sparkle speed
        background_black: bool = True,    # keep background truly black
        seed: Optional[int] = None,       # deterministic runs if set
    ):
        super().__init__(frameBuf, fps=fps)

        if seed is not None:
            np.random.seed(seed)

        self.fps = fps if fps is not None else 30
        self.dt = 1.0 / float(self.fps)

        self.burst_rate = float(burst_rate)
        self.brightness = float(brightness)

        self.launch_seconds = float(launch_seconds)
        self.explode_seconds = float(explode_seconds)
        self.shell_speed = float(shell_speed)
        self.shell_thickness = float(shell_thickness)

        self.trail_length = float(trail_length)
        self.trail_softness = float(trail_softness)

        self.twinkle_strength = float(twinkle_strength)
        self.twinkle_rate = float(twinkle_rate)

        self.background_black = bool(background_black)

        pts = POINTS_3D.astype(np.float32)
        mid = (pts.min(axis=0) + pts.max(axis=0)) / 2.0
        self.P = pts - mid
        self.N = self.P.shape[0]

        # Tree extents in centered coordinates
        self.y_min = float(self.P[:, 1].min())
        self.y_max = float(self.P[:, 1].max())

        # Active bursts
        self.active: List[Dict[str, Any]] = []

        # Pre-spawn one burst so frame 1 isn't empty
        self._spawn_burst(initial=True)

        self.frame = 0

    def _spawn_burst(self, initial: bool = False) -> None:
        """
        Spawn a new burst. Rocket starts near the lower third,
        rises to an apex, then explodes.
        """
        # Small x/z offsets so it doesn't always explode in the exact center
        x = np.random.uniform(-0.20, 0.20)
        z = np.random.uniform(-0.20, 0.20)

        # Start lower; apex higher
        start_y = np.random.uniform(self.y_min * 0.85, self.y_min * 0.35)
        apex_y = np.random.uniform(self.y_max * 0.35, self.y_max * 0.85)

        # Color: pick a base hue per burst, with slight “temperature” shift
        base_h = np.random.rand()
        sat = np.random.uniform(0.85, 1.0)
        val = np.random.uniform(0.90, 1.0)

        # Twinkle phase randomness
        tw_phase = np.random.uniform(0.0, 2.0 * np.pi)
        tw_seed = np.random.uniform(0.5, 3.0)

        burst = {
            "t": 0.0,
            "x": float(x),
            "z": float(z),
            "start_y": float(start_y),
            "apex_y": float(apex_y),
            "base_h": float(base_h),
            "sat": float(sat),
            "val": float(val),
            "tw_phase": float(tw_phase),
            "tw_seed": float(tw_seed),
            # Give the initial burst a slightly bigger “wow” so it reads immediately
            "boost": 1.25 if initial else 1.0,
        }
        self.active.append(burst)

    def _burst_color_rgb01(self, burst: Dict[str, Any], t: float) -> np.ndarray:
        """
        Stable burst hue with subtle time drift for richness,
        but not so much that it looks like random color cycling.
        """
        base_h = burst["base_h"]
        # gentle drift; keep in [0,1)
        h = (base_h + 0.03 * np.sin(2.0 * np.pi * (0.35 * t))) % 1.0
        s = burst["sat"]
        v = burst["val"]
        return np.array(hsv_to_rgb(h, s, v), dtype=np.float32)

    def renderNextFrame(self):
        self.frame += 1

        # Start with black unless the controller sets a background
        out = np.zeros((self.N, 3), dtype=np.float32) if self.background_black else self.frameBuf.astype(np.float32) / 255.0

        # Spawn probability per frame
        if np.random.rand() < (self.burst_rate * self.dt):
            self._spawn_burst()

        alive: List[Dict[str, Any]] = []

        for b in self.active:
            b["t"] += self.dt
            t = float(b["t"])

            x = b["x"]
            z = b["z"]

            # Phase split
            if t < self.launch_seconds:
                # -------------------
                # 1) LAUNCH (rocket)
                # -------------------
                # progress 0..1
                u = t / self.launch_seconds
                # Ease-in-out travel
                u_eased = smoothstep(0.0, 1.0, np.array(u, dtype=np.float32)).item()

                y = b["start_y"] + (b["apex_y"] - b["start_y"]) * u_eased
                rocket_pos = np.array([x, y, z], dtype=np.float32)

                # Rocket "head": bright point
                d_head = np.linalg.norm(self.P - rocket_pos, axis=1)
                head = exp_falloff(d_head, k=18.0)  # tight bright head

                # Trail: distance to rocket path (approx as distance to rocket,
                # but weighted to create a tail behind it)
                # Define a "trail center" slightly below rocket along y
                trail_center = np.array([x, y - self.trail_length * 0.55, z], dtype=np.float32)
                d_trail = np.linalg.norm(self.P - trail_center, axis=1)

                # Softer bloom tail
                trail = exp_falloff(d_trail, k=6.0) * smoothstep(self.trail_length, 0.0, d_trail)

                # Fade-in then slight fade as it nears apex
                launch_bright = (0.55 + 0.65 * np.sin(np.pi * u))  # strong mid-flight
                launch_bright *= b["boost"]

                rgb = self._burst_color_rgb01(b, t)
                # Launch is whiter-hot at the core
                hot = np.array([1.0, 1.0, 1.0], dtype=np.float32)
                rgb_head = 0.55 * hot + 0.45 * rgb

                out += (head[:, None] * rgb_head[None, :] * 2.2 + trail[:, None] * rgb[None, :] * (1.4 + self.trail_softness)) * launch_bright

                alive.append(b)
                continue

            # -----------------------
            # 2) EXPLOSION (shell)
            # -----------------------
            te = t - self.launch_seconds
            if te < self.explode_seconds:
                origin = np.array([x, b["apex_y"], z], dtype=np.float32)

                r = np.linalg.norm(self.P - origin, axis=1)
                shell_radius = te * self.shell_speed

                # Ring/shell intensity: bright when r ~ shell_radius
                band = np.abs(r - shell_radius)
                ring = smoothstep(self.shell_thickness, 0.0, band)

                # Fade curve: quick bloom, slower decay
                bloom = smoothstep(0.0, 0.18, np.array(te, dtype=np.float32)).item()
                decay = np.exp(-te * 1.35)

                rgb = self._burst_color_rgb01(b, te)

                # Twinkle: spatially varied sparkle
                # Use dot with a fixed vector to create per-pixel phase variety
                phase = (self.P[:, 0] * 7.3 + self.P[:, 1] * 11.1 + self.P[:, 2] * 5.7) * b["tw_seed"]
                tw = 0.5 + 0.5 * np.sin(self.twinkle_rate * te + phase + b["tw_phase"])
                tw = (1.0 - self.twinkle_strength) + self.twinkle_strength * tw

                # Add a small "core flash" early in explosion
                core = exp_falloff(r, k=8.0) * smoothstep(0.20, 0.0, np.array(te, dtype=np.float32)).item()

                intensity = b["boost"] * bloom * decay
                out += (ring[:, None] * (rgb[None, :] * 2.3) * tw[:, None] + core[:, None] * 1.6) * intensity

                alive.append(b)

        self.active = alive

        # Tonemap + brightness gain, then convert to 0..255
        out = tonemap_reinhard(out) * self.brightness
        self.frameBuf[:] = clamp255(out * 255.0)