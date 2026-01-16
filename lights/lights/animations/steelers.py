"""
🏈 STEELERS GAME DAY - A Story in Lights 🏈
A multi-scene animation telling the story of a Steelers touchdown drive!

Scenes:
1. Black & Gold Stripes - Classic Steelers pattern
2. Logo Tribute - The red, yellow, blue hypocycloids
3. The Drive - Players rushing up the field with the football
4. TOUCHDOWN! - Celebration explosion cascading down the tree
"""

from lights.animations.base import BaseAnimation
from typing import Optional
import numpy as np
from lights.utils.geometry import POINTS_3D


class SteelersGameDay(BaseAnimation):
    """
    A cinematic Steelers animation with multiple scenes telling
    the story of a touchdown drive!
    """

    def __init__(
        self,
        frameBuf: np.ndarray,
        *,
        fps: Optional[int] = 60,
        scene_duration: int = 300,  # frames per scene (~5 sec at 60fps)
    ) -> None:
        super().__init__(frameBuf, fps=fps)

        self.scene_duration = scene_duration

        # ========== STEELERS COLORS ==========
        self.BLACK = np.array([0, 0, 0])
        self.GOLD = np.array([255, 182, 18])  # Official Steelers Gold
        self.BRIGHT_GOLD = np.array([255, 215, 0])  # Bright gold
        self.LIGHT_GOLD = np.array([255, 230, 100])  # Light gold (closer to white)
        self.PALE_GOLD = np.array([255, 245, 200])  # Very light gold (almost white)
        self.WHITE = np.array([255, 255, 255])

        # Logo hypocycloid colors (represent steel-making) - BRIGHTER
        self.LOGO_YELLOW = np.array([255, 220, 50])  # Brighter yellow (coal)
        self.LOGO_RED = np.array([255, 80, 50])  # Brighter red/orange (iron ore)
        self.LOGO_BLUE = np.array([80, 180, 255])  # Brighter blue (steel scrap)

        # Football color - brown/orange leather
        self.FOOTBALL = np.array([139, 69, 19])

        # Field and opponent colors
        self.FIELD_GREEN = np.array([34, 139, 34])  # Football field green
        self.OPPONENT_PURPLE = np.array([75, 0, 130])  # Darker purple for opposing team

        # ========== GEOMETRY SETUP ==========
        min_pt = np.min(POINTS_3D, axis=0)
        max_pt = np.max(POINTS_3D, axis=0)
        mid = (max_pt + min_pt) / 2
        self.centered = POINTS_3D - mid

        self.x = self.centered[:, 0]
        self.y = self.centered[:, 1]
        self.z = self.centered[:, 2]

        # Normalized height [0, 1] - this is our "field position"
        self.height = (self.z - np.min(self.z)) / (np.max(self.z) - np.min(self.z))

        # Angle around tree
        self.angle = np.arctan2(self.y, self.x)

        # Horizontal distance from center
        self.horiz_dist = np.sqrt(self.x**2 + self.y**2)
        self.max_horiz = np.max(self.horiz_dist)
        self.norm_horiz = self.horiz_dist / self.max_horiz

        # 3D distance
        self.dist_3d = np.linalg.norm(self.centered, axis=1)
        self.max_dist = np.max(self.dist_3d)

        # ========== SCENE STATE ==========
        self.t = 0
        self.current_scene = 0
        self.scene_t = 0  # Time within current scene

        # Random seeds for effects
        np.random.seed(42)
        self.twinkle_phase = np.random.rand(len(frameBuf)) * 2 * np.pi

        # Players for "The Drive" scene - 11 Steelers players + 11 opponents
        self.num_steelers = 11
        self.num_opponents = 11

        # Steelers players - spread around the tree at different angles
        np.random.seed(42)
        self.steelers_angles = np.random.rand(self.num_steelers) * 2 * np.pi

        # Opponents - also spread around, will start at top
        self.opponents_angles = np.random.rand(self.num_opponents) * 2 * np.pi

    def renderNextFrame(self) -> None:
        # Determine which scene we're in
        total_scenes = 4
        scene_frame = self.t % (self.scene_duration * total_scenes)
        self.current_scene = scene_frame // self.scene_duration
        self.scene_t = scene_frame % self.scene_duration

        # Clear to black
        self.frameBuf[:] = self.BLACK

        # Render current scene
        if self.current_scene == 0:
            self.render_stripes()
        elif self.current_scene == 1:
            self.render_logo_tribute()
        elif self.current_scene == 2:
            self.render_the_drive()
        elif self.current_scene == 3:
            self.render_touchdown()

        self.t += 1

    # ==========================================
    # SCENE 1: BLACK & GOLD STRIPES
    # Classic Steelers stripes rotating around the tree
    # ==========================================
    def render_stripes(self):
        # Rotating stripes based on angle + height
        num_stripes = 6
        rotation = self.scene_t * 0.03

        # Combine angle and height for diagonal stripes
        stripe_value = (self.angle / (2 * np.pi) + self.height * 2 + rotation) % 1.0

        # Create stripe pattern
        stripe_index = (stripe_value * num_stripes).astype(int) % 2

        # Gold stripes - use variations for vibrancy
        gold_stripes = stripe_index == 0

        # Vary gold intensity based on position for more depth
        stripe_variation = (stripe_value * num_stripes) % 1.0

        # Use different gold shades based on stripe position
        for i in range(len(self.frameBuf)):
            if gold_stripes[i]:
                var = stripe_variation[i]
                if var < 0.33:
                    self.frameBuf[i] = self.GOLD
                elif var < 0.66:
                    self.frameBuf[i] = self.BRIGHT_GOLD
                else:
                    self.frameBuf[i] = self.LIGHT_GOLD

        # Black stripes stay black (already cleared)

        # Add some twinkling gold highlights - use lighter golds
        twinkle = np.sin(self.twinkle_phase + self.scene_t * 0.15)
        bright_twinkle = (twinkle > 0.7) & gold_stripes
        self.frameBuf[bright_twinkle] = self.PALE_GOLD

        # Very bright sparkles
        super_bright = (twinkle > 0.9) & gold_stripes
        self.frameBuf[super_bright] = self.WHITE

        # Pulsing effect
        pulse = 0.7 + 0.3 * np.sin(self.scene_t * 0.1)
        self.frameBuf[:] = (self.frameBuf * pulse).astype(np.uint8)

    # ==========================================
    # SCENE 2: LOGO TRIBUTE
    # 3 small hypocycloid diamonds rotating around the tree
    # Like the Steelers logo - mostly black/gold with 3 colored accents
    # ==========================================
    def render_logo_tribute(self):
        # Start with dark gold/black background - use gold variations
        bg_intensity = 0.15 + 0.05 * np.sin(self.height * 2 * np.pi)
        bg_variation = np.sin(self.height * 3 * np.pi + self.scene_t * 0.05)

        # Vary gold shades in background
        for i in range(len(self.frameBuf)):
            var = bg_variation[i]
            if var < -0.3:
                base_color = self.GOLD
            elif var < 0.3:
                base_color = self.BRIGHT_GOLD
            else:
                base_color = self.LIGHT_GOLD
            self.frameBuf[i] = (base_color * bg_intensity[i]).astype(np.uint8)

        # Rotation around the tree - FASTER rotation for spiral effect
        rotation = np.pi + self.scene_t * 0.08  # Fast rotation speed

        # Spiral upward - height tied to time (goes up as it spins around)
        # Spirals from bottom to top during the scene
        spiral_progress = self.scene_t / self.scene_duration  # 0 to 1
        spiral_height_base = (
            0.1 + spiral_progress * 0.7
        )  # Spirals from 10% to 80% height

        # The 3 hypocycloids arranged vertically (like on the logo)
        # They spiral around and up the tree together
        hypocycloid_colors = [self.LOGO_YELLOW, self.LOGO_RED, self.LOGO_BLUE]
        # Stack vertically with fixed spacing, all spiraling up together
        hypocycloid_heights = [
            spiral_height_base + 0.12,  # Yellow - top
            spiral_height_base,  # Red - middle
            spiral_height_base - 0.12,  # Blue - bottom
        ]

        # Diamond size (small, like on the logo)
        diamond_height_size = 0.08
        diamond_angle_size = 0.3

        for i, (color, h_pos) in enumerate(
            zip(hypocycloid_colors, hypocycloid_heights)
        ):
            # Each diamond rotates around the tree
            diamond_angle = rotation + i * 0.1  # Slight offset between them

            # Twinkling/pulsing effect for each diamond - BRIGHTER
            twinkle = 0.8 + 0.2 * np.sin(self.scene_t * 0.15 + i * 2)

            # Find LEDs near this diamond position
            angle_diff = np.abs(
                np.arctan2(
                    np.sin(self.angle - diamond_angle),
                    np.cos(self.angle - diamond_angle),
                )
            )
            height_diff = np.abs(self.height - h_pos)

            # Diamond shape - LEDs within the diamond area
            in_diamond = (angle_diff < diamond_angle_size) & (
                height_diff < diamond_height_size
            )

            # Intensity based on distance from center of diamond (brighter in middle)
            if np.any(in_diamond):
                dist_from_center = np.sqrt(
                    (angle_diff[in_diamond] / diamond_angle_size) ** 2
                    + (height_diff[in_diamond] / diamond_height_size) ** 2
                )
                # Brighter overall - less fade, higher minimum
                intensity = (1.0 - dist_from_center * 0.5) * twinkle
                intensity = np.clip(intensity, 0.5, 1.0)  # Minimum 50% brightness

                self.frameBuf[in_diamond] = (color * intensity[:, np.newaxis]).astype(
                    np.uint8
                )

        # Add some gold sparkles in the background - use lighter golds
        sparkle = np.sin(self.twinkle_phase + self.scene_t * 0.1)
        gold_sparkle = sparkle > 0.85
        very_bright_sparkle = sparkle > 0.95

        # Regular sparkles use light gold
        self.frameBuf[gold_sparkle] = np.maximum(
            self.frameBuf[gold_sparkle], (self.LIGHT_GOLD * 0.8).astype(np.uint8)
        )

        # Very bright sparkles use pale gold/white
        self.frameBuf[very_bright_sparkle] = np.maximum(
            self.frameBuf[very_bright_sparkle], self.PALE_GOLD
        )

    # ==========================================
    # SCENE 3: THE DRIVE
    # Players driving up the field (tree) with football
    # ==========================================
    def render_the_drive(self):
        # Drive progress - starts at 0 (bottom), drives to 1 (top/endzone)
        drive_progress = self.scene_t / self.scene_duration  # 0 to 1

        # ===== GREEN FOOTBALL FIELD =====
        # All LEDs start as green (football field)
        self.frameBuf[:] = (self.FIELD_GREEN * 0.5).astype(np.uint8)

        # ===== HORIZONTAL BANDS MOVING UPWARD =====
        # Three horizontal rings wrapping around the tree, moving up together
        # Band thicknesses - Steelers are MORE prominent
        steelers_thickness = 0.09  # THICK - Steelers dominate!
        opponent_thickness = 0.04  # Thin - opponents are smaller
        football_thickness = 0.03  # Football is small

        # Base position moves from bottom (0.05) toward top (0.92) - reaches top for touchdown!
        base_position = 0.05 + drive_progress * 0.87

        # ===== FOOTBALL (BROWN) - Bottom band (SMALLER) =====
        football_height = base_position - 0.08  # Below Steelers
        football_dist = np.abs(self.height - football_height)
        in_football = football_dist < football_thickness

        if np.any(in_football):
            intensity = 1.0 - (football_dist[in_football] / football_thickness)
            intensity = np.clip(intensity, 0.6, 1.0)
            self.frameBuf[in_football] = (
                self.FOOTBALL * intensity[:, np.newaxis]
            ).astype(np.uint8)

        # ===== STEELERS (GOLD) - Middle band (pushing!) - PROMINENT! =====
        steelers_height = base_position
        steelers_dist = np.abs(self.height - steelers_height)
        in_steelers = steelers_dist < steelers_thickness  # Thicker band

        if np.any(in_steelers):
            intensity = 1.0 - (steelers_dist[in_steelers] / steelers_thickness) * 0.5
            intensity = np.clip(intensity, 0.6, 1.0)  # Higher minimum - brighter!
            self.frameBuf[in_steelers] = (
                self.BRIGHT_GOLD * intensity[:, np.newaxis]
            ).astype(np.uint8)

        # ===== OPPONENTS (PURPLE) - Top band (being pushed back!) - smaller/dimmer =====
        opponent_height = base_position + 0.10  # Above Steelers
        opponent_dist = np.abs(self.height - opponent_height)
        in_opponent = opponent_dist < opponent_thickness  # Thinner band

        if np.any(in_opponent):
            intensity = 1.0 - (opponent_dist[in_opponent] / opponent_thickness)
            intensity = np.clip(intensity, 0.3, 0.8)  # Dimmer - less prominent
            self.frameBuf[in_opponent] = (
                self.OPPONENT_PURPLE * intensity[:, np.newaxis]
            ).astype(np.uint8)

    # ==========================================
    # SCENE 4: TOUCHDOWN!!!
    # FIREWORKS first, then original celebration!
    # ==========================================
    def render_touchdown(self):
        progress = self.scene_t / self.scene_duration

        if progress < 0.1:
            # Initial flash - EVERYTHING GOLD, big explosion!
            flash_intensity = 1.0 - (progress / 0.1) * 0.5
            self.frameBuf[:] = (self.BRIGHT_GOLD * flash_intensity).astype(np.uint8)

            # Top of tree is WHITE hot - the touchdown spot!
            top_leds = self.height > 0.85
            self.frameBuf[top_leds] = self.WHITE

        elif progress < 0.70:
            # ===== FIREWORKS PHASE (LONGER!) =====
            # Black background with fireworks exploding
            self.frameBuf[:] = self.BLACK

            # Multiple firework explosions at different positions
            num_fireworks = 10  # More fireworks!
            firework_interval = 0.055  # Time between fireworks

            for fw_idx in range(num_fireworks):
                # Each firework starts at a different time
                fw_start = 0.1 + fw_idx * firework_interval
                fw_progress = progress - fw_start

                if fw_progress > 0 and fw_progress < 0.30:  # Each lasts longer
                    # Firework is active
                    # Random but deterministic position for this firework
                    np.random.seed(42 + fw_idx)
                    fw_x = np.random.uniform(-0.5, 0.5) * self.max_horiz
                    fw_y = np.random.uniform(-0.5, 0.5) * self.max_horiz
                    fw_z_norm = 0.2 + np.random.uniform(0, 0.6)  # Height 20%-80%
                    fw_z = fw_z_norm * (np.max(self.z) - np.min(self.z)) + np.min(
                        self.z
                    )

                    # Explosion expands outward
                    explosion_radius = fw_progress * 2.5 * self.max_dist
                    fade = 1.0 - (fw_progress / 0.30)  # Fades over time

                    # Distance from explosion center
                    dx = self.x - fw_x
                    dy = self.y - fw_y
                    dz = self.z - fw_z
                    dist_to_fw = np.sqrt(dx**2 + dy**2 + dz**2)

                    # Shell of the explosion (expanding ring)
                    shell_thickness = 0.12 * self.max_dist
                    in_shell = np.abs(dist_to_fw - explosion_radius) < shell_thickness

                    if np.any(in_shell):
                        shell_intensity = (
                            1.0
                            - np.abs(dist_to_fw[in_shell] - explosion_radius)
                            / shell_thickness
                        )
                        shell_intensity = shell_intensity * fade

                        # Alternate firework colors - gold and white
                        if fw_idx % 2 == 0:
                            fw_color = self.WHITE
                        else:
                            fw_color = self.BRIGHT_GOLD

                        new_color = (fw_color * shell_intensity[:, np.newaxis]).astype(
                            np.uint8
                        )
                        self.frameBuf[in_shell] = np.maximum(
                            self.frameBuf[in_shell], new_color
                        )

        else:
            # ===== ORIGINAL CELEBRATION (as before) =====
            celebration_progress = (
                progress - 0.70
            ) / 0.30  # 0 to 1 over remaining time

            # Initial flash for this phase
            if celebration_progress < 0.15:
                flash_intensity = 1.0 - (celebration_progress / 0.15) * 0.5
                self.frameBuf[:] = (self.BRIGHT_GOLD * flash_intensity).astype(np.uint8)
                top_leds = self.height > 0.85
                self.frameBuf[top_leds] = self.WHITE
            else:
                # Cascading sparkle wave going DOWN the tree
                wave_progress = (celebration_progress - 0.15) / 0.85
                wave_position = 1.0 - wave_progress  # Start at top, go to bottom

                wave_width = 0.15
                dist_from_wave = self.height - wave_position

                # Ahead of wave (already passed) - gold with sparkles
                ahead = dist_from_wave > wave_width
                ahead_indices = np.where(ahead)[0]
                for idx in ahead_indices:
                    var = np.sin(self.height[idx] * 4 * np.pi + self.scene_t * 0.1)
                    if var < -0.3:
                        self.frameBuf[idx] = (self.GOLD * 0.6).astype(np.uint8)
                    elif var < 0.3:
                        self.frameBuf[idx] = (self.BRIGHT_GOLD * 0.7).astype(np.uint8)
                    else:
                        self.frameBuf[idx] = (self.LIGHT_GOLD * 0.8).astype(np.uint8)

                # In the wave - BRIGHT
                in_wave = np.abs(dist_from_wave) < wave_width
                wave_intensity = 1.0 - np.abs(dist_from_wave[in_wave]) / wave_width
                self.frameBuf[in_wave] = (
                    self.WHITE * wave_intensity[:, np.newaxis]
                ).astype(np.uint8)

                # Behind wave (not yet reached) - black with anticipation sparkles
                behind = dist_from_wave < -wave_width
                anticipation = np.sin(self.twinkle_phase + self.scene_t * 0.5) > 0.9
                sparkle_behind = behind & anticipation
                self.frameBuf[sparkle_behind] = (self.GOLD * 0.5).astype(np.uint8)

                # Random celebration sparkles everywhere
                celebration = np.sin(self.twinkle_phase * 2 + self.scene_t * 0.4)
                confetti = celebration > 0.85

                confetti_color_select = np.random.rand(np.sum(confetti))
                confetti_indices = np.where(confetti)[0]

                for idx, color_val in zip(confetti_indices, confetti_color_select):
                    if color_val < 0.3:
                        self.frameBuf[idx] = self.WHITE
                    elif color_val < 0.5:
                        self.frameBuf[idx] = self.PALE_GOLD
                    elif color_val < 0.7:
                        self.frameBuf[idx] = self.LIGHT_GOLD
                    elif color_val < 0.85:
                        self.frameBuf[idx] = self.BRIGHT_GOLD
                    else:
                        self.frameBuf[idx] = self.GOLD

    @classmethod
    def validate_parameters(cls, parameters):
        super().validate_parameters(parameters)
        full_parameters = {**cls.get_default_parameters(), **parameters}

        if full_parameters["scene_duration"] <= 0:
            raise TypeError("scene_duration must be > 0")