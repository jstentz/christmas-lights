"""
Campfire animation - makes the tree look like a flickering fire.
"""
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D
from typing import Optional
import numpy as np


class Campfire(BaseAnimation):
    """
    Animated campfire effect with flickering flames rising upward.
    """

    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 30) -> None:
        super().__init__(frameBuf, fps=fps)
        self.time = 0.0
        self.num_pixels = len(frameBuf)

        # Normalize Z coordinates to 0-1 range for height-based effects
        self.z_coords = POINTS_3D[:, 2].copy()
        self.z_min = self.z_coords.min()
        self.z_max = self.z_coords.max()
        self.z_normalized = (self.z_coords - self.z_min) / (self.z_max - self.z_min)

        # Get radial distance from center for ember effects
        self.radial_dist = np.sqrt(POINTS_3D[:, 0]**2 + POINTS_3D[:, 1]**2)
        self.radial_normalized = self.radial_dist / self.radial_dist.max()

        # Get angular position for spiral effect
        self.angle = np.arctan2(POINTS_3D[:, 1], POINTS_3D[:, 0])

        # Pre-compute random phase offsets for each pixel (for varied flickering)
        self.phase_offsets = np.random.uniform(0, 2 * np.pi, self.num_pixels)
        self.flicker_speeds = np.random.uniform(0.8, 1.2, self.num_pixels)

    def renderNextFrame(self) -> None:
        """
        Render a campfire frame with flickering flames.
        """
        self.time += 1.0 / (self.fps or 30)

        for i in range(self.num_pixels):
            height = self.z_normalized[i]
            radial = self.radial_normalized[i]
            angle = self.angle[i]

            # Create flickering effect using multiple sine waves (slowed down)
            flicker = (
                0.3 * np.sin(self.time * 2.5 * self.flicker_speeds[i] + self.phase_offsets[i]) +
                0.2 * np.sin(self.time * 4 * self.flicker_speeds[i] + self.phase_offsets[i] * 1.3) +
                0.15 * np.sin(self.time * 6 + self.phase_offsets[i] * 0.7) +
                0.1 * np.sin(self.time * 10 + height * 10)
            )

            # Rising flame effect - flames move upward over time (slowed down)
            rising = np.sin(self.time * 1.0 - height * 8 + self.phase_offsets[i]) * 0.3

            # Spiral flame effect - flames twist as they rise
            # Combines angle with height and time for rotating spiral
            spiral = 0.5 + 0.5 * np.sin(angle * 2 - self.time * 1.5 + height * 6)

            # Heat shimmer - waves of brightness rippling upward
            shimmer = 0.9 + 0.1 * np.sin(self.time * 3 - height * 12 + angle * 0.5)

            # Combined animation value - drives color variation
            anim = flicker + rising + (spiral - 0.5) * 0.5 + (shimmer - 0.9) * 2

            # Normalize to 0-1 range (anim roughly ranges from -1 to 1)
            anim_normalized = (anim + 1.2) / 2.4
            anim_normalized = max(0.0, min(1.0, anim_normalized))

            # Height-based color gradient
            # Bottom: brown logs
            # Lower: deep red/orange (coals)
            # Middle: bright orange (main flames)
            # Top: yellow flame tips

            # Animation affects both brightness and color shift
            # anim_normalized 0 = darker/redder, 1 = brighter/yellower
            brightness = 0.2 + 0.8 * anim_normalized  # 20% to 100% (more drastic dimming)

            if height < 0.08:
                # Log region - dark brown with ember glow
                log_pulse = 0.3 + 0.7 * anim_normalized  # More drastic dimming (30% to 100%)
                r = int(np.clip(140 * log_pulse, 0, 255))
                g = int(np.clip(50 * log_pulse, 0, 255))
                b = int(np.clip(10 * log_pulse, 0, 255))
            elif height < 0.22:
                # Ember/coal region - shifts between deep red and orange
                # Occasional blue ember pulse
                blue_pulse = np.sin(self.time * 1.5 + self.phase_offsets[i] * 3)
                if blue_pulse > 0.85:
                    # Blue ember moment
                    pulse_strength = (blue_pulse - 0.85) / 0.15  # 0 to 1
                    r = int(np.clip(80 + 50 * (1 - pulse_strength), 0, 255))
                    g = int(np.clip(100 + 80 * pulse_strength, 0, 255))
                    b = int(np.clip(200 + 55 * pulse_strength, 0, 255))
                else:
                    # Normal red/orange ember
                    base_g = 20 + 60 * anim_normalized  # 20-80 green based on animation
                    r = int(np.clip(255 * brightness, 0, 255))
                    g = int(np.clip(base_g * brightness, 0, 255))
                    b = int(np.clip(0, 0, 255))
            elif height < 0.50:
                # Main flame region - shifts between red-orange and yellow-orange
                flame_pos = (height - 0.22) / 0.28
                base_g = 40 + 80 * flame_pos + 60 * anim_normalized  # animation adds yellow
                r = int(np.clip(255 * brightness, 0, 255))
                g = int(np.clip(base_g * brightness, 0, 255))
                b = int(np.clip(0, 0, 255))
            else:
                # Flame tips - shifts between orange and bright yellow
                tip_pos = (height - 0.50) / 0.50
                base_g = 120 + 60 * tip_pos + 75 * anim_normalized  # animation adds brightness
                r = int(np.clip(255 * brightness, 0, 255))
                g = int(np.clip(min(255, base_g) * brightness, 0, 255))
                b = int(np.clip(0, 0, 255))

            # Add random blue sparks occasionally (very rare, top third only)
            if height > 0.67 and np.random.random() < 0.0002:
                spark_intensity = np.random.uniform(0.7, 1.0)
                r = int(np.random.uniform(80, 150) * spark_intensity)
                g = int(np.random.uniform(150, 220) * spark_intensity)
                b = int(255 * spark_intensity)

            self.frameBuf[i] = [r, g, b]