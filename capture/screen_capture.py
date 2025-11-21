import mss
import numpy as np
import cv2
import time
from typing import Dict, Any

class ScreenCapturer:
    """
    Handles capturing the screen content efficiently.
    Uses 'mss' for high-performance capture on Linux/Windows/macOS.
    """

    def __init__(self, region: Dict[str, int] = None):
        """
        Initialize the screen capturer.
        
        Args:
            region: Dictionary with 'top', 'left', 'width', 'height'.
                    If None, captures the primary monitor (not recommended for performance).
        """
        self.sct = mss.mss()
        self.region = region
        
        # If no region provided, default to the first monitor (full screen)
        if self.region is None:
            self.region = self.sct.monitors[1]

    def capture(self) -> np.ndarray:
        """
        Capture a single frame from the screen.
        """
        try:
            # Try high-performance mss capture first
            screenshot = self.sct.grab(self.region)
            img = np.array(screenshot)
            img_bgr = img[:, :, :3]
            return np.ascontiguousarray(img_bgr)
            
        except Exception as e:
            # Fallback for Wayland if mss fails
            # print(f"MSS failed ({e}), trying fallback...") # Commented out to avoid spam
            return self._capture_fallback()

    def _capture_fallback(self) -> np.ndarray:
        """
        Fallback capture method for Wayland using gnome-screenshot.
        Note: This is much slower than mss.
        """
        import subprocess
        import cv2
        import os
        
        # Define a temporary file path
        tmp_file = "/tmp/pacman_vision_frame.png"
        
        # Construct gnome-screenshot command
        # We capture the specific region to minimize overhead
        # gnome-screenshot area format: -a (interactive) or we can't easily script area without interaction on some versions.
        # On standard Ubuntu GNOME, scripting area is hard without 'screenshot-tool' or similar.
        # Let's try capturing the whole screen and cropping, or just fail gracefully if we can't.
        
        # Actually, on Wayland, automated screenshots often require permission or flash the screen.
        # Let's try capturing the full screen and cropping in numpy.
        
        try:
            # Capture full screen to file (silent if possible)
            # Note: This might flash the screen or make a shutter sound
            subprocess.run(["gnome-screenshot", "--file", tmp_file], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Read back
            img = cv2.imread(tmp_file)
            
            if img is None:
                return None
                
            # Crop to region
            top = self.region['top']
            left = self.region['left']
            width = self.region['width']
            height = self.region['height']
            
            # Ensure bounds
            img_h, img_w = img.shape[:2]
            top = max(0, min(top, img_h))
            left = max(0, min(left, img_w))
            bottom = min(img_h, top + height)
            right = min(img_w, left + width)
            
            return img[top:bottom, left:right]
            
        except Exception as e:
            print(f"Fallback capture failed: {e}")
            return None

    def update_region(self, region: Dict[str, int]):
        """Update the capture region dynamically."""
        self.region = region

if __name__ == "__main__":
    # Simple test
    capturer = ScreenCapturer(region={'top': 100, 'left': 100, 'width': 640, 'height': 480})
    print("Starting capture test...")
    start_time = time.time()
    frames = 0
    
    try:
        while frames < 60:
            frame = capturer.capture()
            frames += 1
            # Just to simulate work
            pass
    except Exception as e:
        print(f"Error: {e}")
        
    end_time = time.time()
    print(f"Captured {frames} frames in {end_time - start_time:.2f} seconds.")
    print(f"FPS: {frames / (end_time - start_time):.2f}")
