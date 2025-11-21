import numpy as np
from typing import List, Dict, Any

class ObjectDetectorCV:
    """
    Classical Computer Vision based object detector.
    Uses template matching and color segmentation.
    """
    
    def __init__(self):
        # TODO: Load templates from config.TEMPLATE_DIR
        self.templates = {} 
        pass
        
    def detect_objects(self, frame: np.ndarray) -> Dict[str, List[Any]]:
        """
        Detect Pac-Man, Ghosts, and Pellets in the frame.
        
        Args:
            frame: The cropped game region image.
            
        Returns:
            Dictionary containing lists of detected objects and their coordinates.
            e.g., {
                'pacman': (x, y),
                'ghosts': [(x1, y1, color), ...],
                'pellets': [(x1, y1), ...]
            }
        """
        # TODO: Implement template matching here.
        # cv2.matchTemplate(...)
        
        return {
            'pacman': None,
            'ghosts': [],
            'pellets': []
        }
