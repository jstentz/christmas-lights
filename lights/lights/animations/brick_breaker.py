"""
Brick Breaker Game on the Christmas Tree - Version 2.1 (Grid-Based)

An automated brick breaker game that runs on a 500-LED Christmas tree. The game plays itself with an AI-controlled paddle.
This version uses a TRUE 3D GRID system based on angular sections and height bands,
creating properly mapped "faces" of the tree for accurate spatial gameplay.

Features:
- Grid-based bricks: 8 angular sections × 8 height bands = 64 bricks
- Bricks cover upper 2/3 of tree with alternating RED and GREEN pattern
- Each brick contains all LEDs within its angular/height cell
- Face-aware gameplay: Ball and paddle operate on the visible face
- Cylindrical coordinate system for proper 3D-to-2D mapping
- AI-controlled paddle at the bottom of the tree
- Win animation: Rainbow wave effect with smooth color transitions
- Loss animation: White wash cascading from top to bottom

Implementation:
- LEDs assigned to grid cells by (angle, height) coordinates
- Ball position tracked in cylindrical coordinates (angle, z)
- Collision detection uses angular distance, not just Y projection
- Visible face = ±72° from viewing angle (144° total visible)
- Checkerboard red/green pattern: (section + band) % 2

================================================================================
Designed by: Pat "seeknay" (from TikTok)
Created with: Cursor AI Assistant
Purpose: For fun and learning - NOT a contest entry
Date: December 27, 2025
Version: 2.1 - Red/Green bricks covering 2/3 of tree
================================================================================
"""
from lights.animations.base import BaseAnimation
from typing import Optional
from lights.utils.geometry import POINTS_3D
import numpy as np


class BrickBreaker(BaseAnimation):
    """
    Classic Brick Breaker game displayed on a 3D Christmas tree.
    
    This game uses a TRUE 3D GRID system that properly maps the tree's conical
    surface into a playable 2D game space. Instead of treating the tree as a
    flat surface, we divide it into angular sections (like pizza slices when
    viewed from above) and height bands (horizontal layers).
    
    How it works:
    - The tree is divided into 8 angular sections (45° each)
    - Each section is divided into 8 height bands
    - Each brick = one cell in this grid (section × band)
    - Bricks cover the upper 2/3 of the tree (from 33% to 100% height)
    - Gameplay happens on a "visible face" that rotates slowly around the tree
    
    Game Elements:
    - Paddle (white): AI-controlled, follows ball at the bottom of the tree
    - Ball (yellow): Bounces around, breaks bricks on contact
    - Bricks (red/green): Grid cells in a checkerboard pattern
    
    Why this approach is better:
    - Previous versions used sequential LED indices, which didn't match the
      tree's 3D structure. This version uses actual spatial coordinates.
    - Collision detection works in cylindrical space (angle + height), so
      the ball properly bounces off bricks that are actually next to each
      other in 3D space, not just in the LED string order.
    """
    
    def __init__(self, frameBuf: np.ndarray, *, 
                 fps: Optional[int] = 30,
                 ball_speed: float = 0.02,
                 paddle_speed: float = 0.025,
                 paddle_width: float = 0.8,  # In radians (~45 degrees)
                 num_sections: int = 8,
                 num_bands: int = 8,  # More bands to fill 2/3 of tree
                 rotation_speed: float = 0.002):
        """
        Initialize the Grid-Based Brick Breaker game.
        
        Args:
            frameBuf: Numpy array (500, 3) for RGB values (0-255) - one row per LED
            fps: Frames per second for animation timing (30 = smooth gameplay)
            ball_speed: How fast the ball moves (radians per frame for angle, units for z)
            paddle_speed: How fast the AI paddle tracks the ball (radians per frame)
            paddle_width: How wide the paddle is in radians (~45 degrees = 0.8)
            num_sections: Number of angular sections (8 = 45° each, like pizza slices)
            num_bands: Number of height bands for bricks (8 bands = more bricks)
            rotation_speed: How fast the visible face rotates around the tree
        """
        super().__init__(frameBuf, fps=fps)
        
        # Store game parameters so we can use them later
        self.ball_speed = ball_speed
        self.paddle_speed = paddle_speed
        self.paddle_width = paddle_width
        self.num_sections = num_sections
        self.num_bands = num_bands
        self.rotation_speed = rotation_speed
        
        # === 3D Coordinate Setup ===
        # First, we center all the LED coordinates at the origin (0,0,0)
        # This makes calculations easier - everything is relative to the tree center
        self.center = np.mean(POINTS_3D, axis=0)
        self.centered = POINTS_3D - self.center
        
        # Extract individual coordinate arrays for easier access
        # X = front-to-back depth, Y = left-to-right, Z = bottom-to-top (height)
        self.x = self.centered[:, 0]
        self.y = self.centered[:, 1]
        self.z = self.centered[:, 2]
        
        # === Cylindrical Coordinates ===
        # This is the KEY improvement - we convert from 3D (x,y,z) to cylindrical (r,θ,z)
        # Think of it like unrolling the tree into a cylinder:
        # - r = distance from center axis (how far from center)
        # - θ (theta) = angle around the tree (0° to 360°, like a clock)
        # - z = height (same as before)
        self.radii = np.sqrt(self.x**2 + self.y**2)  # Distance from center axis
        self.angles = np.arctan2(self.y, self.x)  # Angle around tree [-π, π]
        self.angles_normalized = (self.angles + np.pi) / (2 * np.pi)  # Normalize to [0, 1] for easier math
        
        # Height boundaries - find the actual min/max heights of LEDs
        self.z_min, self.z_max = self.z.min(), self.z.max()
        self.z_range = self.z_max - self.z_min
        
        # Normalize z to [0, 1] so we can work with percentages
        # 0 = bottom of tree, 1 = top of tree
        self.z_normalized = (self.z - self.z_min) / self.z_range
        
        # === Grid System Setup ===
        # This creates the brick grid by assigning each LED to a section and band
        self._setup_grid()
        
        # === Game Boundaries ===
        # The "visible face" is the part of the tree you can see and play on
        # It's like a window that shows ±72° (144° total) of the tree
        self.face_half_width = np.pi * 0.4  # ±72° visible = 144° total
        self.viewing_angle = 0.0  # Current center of visible face (starts at 0°)
        
        # Height boundaries for gameplay
        self.game_z_min = 0.1  # Paddle area (bottom 10% of tree)
        self.game_z_max = 0.98  # Top boundary (98% of tree height)
        self.brick_z_min = 0.33  # Bricks start at 1/3 height (upper 2/3 for bricks)
        
        # === Paddle Setup ===
        # Paddle position in cylindrical coordinates
        # The paddle moves around the tree at a fixed height, following the ball
        self.paddle_angle = 0.0  # Angular position (starts at center of visible face)
        self.paddle_z = 0.15  # Height position (15% up from bottom, normalized)
        self.paddle_thickness = 0.08  # How thick the paddle is in the Z direction
        
        # === Ball Setup ===
        # Ball position and velocity in cylindrical coordinates
        self.ball_angle = 0.0  # Angular position (where around the tree)
        self.ball_z = 0.25  # Height position (25% up from bottom)
        self.ball_v_angle = ball_speed * 0.7  # Angular velocity (how fast it moves around)
        self.ball_v_z = ball_speed  # Vertical velocity (how fast it moves up/down)
        self.ball_radius_angle = 0.15  # Collision radius in radians (how "big" the ball is)
        self.ball_radius_z = 0.04  # Collision radius in z direction
        
        # === Colors ===
        # Classic brick breaker color scheme
        self.bg_color = np.array([5, 5, 15])  # Dark blue-black background
        self.paddle_color = np.array([255, 255, 255])  # White paddle
        self.ball_color = np.array([255, 255, 0])  # Yellow ball
        
        # Classic brick breaker colors - red and green alternating in checkerboard pattern
        self.brick_red = np.array([255, 0, 0])  # Bright red
        self.brick_green = np.array([0, 255, 0])  # Bright green
        self.brick_dim_red = np.array([60, 0, 0])  # Dim red for back-face bricks (not visible)
        self.brick_dim_green = np.array([0, 60, 0])  # Dim green for back-face bricks
        
        # === Game State ===
        # Track whether the game is won, lost, or playing
        self.won = False
        self.lost = False
        self.win_animation_frames = 0  # Counter for win animation
        self.loss_animation_frames = 0  # Counter for loss animation
        self.ball_fall_count = 0  # How many times the ball has fallen (lives system)
        self.brick_hit_cooldown = 0  # Prevent hitting multiple bricks in one frame
        self.frame_count = 0  # Total frames rendered
        self.game_count = 0  # How many games have been played
        
        # Print initialization info so we can see what was set up
        self._print_init_info()
    
    def _setup_grid(self):
        """
        Create the grid-based brick system.
        
        This is where the magic happens - we divide the tree into a grid and
        assign each LED to a brick based on its position.
        
        How it works:
        1. Divide the tree into angular sections (like pizza slices from above)
        2. Divide each section into height bands (horizontal layers)
        3. Each brick = one cell in this grid (section × band)
        4. Find all LEDs that fall within each cell
        5. Store them as a brick
        
        Bricks cover the upper 2/3 of the tree (from z=0.33 to z=1.0).
        The bottom 1/3 is reserved for the paddle and ball area.
        """
        # Calculate how wide each angular section is (in radians)
        # 8 sections = 360° / 8 = 45° each = π/4 radians
        section_width = 2 * np.pi / self.num_sections
        
        # Assign each LED to a section based on its angle around the tree
        # First, shift angles from [-π, π] to [0, 2π] for easier math
        angles_positive = (self.angles + np.pi) % (2 * np.pi)
        # Then divide by section width and round down to get section number (0-7)
        self.led_sections = (angles_positive / section_width).astype(int) % self.num_sections
        
        # Assign each LED to a height band
        # Bricks cover upper 2/3 of tree (from 33% to 100% height)
        band_z_min = 0.33  # Start bricks at 1/3 height (2/3 of tree for bricks)
        band_z_range = 1.0 - band_z_min  # Remaining height for bricks (0.67)
        band_height = band_z_range / self.num_bands  # Height of each band
        
        # Calculate which band each LED belongs to
        # LEDs below the brick area get -1 (not in any brick)
        self.led_bands = np.full(len(POINTS_3D), -1, dtype=int)
        in_brick_area = self.z_normalized >= band_z_min  # Which LEDs are in brick area?
        # For LEDs in brick area, calculate which band they're in
        self.led_bands[in_brick_area] = np.clip(
            ((self.z_normalized[in_brick_area] - band_z_min) / band_height).astype(int),
            0, self.num_bands - 1
        )
        
        # Create brick dictionary: (section, band) -> brick info
        # This stores all the information about each brick
        self.bricks = {}
        for section in range(self.num_sections):
            for band in range(self.num_bands):
                # Find all LEDs that are in this specific cell (section AND band)
                mask = (self.led_sections == section) & (self.led_bands == band)
                indices = np.where(mask)[0].tolist()  # Get the LED indices
                
                # Only create a brick if there are LEDs in this cell
                if len(indices) > 0:
                    # Calculate the center of this brick in cylindrical coordinates
                    # This is used for collision detection - where is the brick "centered"?
                    brick_angles = self.angles[indices]
                    brick_z = self.z_normalized[indices]
                    
                    # Handle angle wraparound for center calculation
                    # We use sin/cos average to handle the case where angles wrap around 0/360°
                    mean_sin = np.mean(np.sin(brick_angles))
                    mean_cos = np.mean(np.cos(brick_angles))
                    center_angle = np.arctan2(mean_sin, mean_cos)
                    center_z = np.mean(brick_z)  # Average height
                    
                    # Store all the brick information
                    self.bricks[(section, band)] = {
                        'indices': indices,  # Which LEDs make up this brick
                        'active': True,  # Is this brick still in play? (False when hit)
                        'section': section,  # Which angular section (0-7)
                        'band': band,  # Which height band (0-7)
                        'center_angle': center_angle,  # Center angle for collision
                        'center_z': center_z,  # Center height for collision
                        'num_leds': len(indices),  # How many LEDs in this brick
                    }
        
        # Store brick boundaries for collision detection
        self.section_width = section_width
        self.band_height = band_height
        self.band_z_min = band_z_min
        
        # Print summary so we know what was created
        print(f"Grid setup complete: {len(self.bricks)} bricks created")
        print(f"  Sections: {self.num_sections} ({np.degrees(section_width):.1f}° each)")
        print(f"  Bands: {self.num_bands} ({band_height:.3f} z-units each)")
    
    def _print_init_info(self):
        """Print initialization summary so we can see what was set up."""
        print(f"\n{'='*60}")
        print("BRICK BREAKER v2.1 - Red/Green Grid-Based")
        print(f"{'='*60}")
        print(f"Grid: {self.num_sections} sections × {self.num_bands} bands")
        print(f"Total bricks: {len(self.bricks)}")
        print(f"LEDs per brick: {np.mean([b['num_leds'] for b in self.bricks.values()]):.1f} avg")
        print(f"Brick coverage: Upper 2/3 of tree (z >= 0.33)")
        print(f"Colors: Alternating RED and GREEN (checkerboard)")
        print(f"Visible face: ±{np.degrees(self.face_half_width):.0f}° ({np.degrees(2*self.face_half_width):.0f}° total)")
        print(f"Ball speed: {self.ball_speed}")
        print(f"{'='*60}\n")
    
    def _get_angular_distance(self, angle1, angle2):
        """
        Calculate the shortest angular distance between two angles.
        
        This handles the tricky case where angles wrap around at ±180°.
        For example, the distance between 170° and -170° is 20°, not 340°.
        
        Args:
            angle1: First angle in radians
            angle2: Second angle in radians
            
        Returns:
            Shortest angular distance in radians (always between -π and π)
        """
        diff = angle1 - angle2
        # Normalize to [-π, π] range by wrapping around
        while diff > np.pi:
            diff -= 2 * np.pi
        while diff < -np.pi:
            diff += 2 * np.pi
        return diff
    
    def _is_angle_visible(self, angle):
        """
        Check if an angle is within the visible face.
        
        The visible face is the part of the tree you can currently see and play on.
        It's centered at self.viewing_angle and extends ±72° in each direction.
        
        Args:
            angle: Angle to check (in radians)
            
        Returns:
            True if this angle is visible, False if it's on the back of the tree
        """
        diff = abs(self._get_angular_distance(angle, self.viewing_angle))
        return diff < self.face_half_width
    
    def _get_visible_sections(self):
        """
        Get list of section indices that are currently visible.
        
        Only sections within the visible face can be hit by the ball.
        This makes the game feel more like a traditional 2D brick breaker
        while still showing the 3D structure of the tree.
        
        Returns:
            List of section numbers (0-7) that are currently visible
        """
        visible = []
        for section in range(self.num_sections):
            # Calculate the center angle of this section
            # Sections are numbered 0-7, starting at -π and going around
            section_center = -np.pi + (section + 0.5) * self.section_width
            if self._is_angle_visible(section_center):
                visible.append(section)
        return visible
    
    def _move_paddle(self):
        """
        Move paddle to follow ball using AI.
        
        Simple but effective AI: the paddle moves toward the ball's angular
        position with some lag, making it feel realistic. The paddle stays
        within the visible face so you can always see it.
        """
        # Calculate angular difference between paddle and ball
        # Positive = ball is to the right, negative = ball is to the left
        angle_diff = self._get_angular_distance(self.ball_angle, self.paddle_angle)
        
        # Move toward ball with some lag (dead zone prevents jittery movement)
        if abs(angle_diff) > 0.05:  # Dead zone to prevent jitter
            if angle_diff > 0:
                self.paddle_angle += self.paddle_speed  # Move right
            else:
                self.paddle_angle -= self.paddle_speed  # Move left
        
        # Keep paddle within visible face
        # Don't let it go off the edges where you can't see it
        max_paddle_offset = self.face_half_width - self.paddle_width / 2
        paddle_diff = self._get_angular_distance(self.paddle_angle, self.viewing_angle)
        if paddle_diff > max_paddle_offset:
            self.paddle_angle = self.viewing_angle + max_paddle_offset
        elif paddle_diff < -max_paddle_offset:
            self.paddle_angle = self.viewing_angle - max_paddle_offset
        
        # Normalize paddle angle to [-π, π] range
        # Keep it in the standard range for easier calculations
        while self.paddle_angle > np.pi:
            self.paddle_angle -= 2 * np.pi
        while self.paddle_angle < -np.pi:
            self.paddle_angle += 2 * np.pi
    
    def _move_ball(self):
        """
        Move ball and handle all collision detection.
        
        This is the core game logic that handles:
        - Ball movement (update position based on velocity)
        - Wall collisions (bounce off edges of visible face)
        - Top wall collision (bounce off top of tree)
        - Paddle collision (bounce up with spin)
        - Brick collisions (destroy brick and bounce)
        - Ball falling (lives system - lose on 3rd fall)
        - Win condition (all bricks destroyed)
        """
        # === Ball Movement ===
        # Update ball position based on velocity
        self.ball_angle += self.ball_v_angle  # Move around the tree
        self.ball_z += self.ball_v_z  # Move up/down
        
        # Normalize ball angle to [-π, π] range
        # Keep it in the standard range for easier calculations
        while self.ball_angle > np.pi:
            self.ball_angle -= 2 * np.pi
        while self.ball_angle < -np.pi:
            self.ball_angle += 2 * np.pi
        
        # === Side Wall Collisions (edge of visible face) ===
        # The ball bounces off the left and right edges of the visible face
        ball_to_center = self._get_angular_distance(self.ball_angle, self.viewing_angle)
        wall_limit = self.face_half_width - self.ball_radius_angle  # Account for ball size
        
        if abs(ball_to_center) > wall_limit:
            # Ball hit the wall - reverse direction
            self.ball_v_angle = -self.ball_v_angle
            # Push ball back inside the boundary
            if ball_to_center > 0:
                self.ball_angle = self.viewing_angle + wall_limit
            else:
                self.ball_angle = self.viewing_angle - wall_limit
        
        # === Top Wall Collision ===
        # Ball bounces off the top of the tree
        if self.ball_z > self.game_z_max:
            self.ball_v_z = -abs(self.ball_v_z)  # Always bounce down
            self.ball_z = self.game_z_max  # Keep ball inside boundary
        
        # === Paddle Collision ===
        # Check if ball hit the paddle
        paddle_angle_diff = abs(self._get_angular_distance(self.ball_angle, self.paddle_angle))
        if (self.ball_z <= self.paddle_z + self.paddle_thickness and
            self.ball_z >= self.paddle_z - self.ball_radius_z and
            paddle_angle_diff < self.paddle_width / 2):
            # Ball hit paddle - bounce up
            self.ball_v_z = abs(self.ball_v_z)  # Always go up
            # Add spin based on where ball hit paddle
            # Hit on edge = more spin, hit on center = less spin
            hit_pos = self._get_angular_distance(self.ball_angle, self.paddle_angle)
            spin = (hit_pos / (self.paddle_width / 2)) * self.ball_speed
            self.ball_v_angle = spin
            # Push ball slightly above paddle so it doesn't get stuck
            self.ball_z = self.paddle_z + self.paddle_thickness + 0.01
        
        # === Brick Collisions ===
        # Check if ball hit any bricks
        if self.brick_hit_cooldown > 0:
            # Cooldown prevents hitting multiple bricks in one frame
            self.brick_hit_cooldown -= 1
        else:
            # Only check bricks in visible sections (can't hit back-face bricks)
            visible_sections = self._get_visible_sections()
            for (section, band), brick in self.bricks.items():
                if not brick['active']:
                    continue  # Skip destroyed bricks
                if section not in visible_sections:
                    continue  # Skip back-face bricks
                
                # Check collision with brick center
                # Calculate distance from ball to brick center
                angle_diff = abs(self._get_angular_distance(self.ball_angle, brick['center_angle']))
                z_diff = abs(self.ball_z - brick['center_z'])
                
                # Collision thresholds - ball is within brick if both distances are small
                angle_threshold = self.section_width / 2 + self.ball_radius_angle
                z_threshold = self.band_height / 2 + self.ball_radius_z
                
                if angle_diff < angle_threshold and z_diff < z_threshold:
                    # Ball hit brick! Destroy it and bounce
                    brick['active'] = False
                    # Determine bounce direction based on which side was hit
                    # If hit top/bottom, bounce vertically; if hit side, bounce horizontally
                    if z_diff > angle_diff * (self.band_height / self.section_width):
                        self.ball_v_z = -self.ball_v_z  # Hit top or bottom
                    else:
                        self.ball_v_angle = -self.ball_v_angle  # Hit left or right side
                    self.brick_hit_cooldown = 5  # Prevent multiple hits
                    break  # Only one brick per frame
        
        # === Ball Falls Below Paddle ===
        # Ball fell off the bottom - lives system
        if self.ball_z < self.game_z_min - 0.1:
            self.ball_fall_count += 1
            # Lose on every 3rd fall (3 lives)
            if self.ball_fall_count % 3 == 0:
                self.lost = True
                self.loss_animation_frames = 0
            else:
                # Give another chance - reset ball position
                self._reset_ball()
        
        # === Win Condition ===
        # Check if all bricks are destroyed
        active_bricks = sum(1 for b in self.bricks.values() if b['active'])
        if active_bricks == 0 and not self.won:
            self.won = True
            self.win_animation_frames = 0
    
    def _reset_ball(self):
        """
        Reset ball to starting position above paddle.
        
        Called when ball falls (but not on final life) or when game resets.
        Ball starts at paddle position with random direction.
        """
        self.ball_angle = self.paddle_angle  # Start at paddle position
        self.ball_z = self.paddle_z + 0.15  # Start slightly above paddle
        self.ball_v_z = abs(self.ball_speed)  # Always start going up
        # Random direction (left or right)
        self.ball_v_angle = self.ball_speed * 0.5 * (1 if np.random.random() > 0.5 else -1)
    
    def _reset_game(self):
        """
        Reset the entire game.
        
        Called after win or loss animation completes. Resets all bricks,
        moves to a new face of the tree, and starts a new game.
        """
        # Reset all bricks to active
        for brick in self.bricks.values():
            brick['active'] = True
        
        # Rotate to a new face for variety
        self.game_count += 1
        self.viewing_angle = (self.game_count * np.pi / 3) % (2 * np.pi) - np.pi
        self.paddle_angle = self.viewing_angle  # Start paddle at center of new face
        
        # Reset ball and game state
        self._reset_ball()
        self.won = False
        self.lost = False
        self.win_animation_frames = 0
        self.loss_animation_frames = 0
        self.ball_fall_count = 0
        self.brick_hit_cooldown = 0
    
    def renderNextFrame(self) -> None:
        """
        Render one frame of the game.
        
        This is called every frame by the animation framework. It:
        1. Updates the viewing angle (slow rotation)
        2. Handles win/loss animations
        3. Updates game state (move paddle, move ball)
        4. Renders everything to frameBuf (bricks, paddle, ball)
        """
        self.frame_count += 1
        
        # Slow rotation of the viewing angle
        # This makes the game slowly rotate around the tree, showing different faces
        self.viewing_angle += self.rotation_speed
        if self.viewing_angle > np.pi:
            self.viewing_angle -= 2 * np.pi
        
        # Handle win/loss animations
        if self.lost:
            self.loss_animation_frames += 1
            if self.loss_animation_frames >= 120:  # 4 seconds at 30fps
                # Animation complete, reset game
                self._reset_game()
            else:
                # Show loss effect (white wash)
                self._render_loss_effect()
                return
        
        if self.won:
            self.win_animation_frames += 1
            if self.win_animation_frames >= 90:  # 3 seconds at 30fps
                # Animation complete, reset game
                self._reset_game()
            else:
                # Show win celebration (rainbow)
                self._render_win_celebration()
                return
        
        # Update game state (move paddle, move ball, check collisions)
        self._move_paddle()
        self._move_ball()
        
        # === Render Frame ===
        # Clear to background color
        self.frameBuf[:] = self.bg_color
        
        # Get which sections are currently visible
        visible_sections = self._get_visible_sections()
        
        # Draw bricks - alternating red and green in checkerboard pattern
        for (section, band), brick in self.bricks.items():
            if not brick['active']:
                continue  # Skip destroyed bricks
            
            # Checkerboard pattern: alternate based on section + band
            # Even sum = red, odd sum = green
            is_red = (section + band) % 2 == 0
            
            if section in visible_sections:
                # Full brightness for visible bricks
                color = self.brick_red if is_red else self.brick_green
            else:
                # Dim color for back-face bricks (so you can see tree structure)
                color = self.brick_dim_red if is_red else self.brick_dim_green
            
            # Set color for all LEDs in this brick
            for idx in brick['indices']:
                self.frameBuf[idx] = color
        
        # Draw paddle
        # Find all LEDs that are near the paddle position
        for i in range(len(POINTS_3D)):
            angle_diff = abs(self._get_angular_distance(self.angles[i], self.paddle_angle))
            z_diff = abs(self.z_normalized[i] - self.paddle_z)
            
            # Check if this LED is within paddle bounds
            if angle_diff < self.paddle_width / 2 and z_diff < self.paddle_thickness:
                # Only draw if it's on the visible face
                if self._is_angle_visible(self.angles[i]):
                    self.frameBuf[i] = self.paddle_color
        
        # Draw ball
        # Find all LEDs that are near the ball position
        for i in range(len(POINTS_3D)):
            angle_diff = abs(self._get_angular_distance(self.angles[i], self.ball_angle))
            z_diff = abs(self.z_normalized[i] - self.ball_z)
            
            # Calculate distance in normalized space (ellipse shape)
            # Ball is slightly wider in angle than in height
            dist = np.sqrt((angle_diff / self.ball_radius_angle)**2 + 
                          (z_diff / self.ball_radius_z)**2)
            
            # If within ball radius and visible, draw ball
            if dist < 1.0 and self._is_angle_visible(self.angles[i]):
                self.frameBuf[i] = self.ball_color
    
    def _render_win_celebration(self):
        """
        Render rainbow celebration effect when the game is won.
        
        Creates a beautiful rainbow effect that rotates around the tree
        with pulsing brightness. Each LED's color is based on its angle
        around the tree plus a time-based rotation.
        """
        progress = self.win_animation_frames / 90.0  # 0 to 1 over 3 seconds
        
        # Create expanding rainbow rings
        for i in range(len(POINTS_3D)):
            # Hue based on angle around tree + time
            # This creates a rotating rainbow effect
            hue = (self.angles_normalized[i] + progress * 0.5) % 1.0
            
            # Brightness pulse - makes it feel alive
            pulse = 0.7 + 0.3 * np.sin(self.win_animation_frames * 0.1 + self.z_normalized[i] * 10)
            
            # Convert HSV to RGB manually (for speed)
            h = hue * 6
            c = 1.0
            x = c * (1 - abs(h % 2 - 1))
            
            if h < 1:
                r, g, b = c, x, 0
            elif h < 2:
                r, g, b = x, c, 0
            elif h < 3:
                r, g, b = 0, c, x
            elif h < 4:
                r, g, b = 0, x, c
            elif h < 5:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
            
            # Apply pulse and convert to RGB
            self.frameBuf[i] = [int(r * 255 * pulse), int(g * 255 * pulse), int(b * 255 * pulse)]
    
    def _render_loss_effect(self):
        """
        Render white wash effect from top to bottom when the game is lost.
        
        Creates a dramatic white wave that cascades down the tree from top
        to bottom, like a "game over" effect.
        """
        progress = self.loss_animation_frames / 120.0  # 0 to 1 over 4 seconds
        
        for i in range(len(POINTS_3D)):
            # Calculate position from top (0 = top, 1 = bottom)
            z_from_top = 1.0 - self.z_normalized[i]
            
            # Wash position moves from top to bottom
            wash_position = progress * 1.15  # Slightly extend past bottom
            
            # Distance from wash edge
            distance_from_wash = wash_position - z_from_top
            
            # Brightness: 1.0 if above wash, fade to 0.0 in transition band
            brightness = np.clip(1.0 - (distance_from_wash / 0.15), 0.0, 1.0)
            
            # White color with calculated brightness
            self.frameBuf[i] = [int(255 * brightness)] * 3
