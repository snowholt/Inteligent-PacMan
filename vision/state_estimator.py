from typing import Dict, Any, List, Tuple
import numpy as np
import config

class StateEstimator:
    """
    Converts raw object detections into a logical grid/graph representation.
    """
    
    def __init__(self):
        # Standard Pac-Man grid is roughly 28x31 tiles
        # Load from config if available, else default
        self.grid_width = getattr(config, 'GRID_SIZE', (28, 31))[0]
        self.grid_height = getattr(config, 'GRID_SIZE', (28, 31))[1]
        self.grid = np.zeros((self.grid_height, self.grid_width), dtype=int)
        
        # We need to know the pixel size of the game board to map to grid
        # These will be updated on the first frame
        self.pixel_width = 0
        self.pixel_height = 0
        
        # Static map (walls, pellets)
        self.static_grid = None # 1=Wall, 2=Pellet, 0=Empty
        self.total_pellets = 0
        self.pellets_eaten = 0
        
    def initialize_from_map(self, clean_map: np.ndarray):
        """
        Initialize the grid using the clean static map.
        """
        self.pixel_height, self.pixel_width = clean_map.shape[:2]
        self.grid = np.zeros((self.grid_height, self.grid_width), dtype=int)
        
        # Run the color detection ONCE on the clean map
        self._update_grid_from_colors(clean_map)
        
        # Detect pellets
        self._detect_pellets(clean_map)
        
    def _detect_pellets(self, clean_map: np.ndarray):
        """
        Detect pellets on the static map based on color.
        Updates self.grid with value 2 for pellets.
        """
        if 'PELLETS' not in config.GAME_COLORS:
            return

        pellet_colors = np.array(config.GAME_COLORS['PELLETS'], dtype=np.uint8)
        color_tol = 60 # Increased tolerance
        
        pad = getattr(config, 'GRID_PADDING', {'top': 0, 'bottom': 0, 'left': 0, 'right': 0})
        eff_w = self.pixel_width - pad['left'] - pad['right']
        eff_h = self.pixel_height - pad['top'] - pad['bottom']
        
        cell_w = eff_w / self.grid_width
        cell_h = eff_h / self.grid_height
        
        pellet_count = 0
        for r in range(self.grid_height):
            for c in range(self.grid_width):
                # If it's a wall, skip
                if self.grid[r, c] == 1:
                    continue
                    
                # Check center of cell for pellet color
                cx = int(pad['left'] + (c + 0.5) * cell_w)
                cy = int(pad['top'] + (r + 0.5) * cell_h)
                
                # Safety check
                if cx < 0 or cx >= self.pixel_width or cy < 0 or cy >= self.pixel_height:
                    continue
                    
                # Sample a larger area (60% of the cell) to catch dots even if off-center
                # Calculate scan box size
                scan_w = int(cell_w * 0.6)
                scan_h = int(cell_h * 0.6)
                
                # Ensure minimum size of 4x4
                scan_w = max(4, scan_w)
                scan_h = max(4, scan_h)
                
                x1 = max(0, cx - scan_w // 2)
                x2 = min(self.pixel_width, cx + scan_w // 2)
                y1 = max(0, cy - scan_h // 2)
                y2 = min(self.pixel_height, cy + scan_h // 2)
                
                patch = clean_map[y1:y2, x1:x2]
                
                if patch.size == 0:
                    continue
                    
                # Check if any pixel in patch matches any pellet color
                is_pellet = False
                for p_color in pellet_colors:
                    diff = np.abs(patch - p_color)
                    dist = np.sum(diff, axis=2)
                    # If we find at least a few pixels (e.g. 4) that match, it's a pellet
                    if np.count_nonzero(dist < color_tol) >= 4:
                        is_pellet = True
                        break
                
                if is_pellet:
                    self.grid[r, c] = 2 # 2 = Pellet
                    pellet_count += 1
        
        self.total_pellets = pellet_count
        print(f"DEBUG: Detected {pellet_count} pellets on the map.")
        
    def update(self, detections: Dict[str, Any], frame: np.ndarray) -> Dict[str, Any]:
        """
        Update the internal state based on new detections.
        """
        self.pixel_height, self.pixel_width = frame.shape[:2]
        
        pacman_grid = None
        if detections['pacman']:
            # Filter out detections that are likely "lives" (usually at the very bottom)
            # We assume the playable maze is the main part of the screen.
            # Let's pick the detection that is closest to the center of the screen OR
            # just filter out anything in the bottom 10% if it's a lives counter.
            
            valid_detections = []
            for (x, y, w, h) in detections['pacman']:
                # Check against ignored areas
                ignored = False
                # Center of detection
                cx, cy = x + w//2, y + h//2
                
                if hasattr(config, 'IGNORE_AREAS'):
                    for (ix, iy, iw, ih) in config.IGNORE_AREAS:
                        # Check if center is inside ignore rect
                        if ix <= cx <= ix + iw and iy <= cy <= iy + ih:
                            ignored = True
                            break
                
                if ignored:
                    continue
                    
                valid_detections.append((x, y, w, h))
            
            if valid_detections:
                # If multiple valid ones, pick the first (or closest to last known pos)
                x, y, w, h = valid_detections[0]
                
                # Center of Pac-Man
                cx, cy = x + w // 2, y + h // 2
                
                # Map to grid
                # Apply Padding
                pad = getattr(config, 'GRID_PADDING', {'top': 0, 'bottom': 0, 'left': 0, 'right': 0})
                
                eff_w = self.pixel_width - pad['left'] - pad['right']
                eff_h = self.pixel_height - pad['top'] - pad['bottom']
                
                if eff_w > 0 and eff_h > 0:
                    # Adjust cx, cy to be relative to the padded area
                    cx_rel = cx - pad['left']
                    cy_rel = cy - pad['top']
                    
                    # Formula: grid_x = (cx_rel / eff_w) * grid_width
                    gx = int((cx_rel / eff_w) * self.grid_width)
                    gy = int((cy_rel / eff_h) * self.grid_height)
                    
                    # Clamp to bounds
                    gx = max(0, min(gx, self.grid_width - 1))
                    gy = max(0, min(gy, self.grid_height - 1))
                    
                    pacman_grid = (gx, gy)

        # Update grid (static map) occasionally or if empty
        # For MVP, we update it every frame or just once? 
        # Let's update it every frame for now to handle dynamic changes or camera shifts
        # self._update_grid_from_colors(frame) # <--- DISABLED: This was erasing pellets!

        # Check for eating
        if pacman_grid:
            gx, gy = pacman_grid
            if self.grid[gy, gx] == 2:
                self.grid[gy, gx] = 0 # Eat pellet
                print(f"Nom nom! Ate pellet at {gx}, {gy}")

        # Count remaining pellets
        remaining_pellets = np.count_nonzero(self.grid == 2)
        self.pellets_eaten = self.total_pellets - remaining_pellets

        return {
            'grid': self.grid,
            'pacman_pos': pacman_grid,
            'ghost_positions': [],
            'pellets_total': self.total_pellets,
            'pellets_remaining': remaining_pellets,
            'pellets_eaten': self.pellets_eaten
        }

    def _update_grid_from_colors(self, frame):
        """
        Scan the grid cells and determine if they are walls based on color.
        """
        # Apply Padding
        pad = getattr(config, 'GRID_PADDING', {'top': 0, 'bottom': 0, 'left': 0, 'right': 0})
        
        eff_w = self.pixel_width - pad['left'] - pad['right']
        eff_h = self.pixel_height - pad['top'] - pad['bottom']
        
        if eff_w <= 0 or eff_h <= 0:
            return

        cell_w = eff_w / self.grid_width
        cell_h = eff_h / self.grid_height
        
        # Threshold for color matching
        color_tol = 60
        
        for r in range(self.grid_height):
            for c in range(self.grid_width):
                # Get center of cell (relative to padded area)
                cx_rel = int((c + 0.5) * cell_w)
                cy_rel = int((r + 0.5) * cell_h)
                
                # Add padding offset
                cx = cx_rel + pad['left']
                cy = cy_rel + pad['top']
                
                # Safety check
                if cx >= self.pixel_width or cy >= self.pixel_height:
                    continue
                
                # Sample a small patch (3x3) to catch thin walls
                # We take the max match in the patch
                is_wall = False
                
                # Define patch bounds
                r1 = max(0, cy-1)
                r2 = min(self.pixel_height, cy+2)
                c1 = max(0, cx-1)
                c2 = min(self.pixel_width, cx+2)
                
                patch = frame[r1:r2, c1:c2]
                
                # Check if ANY pixel in patch matches ANY wall color
                # This is computationally heavier but safer for thin walls
                
                # Optimization: First check if it's clearly a PATH (Black)
                # If the center is black, it's likely a path, unless we are on the edge of a wall
                center_pixel = frame[cy, cx]
                # Check if close to black (Path color)
                if np.linalg.norm(center_pixel - np.array(config.GAME_COLORS['PATH'])) < 40:
                    # It's black, so it's a path.
                    self.grid[r, c] = 0
                    continue
                
                for wall_color in config.GAME_COLORS['WALLS']:
                    # Calculate distance for all pixels in patch
                    # patch shape: (h, w, 3), wall_color shape: (3,)
                    diff = np.linalg.norm(patch - np.array(wall_color), axis=2)
                    
                    # We need a certain NUMBER of pixels to match, not just one stray pixel
                    # This reduces noise
                    matches = np.sum(diff < color_tol)
                    if matches > 2: # Require at least 3 pixels in the 3x3 patch to match
                        is_wall = True
                        break
                
                if is_wall:
                    self.grid[r, c] = 1 # 1 = Wall
                else:
                    self.grid[r, c] = 0 # 0 = Walkable
