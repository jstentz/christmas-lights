"""
Template animation file.
Replace this with your own animation class, or use --sample to run a sample animation.
"""
from lights.animations.base import BaseAnimation
from typing import Optional
from lights.utils.geometry import POINTS_3D
from lights.utils.colors import hsv_to_rgb
import numpy as np

# Write your animation here!


class Plinko(BaseAnimation):
    """
    Example animation template.
    Modify this class to create your own animation.
    """

    def __init__(self, frameBuf: np.ndarray, *, fps: Optional[int] = 30,
                 num_balls: int = 1, trail_len: int = 2,
                 fall_speed: float = 0.006, bounce_interval: float = 0.12) -> None:
        super().__init__(frameBuf, fps=fps)

        #parameters
        self.num_balls = num_balls
        self.trail_len = trail_len
        self.fall_speed = fall_speed
        self.bounce_interval = bounce_interval


        #analyze the 3D point cloud to see the bounds
        self.points = POINTS_3D.copy()
        
        # Rotate all points by 180 degrees around the vertical axis
        # First, find which axis is vertical
        temp_ranges = np.max(self.points, axis=0) - np.min(self.points, axis=0)
        temp_vertical_axis = np.argmax(temp_ranges)
        temp_horizontal_axis = [i for i in range(3) if i != temp_vertical_axis]
        
        # Calculate center before rotation
        temp_center = (np.min(self.points, axis=0) + np.max(self.points, axis=0)) / 2
        
        # Rotate horizontal coordinates by 180 degrees (negate relative to center)
        # Vectorized operation: center, negate, un-center
        self.points[:, temp_horizontal_axis[0]] = 2 * temp_center[temp_horizontal_axis[0]] - self.points[:, temp_horizontal_axis[0]]
        self.points[:, temp_horizontal_axis[1]] = 2 * temp_center[temp_horizontal_axis[1]] - self.points[:, temp_horizontal_axis[1]]
        
        self.min_bounds = np.min(self.points, axis=0)
        self.max_bounds = np.max(self.points, axis=0)
        self.center = ((self.min_bounds + self.max_bounds) / 2)


        #find which axis has the most range
        ranges = self.max_bounds - self.min_bounds
        #find index of range to find vertical axis
        #Usually Y (index 1)
        self.vertical_axis = np.argmax(ranges)

        #horizontal axis are the other two

        self.horizontal_axis = [i for i in range(3) if i != self.vertical_axis]

        #compute the normal height for each pixel (0 = bottom, 1 = top)
        self.pixel_heights = (self.points[:, self.vertical_axis] - self.min_bounds[self.vertical_axis]) / ranges[self.vertical_axis]

        #initialize pegs
        self.peg_pixels = self.create_pegs()

        #initalize the balls
        self.balls = []
        for i in range(num_balls):
            #stagger the initial spawns
            self.balls.append(self.create_ball())

        self.frame_count = 0

        self.snake_active = False
        self.snake_progress = 0
        self.snake_color = [255, 255, 255]
        self.snake_length = 20

        self.snake_pixels = self.get_snake_pixels()

    def create_pegs(self) -> list:
        """Create horizontal ring layers with small gaps."""
        peg_pixels = []
        self.peg_layers = {}  # Track which layer each peg is on

        num_layers = 3
        num_gaps = 4
        gap_size = 4

        for layer in range(num_layers):
            height = 0.15 + (layer / (num_layers - 1)) * 0.55

            height_tolerance = 0.04
            pixels_at_height = np.where(
                np.abs(self.pixel_heights - height) < height_tolerance
            )[0]

            if len(pixels_at_height) == 0:
                continue

            h_axis1 = self.horizontal_axis[0]
            h_axis2 = self.horizontal_axis[1]
            angles = np.arctan2(
                self.points[pixels_at_height, h_axis1] - self.center[h_axis1],
                self.points[pixels_at_height, h_axis2] - self.center[h_axis2]
            )
            sorted_indices = np.argsort(angles)
            sorted_pixels = pixels_at_height[sorted_indices]

            total = len(sorted_pixels)
            gap_spacing = total // num_gaps

            offset = (layer % 2) * (gap_spacing // 2)

            for i, px in enumerate(sorted_pixels):
                pos = (i + offset) % total
                in_gap = False
                for g in range(num_gaps):
                    gap_start = g * gap_spacing
                    if gap_start <= pos < gap_start + gap_size:
                        in_gap = True
                        break

                if not in_gap:
                    peg_pixels.append(px)
                    self.peg_layers[px] = layer

        return peg_pixels

    def create_ball(self, initial_delay: float = 0.0):
        h_axis1 = self.horizontal_axis[0]
        h_axis2 = self.horizontal_axis[1]
        x_pos = np.random.uniform(
            self.min_bounds[h_axis1] + (self.max_bounds[h_axis1] - self.min_bounds[h_axis1]) * 0.4,
            self.min_bounds[h_axis1] + (self.max_bounds[h_axis1] - self.min_bounds[h_axis1]) * 0.6
        )
        z_pos = np.random.uniform(
            self.min_bounds[h_axis2] + (self.max_bounds[h_axis2] - self.min_bounds[h_axis2]) * 0.4,
            self.min_bounds[h_axis2] + (self.max_bounds[h_axis2] - self.min_bounds[h_axis2]) * 0.6
        )

        hue = np.random.random()

        return {
            'height': 1.0,
            'x_offset': x_pos,
            'z_offset': z_pos,
            'hue': hue,
            'trail': [],
            'last_bounce_height': 0.95,
            'active': True,
            'landed_frames': 0,
            'velocity_y': 0,
            'last_peg_hit': None,
            'stuck_count': 0,
            'last_layer_hit': None,
        }

    def respawn_ball(self, ball: dict):
        """
        reset a ball to the top of the tree
        """
        h_axis1 = self.horizontal_axis[0]
        h_axis2 = self.horizontal_axis[1]
        ball['height'] = 1.0
        ball['velocity_y'] = 0.0
        ball['stuck_count'] = 0
        ball['last_layer_hit'] = None
        ball['x_offset'] = np.random.uniform(
            self.min_bounds[h_axis1],
            self.max_bounds[h_axis1]
        )
        ball['z_offset'] = np.random.uniform(
            self.min_bounds[h_axis2],
            self.max_bounds[h_axis2]
        )
        ball['hue'] = np.random.random()
        ball['trail'] = []
        ball['last_bounce_height'] = 1.0
        ball['active'] = True
        ball['landed_frames'] = 0
        ball['last_peg_hit'] = None

    def get_snake_pixels(self):
        """Get pixels sorted from bottom to top in a spiral pattern."""
        # Sort all pixels by height
        sorted_by_height = np.argsort(self.pixel_heights)

        # For each height level, sort by angle to create spiral effect
        spiral_pixels = []
        height_chunks = np.array_split(sorted_by_height, 50)  # Split into 50 levels

        h_axis1 = self.horizontal_axis[0]
        h_axis2 = self.horizontal_axis[1]

        angle_offset = 0
        for chunk in height_chunks:
            # Calculate angles for this chunk
            angles = np.arctan2(
                self.points[chunk, h_axis1] - self.center[h_axis1],
                self.points[chunk, h_axis2] - self.center[h_axis2]
            )
            # Add offset to create spiral
            adjusted_angles = (angles + angle_offset) % (2 * np.pi)
            sorted_chunk = chunk[np.argsort(adjusted_angles)]
            spiral_pixels.extend(sorted_chunk)
            angle_offset += 0.3  # Rotate each level

        return spiral_pixels

    def find_nearest_pixel(self, height: float, x_offset: float, z_offset: float = None) -> int:
        """Find the pixel index nearest to the given height, staying on same side of tree."""
        v_axis = self.vertical_axis
        h_axis1 = self.horizontal_axis[0]
        h_axis2 = self.horizontal_axis[1]

        target_height = self.min_bounds[v_axis] + height * (self.max_bounds[v_axis] - self.min_bounds[v_axis])

        # Find pixels close to our target height
        height_diff = np.abs(self.points[:, v_axis] - target_height)
        close_to_height = np.where(height_diff < 0.05)[0]

        if len(close_to_height) == 0:
            return np.argmin(height_diff)

        # Use both horizontal axes to find truly nearest pixel
        x_diffs = np.abs(self.points[close_to_height, h_axis1] - x_offset)

        if z_offset is not None:
            z_diffs = np.abs(self.points[close_to_height, h_axis2] - z_offset)
            total_diffs = x_diffs + z_diffs
        else:
            total_diffs = x_diffs

        best_idx = np.argmin(total_diffs)
        return close_to_height[best_idx]

    def update_ball(self, ball: dict):
        """
        update a single ball's position
        """
        if not ball['active']:
            ball['landed_frames'] += 1
            # Only respawn after snake AND celebration are done (celebration is 30 frames after snake)
            if ball['landed_frames'] >= 30 and not self.snake_active and self.snake_progress >= len(self.snake_pixels):
                self.respawn_ball(ball)
            return

        # Apply gravity
        gravity = 0.0003
        ball['velocity_y'] -= gravity

        # Move based on velocity
        ball['height'] += ball['velocity_y']

        # Find nearest pixel and add to trail
        if ball['height'] > 0 and ball['height'] <= 1.0:
            nearest_pixel = self.find_nearest_pixel(ball['height'], ball['x_offset'], ball['z_offset'])

            if ball['trail']:
                last_pixel = ball['trail'][-1]
                last_pos = self.points[last_pixel]
                new_pos = self.points[nearest_pixel]
                distance = np.linalg.norm(last_pos - new_pos)

                # Only move if the new pixel is close enough
                if distance > 0.15:
                    # Only move down every few frames to slow things down
                    if ball['velocity_y'] < 0 and self.frame_count % 2 == 0:
                        # Can't move to nearest_pixel, find closest pixel that's LOWER
                        current_height = self.pixel_heights[last_pixel]

                        # Find all pixels lower than current
                        lower_mask = (self.pixel_heights < current_height - 0.01) & (self.pixel_heights > current_height - 0.08)
                        lower_pixels = np.where(lower_mask)[0]

                        if len(lower_pixels) > 0:
                            # Find the closest lower pixel
                            distances_to_lower = np.linalg.norm(self.points[lower_pixels] - last_pos, axis=1)
                            closest_lower_idx = np.argmin(distances_to_lower)
                            nearest_pixel = lower_pixels[closest_lower_idx]
                        else:
                            nearest_pixel = last_pixel
                    else:
                        nearest_pixel = last_pixel

                # Simple bounce: if on a peg, bounce once per layer then pass through
                if nearest_pixel in self.peg_pixels:
                    layer = self.peg_layers.get(nearest_pixel, 0)
                    if layer != ball['last_layer_hit']:
                        ball['last_layer_hit'] = layer
                        # Nudge sideways
                        h_axis = self.horizontal_axis[0]
                        nudge = (self.max_bounds[h_axis] - self.min_bounds[h_axis]) * 0.06
                        if np.random.random() > 0.5:
                            ball['x_offset'] += nudge
                        else:
                            ball['x_offset'] -= nudge

                        # Actually move UP to a higher pixel
                        current_pos = self.points[nearest_pixel]
                        current_height = self.pixel_heights[nearest_pixel]
                        higher_mask = (self.pixel_heights > current_height + 0.08) & (
                                self.pixel_heights < current_height + 0.20)
                        higher_pixels = np.where(higher_mask)[0]

                        if len(higher_pixels) > 0:
                            # Pick a pixel that's both close horizontally AND high
                            h_axis1 = self.horizontal_axis[0]
                            h_axis2 = self.horizontal_axis[1]
                            h_dist = np.abs(self.points[higher_pixels, h_axis1] - current_pos[h_axis1]) + \
                                     np.abs(self.points[higher_pixels, h_axis2] - current_pos[h_axis2])
                            # Prefer pixels that are close horizontally
                            closest_idx = np.argmin(h_dist)
                            nearest_pixel = higher_pixels[closest_idx]

                        # Set velocity positive so it doesn't immediately fall
                        ball['velocity_y'] = 0.004

                # Clear last layer after moving far enough below it
                if ball['last_layer_hit'] is not None:
                    layer_heights = [0.15, 0.425, 0.70]
                    layer_height = layer_heights[ball['last_layer_hit']]
                    if ball['height'] < layer_height - 0.12:
                        ball['last_layer_hit'] = None

            # Reset stuck count if we're not on a peg
            if nearest_pixel not in self.peg_pixels:
                ball['stuck_count'] = 0

            # Reset last_peg_hit if we've moved away from it
            if ball['last_peg_hit'] is not None:
                peg_pos = self.points[ball['last_peg_hit']]
                current_pos = self.points[nearest_pixel]
                if np.linalg.norm(current_pos - peg_pos) > 0.1:
                    ball['last_peg_hit'] = None

            # Only add to trail if it's a new pixel
            if not ball['trail'] or ball['trail'][-1] != nearest_pixel:
                ball['trail'].append(nearest_pixel)

            # Limit trail length
            if len(ball['trail']) > self.trail_len:
                ball['trail'].pop(0)

        # Check if ball has landed (must be at bottom AND have traveled down the tree)
        if len(ball['trail']) > 0:
            # Verify the ball is actually near the bottom of the tree
            current_pixel = ball['trail'][-1]
            if self.pixel_heights[current_pixel] < 0.10:
                ball['active'] = False
                ball['landed_frames'] = 0
                # Start the snake!
                self.snake_active = True
                self.snake_progress = 0
                r, g, b = hsv_to_rgb(np.random.random(), 1.0, 1.0)
                self.snake_color = [r, g, b]

    def renderNextFrame(self) -> None:
        """
        Called every frame. Update self.frameBuf with RGB values (0-255).
        frameBuf is a numpy array of shape (NUM_PIXELS, 3).
        """

        # Check if snake is done (triggers rainbow)
        celebration_active = False
        if self.snake_active:
            self.snake_progress += 12  # Speed of snake
            if self.snake_progress >= len(self.snake_pixels):
                # Snake finished, start celebration
                self.snake_active = False
                celebration_active = True
                for ball in self.balls:
                    if not ball['active']:
                        ball['landed_frames'] = 0  # Reset for rainbow timing

        # Check if rainbow is active
        for ball in self.balls:
            if not ball['active'] and ball['landed_frames'] < 30 and not self.snake_active:
                if self.snake_progress >= len(self.snake_pixels):
                    celebration_active = True

        # if celebrating, sparkly rainbow
        if celebration_active:
            for i in range(len(self.frameBuf)):
                if np.random.random() < 0.3:
                    hue = (i / len(self.frameBuf) + self.frame_count * 0.02) % 1.0
                    r, g, b = hsv_to_rgb(hue, 1.0, np.random.uniform(0.5, 1.0))
                    self.frameBuf[i] = [r, g, b]
                else:
                    hue = (i / len(self.frameBuf) + self.frame_count * 0.02) % 1.0
                    r, g, b = hsv_to_rgb(hue, 1.0, 0.2)
                    self.frameBuf[i] = [r, g, b]
        elif self.snake_active:
            # Draw dark background
            self.frameBuf[:] = [2, 2, 5]

            # Draw the snake
            snake_head = min(self.snake_progress, len(self.snake_pixels) - 1)
            snake_tail = max(0, self.snake_progress - self.snake_length)

            for i in range(snake_tail, snake_head + 1):
                px = self.snake_pixels[i]
                # Fade from tail to head
                fade = (i - snake_tail) / max(1, snake_head - snake_tail)
                self.frameBuf[px] = [
                    int(self.snake_color[0] * fade),
                    int(self.snake_color[1] * fade),
                    int(self.snake_color[2] * fade),
                ]
        else:
            self.frameBuf[:] = [2, 2, 5]  # dark background

        # Draw the pegs with different colors per layer (only when not celebrating and not snake)
        if not celebration_active and not self.snake_active:
            layer_colors = [
                [255, 0, 0],  # Layer 0: Red (top)
                [255, 150, 0],  # Layer 1: Orange (middle)
                [255, 255, 0],  # Layer 2: Yellow (bottom)
            ]
            for peg_idx in self.peg_pixels:
                layer = self.peg_layers.get(peg_idx, 0)
                self.frameBuf[peg_idx] = layer_colors[layer]

        # update and draw each ball
        for ball in self.balls:
            self.update_ball(ball)

            # get balls RGB color
            r, g, b = hsv_to_rgb(ball['hue'], 1.0, 1.0)

            if ball['active']:
                # draw trail with fading brightness
                for i, pixel_idx in enumerate(ball['trail']):
                    fade = (i + 1) / len(ball['trail']) if ball['trail'] else 1
                    self.frameBuf[pixel_idx] = [
                        int(r * fade * 0.6),
                        int(g * fade * 0.6),
                        int(b * fade * 0.6),
                    ]

                # draw the ball itself (brighter)
                if ball['trail']:
                    current_pixel = ball['trail'][-1]
                    # Make it brighter by mixing with white
                    self.frameBuf[current_pixel] = [
                        min(255, r + 100),
                        min(255, g + 100),
                        min(255, b + 100),
                    ]

        self.frame_count += 1