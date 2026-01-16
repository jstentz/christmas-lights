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
    Lightweight tonemapping to reduce harsh clipping while preserving bright pops.
    Assumes rgb is in linear-ish space (0..inf), returns ~0..1.
    """
    return rgb / (1.0 + rgb)


class FireworksAgain(BaseAnimation):
    """
    Firework Tree (Launch + Explosion)

    Change in this version: remove/shorten perceived "pauses" by making burst spawning
    time-scheduled (not random per-frame), enforcing a minimum number of active bursts,
    and overlapping bursts so the tree rarely goes dark between sequences.
    """

    def __init__(
        self,
        frameBuf,
        *,
        fps: Optional[int] = 30,
        burst_rate: float = 1.15,          # bursts per second (slightly higher than before)
        brightness: float = 1.6,           # overall gain after tonemap

        launch_seconds: float = 0.70,      # rocket travel time
        explode_seconds: float = 1.30,     # shell visible time

        shell_speed: float = 1.15,         # radius expansion per second (tree units)
        shell_thickness: float = 0.08,     # ring thickness (tree units)

        trail_length: float = 0.28,        # trail length (tree units)
        trail_softness: float = 0.10,      # makes trail bloom softer

        twinkle_strength: float = 0.65,    # sparkle modulation depth
        twinkle_rate: float = 10.0,        # sparkle speed

        # --- Anti-pause controls ---
        min_active_bursts: int = 1,        # guarantees something is always happening
        spawn_jitter: float = 0.18,        # 0..~0.3 is good; adds natural variation without gaps
        overlap_seconds: float = 0.35,     # spawn next burst this many seconds earlier than strict rate
        initial_preheat: float = 0.22,     # start first burst already "in motion" to avoid empty-looking first frames

        background_black: bool = True,     # keep background truly black
        seed: Optional[int] = None,        # deterministic runs if set
    ):
        super().__init__(frameBuf, fps=fps)

        if seed is not None:
            np.random.seed(seed)

        self.fps = fps if fps is not None else 30
        self.dt = 1.0 / float(self.fps)

        self.burst_rate = max(0.05, float(burst_rate))
        self.brightness = float(brightness)

        self.launch_seconds = float(launch_seconds)
        self.explode_seconds = float(explode_seconds)
        self.shell_speed = float(shell_speed)
        self.shell_thickness = float(shell_thickness)

        self.trail_length = float(trail_length)
        self.trail_softness = float(trail_softness)

        self.twinkle_strength = float(twinkle_strength)
        self.twinkle_rate = float(twinkle_rate)

        self.min_active_bursts = max(0, int(min_active_bursts))
        self.spawn_jitter = float(np.clip(spawn_jitter, 0.0, 0.9))
        self.overlap_seconds = max(0.0, float(overlap_seconds))
        self.initial_preheat = float(np.clip(initial_preheat, 0.0, 0.9))

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

        # Time + deterministic spawn scheduling (prevents random "dead air")
        self.t_global = 0.0
        self.next_spawn_t = 0.0

        # Pre-spawn one burst so frame 1 isn't empty-looking, and "preheat" it.
        self._spawn_burst(initial=True)
        self.active[-1]["t"] = self.launch_seconds * self.initial_preheat

        # Schedule the next burst promptly (with overlap) so we don’t dip to black.
        self._schedule_next_spawn(now=0.0, immediate=False)

        self.frame = 0

    def _schedule_next_spawn(self, now: float, *, immediate: bool) -> None:
        """
        Schedule next burst with slight jitter and overlap so bursts "chain" smoothly.
        """
        interval = 1.0 / self.burst_rate

        if immediate:
            self.next_spawn_t = now
            return

        # Pull the next burst earlier by overlap_seconds to reduce mid-sequence darkness.
        base = max(0.02, interval - self.overlap_seconds)

        # Apply jitter without allowing it to create long gaps.
        j = (np.random.rand() * 2.0 - 1.0) * (self.spawn_jitter * interval)
        dt_next = max(0.02, base + j)

        self.next_spawn_t = now + dt_next

    def _spawn_burst(self, initial: bool = False) -> None:
        """
        Spawn a new burst. Rocket starts near the lower third, rises to an apex, then explodes.
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
        h = (base_h + 0.03 * np.sin(2.0 * np.pi * (0.35 * t))) % 1.0
        s = burst["sat"]
        v = burst["val"]
        return np.array(hsv_to_rgb(h, s, v), dtype=np.float32)

    def renderNextFrame(self):
        self.frame += 1
        self.t_global += self.dt

        # Start with black unless the controller sets a background
        out = (
            np.zeros((self.N, 3), dtype=np.float32)
            if self.background_black
            else self.frameBuf.astype(np.float32) / 255.0
        )

        # Time-scheduled spawning (prevents random long gaps).
        # Spawn as many as needed if we somehow fall behind.
        while self.t_global >= self.next_spawn_t:
            self._spawn_burst()
            self._schedule_next_spawn(now=self.t_global, immediate=False)

        # Enforce a minimum number of active bursts (removes “middle/end” dead air).
        # If a burst ends and RNG would have delayed the next one, this keeps it alive.
        while len(self.active) < self.min_active_bursts:
            self._spawn_burst()
            # After forced spawn, schedule the next normally (don’t chain too aggressively)
            self._schedule_next_spawn(now=self.t_global, immediate=False)

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
                u = t / self.launch_seconds
                u_eased = smoothstep(0.0, 1.0, np.array(u, dtype=np.float32)).item()

                y = b["start_y"] + (b["apex_y"] - b["start_y"]) * u_eased
                rocket_pos = np.array([x, y, z], dtype=np.float32)

                d_head = np.linalg.norm(self.P - rocket_pos, axis=1)
                head = exp_falloff(d_head, k=18.0)

                trail_center = np.array([x, y - self.trail_length * 0.55, z], dtype=np.float32)
                d_trail = np.linalg.norm(self.P - trail_center, axis=1)
                trail = exp_falloff(d_trail, k=6.0) * smoothstep(self.trail_length, 0.0, d_trail)

                # Strong mid-flight, but keep the first frames visible (reduces “start pause” feel).
                launch_bright = (0.70 + 0.55 * np.sin(np.pi * u)) * b["boost"]

                rgb = self._burst_color_rgb01(b, t)
                hot = np.array([1.0, 1.0, 1.0], dtype=np.float32)
                rgb_head = 0.55 * hot + 0.45 * rgb

                out += (
                    (head[:, None] * rgb_head[None, :] * 2.2)
                    + (trail[:, None] * rgb[None, :] * (1.4 + self.trail_softness))
                ) * launch_bright

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

                band = np.abs(r - shell_radius)
                ring = smoothstep(self.shell_thickness, 0.0, band)

                # Fade curve: quick bloom, slower decay
                bloom = smoothstep(0.0, 0.18, np.array(te, dtype=np.float32)).item()
                decay = np.exp(-te * 1.35)

                rgb = self._burst_color_rgb01(b, te)

                phase = (self.P[:, 0] * 7.3 + self.P[:, 1] * 11.1 + self.P[:, 2] * 5.7) * b["tw_seed"]
                tw = 0.5 + 0.5 * np.sin(self.twinkle_rate * te + phase + b["tw_phase"])
                tw = (1.0 - self.twinkle_strength) + self.twinkle_strength * tw

                core = exp_falloff(r, k=8.0) * smoothstep(0.20, 0.0, np.array(te, dtype=np.float32)).item()

                intensity = b["boost"] * bloom * decay
                out += (ring[:, None] * (rgb[None, :] * 2.3) * tw[:, None] + core[:, None] * 1.6) * intensity

                alive.append(b)

        self.active = alive

        # Tonemap + brightness gain, then convert to 0..255
        out = tonemap_reinhard(out) * self.brightness
        self.frameBuf[:] = clamp255(out * 255.0)
