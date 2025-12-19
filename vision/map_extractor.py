import cv2
import numpy as np
import time
from typing import List

class MapExtractor:
    """
    Extracts a static map of the game by observing multiple frames
    and removing moving objects (ghosts, pacman).
    """
    def __init__(self):
        self.frames = []
        
    def capture_frames(self, capturer, duration=3.0):
        """
        Capture frames for a set duration.
        """
        print(f"Capturing map frames for {duration} seconds...")
        start_time = time.time()
        count = 0
        while time.time() - start_time < duration:
            frame = capturer.capture()
            if frame is not None:
                self.frames.append(frame)
                count += 1
            time.sleep(0.05) # 20 FPS capture for map is enough
        print(f"Captured {count} frames for map extraction.")
        
    def extract_clean_map(self) -> np.ndarray:
        """
        Compute the median frame to remove moving objects.
        """
        if not self.frames:
            return None
            
        # Stack frames: (N, H, W, 3)
        stack = np.stack(self.frames, axis=0)
        
        # Calculate median along the time axis (axis 0)
        # This effectively removes anything that moves (ghosts, pacman)
        # leaving only the static background (walls, pellets)
        median_frame = np.median(stack, axis=0).astype(np.uint8)
        
        return median_frame
