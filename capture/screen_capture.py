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
        
        Returns:
            numpy.ndarray: The captured image in BGR format (ready for OpenCV).
        """
        # mss returns BGRA, we usually want BGR for OpenCV processing
        # grab() is fast.
        screenshot = self.sct.grab(self.region)
        
        # Convert to numpy array
        img = np.array(screenshot)
        
        # Drop the alpha channel to get BGR
        img_bgr = img[:, :, :3]
        
        # Ensure it's contiguous for OpenCV performance
        img_bgr = np.ascontiguousarray(img_bgr)
        
        return img_bgr

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
