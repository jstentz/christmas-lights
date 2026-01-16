"""
White light ball Christmas tree animation with consumption logic.
Lights start red, blue, or yellow. A white light ball moves around eating them.
At the end, all lights blink, turn off, and restart.
"""
import numpy as np
from typing import Optional
from lights.animations.base import BaseAnimation
from lights.utils.geometry import POINTS_3D

class Consumption(BaseAnimation):
    def __init__(
        self,
        frameBuf: np.ndarray,
        *,
        fps: Optional[int] = 60,
        speed: float = 0.02,
        radius: float = 0.14
    ) -> None:
        super().__init__(frameBuf, fps=fps)

        # Center the tree around origin for easier calculations
        min_pt = np.min(POINTS_3D, axis=0)
        max_pt = np.max(POINTS_3D, axis=0)
        center = (min_pt + max_pt) / 2
        self.POINTS = POINTS_3D - center

        self.speed = speed
        self.radius = radius

        # Base colors
        self.base_colors = np.array([
            [255, 0, 0],    # red
            [0, 0, 255],    # blue
            [255, 200, 0],  # yellow
        ], dtype=np.float64)

        self.reset()

    # -------------------------------------------------
    def reset(self):
        # Assign random base color to each LED (500 points)
        choices = np.random.randint(0, 3, size=len(self.POINTS))
        self.colors = self.base_colors[choices].copy()

        # Pellet states for all 500 LEDs
        self.uneaten = np.ones(len(self.POINTS), dtype=bool)

        # White ball starts at a random LED position
        start_idx = np.random.randint(len(self.POINTS))
        self.ball_pos = self.POINTS[start_idx].copy()
        
        self.target_idx = self.pick_target()

        # End animation state
        self.finish_timer = 0
        self.finishing = False

    # -------------------------------------------------
    def pick_target(self):
        """Pick next target from uneaten LEDs"""
        # Get indices of all uneaten LEDs
        remaining = np.where(self.uneaten)[0]
        if len(remaining) == 0:
            return None
        
        return np.random.choice(remaining)

    def move_towards(self, pos, target):
        """Move snake head towards target position, following tree surface"""
        direction = target - pos
        dist = np.linalg.norm(direction)
        
        if dist < self.speed:
            return target.copy()
        
        # Move along a path that stays near the tree surface
        # Get cylindrical coordinates (radius from Z-axis)
        pos_radius = np.sqrt(pos[0]**2 + pos[1]**2)
        target_radius = np.sqrt(target[0]**2 + target[1]**2)
        
        # If moving through center would be too direct, curve around the surface
        if pos_radius > 0.05 and target_radius > 0.05:
            # Calculate angles
            pos_angle = np.arctan2(pos[1], pos[0])
            target_angle = np.arctan2(target[1], target[0])
            
            # Find shortest angular distance
            angle_diff = target_angle - pos_angle
            if angle_diff > np.pi:
                angle_diff -= 2 * np.pi
            elif angle_diff < -np.pi:
                angle_diff += 2 * np.pi
            
            # Interpolate in cylindrical coordinates
            t = self.speed / dist
            t = min(t, 1.0)
            
            new_angle = pos_angle + angle_diff * t
            new_radius = pos_radius + (target_radius - pos_radius) * t
            new_z = pos[2] + (target[2] - pos[2]) * t
            
            new_pos = np.array([
                new_radius * np.cos(new_angle),
                new_radius * np.sin(new_angle),
                new_z
            ])
            return new_pos
        else:
            # Near center or poles, use direct movement
            return pos + (direction / dist) * self.speed

    def update_snake_occupied(self):
        """No longer needed - removed for ball version"""
        pass

    def get_leds_near_position(self, position):
        """Get LED indices near a given 3D position using distance calculation"""
        distances = np.linalg.norm(self.POINTS - position, axis=1)
        return np.where(distances < self.radius)[0]

    # -------------------------------------------------
    def renderNextFrame(self) -> None:
        # -------- Finish blinking --------
        if self.finishing:
            self.finish_timer += 1
            
            # Blink all lights with their original colors
            blink = (self.finish_timer // 15) % 2 == 0
            if blink:
                # Turn all lights on with their base colors
                self.frameBuf[:] = self.colors
            else:
                # Turn all lights off
                self.frameBuf[:] = 0

            # After 90 frames (~1.5 seconds), turn everything off and restart
            if self.finish_timer > 90:
                self.frameBuf[:] = 0
                self.reset()
            return

        # -------- Normal gameplay --------
        target_pos = self.POINTS[self.target_idx]
        self.ball_pos = self.move_towards(self.ball_pos, target_pos)

        # Turn off any lights the ball passes through
        ball_leds = self.get_leds_near_position(self.ball_pos)
        self.uneaten[ball_leds] = False

        # Check if ball reached target using distance calculation
        if np.linalg.norm(self.ball_pos - target_pos) < self.radius:
            self.target_idx = self.pick_target()
            
            if self.target_idx is None:
                self.finishing = True
                return

        # Reset frame buffer
        self.frameBuf[:] = 0

        # Draw uneaten pellets with their base colors
        self.frameBuf[self.uneaten] = self.colors[self.uneaten]

        # Draw the white ball
        self.frameBuf[ball_leds] = [255, 255, 255]  # White ball