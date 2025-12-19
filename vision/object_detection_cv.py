import cv2
import numpy as np
import os
from typing import List, Dict, Any
import config

class ObjectDetectorCV:
    """
    Classical Computer Vision based object detector.
    Uses template matching and color segmentation.
    """
    
    def __init__(self, template_dir: str = 'assets/templates'):
        self.template_dir = template_dir
        self.templates = {}
        self.load_templates()
        
    def load_templates(self):
        """Load template images from the config directory."""
        if not os.path.exists(config.TEMPLATE_DIR):
            print(f"Warning: Template directory {config.TEMPLATE_DIR} not found.")
            return

        for filename in os.listdir(config.TEMPLATE_DIR):
            if filename.endswith('.png') and 'snapshot' not in filename:
                name = os.path.splitext(filename)[0]
                path = os.path.join(config.TEMPLATE_DIR, filename)
                template = cv2.imread(path)
                if template is not None:
                    self.templates[name] = template
                    print(f"Loaded template: {name}")
                else:
                    print(f"Failed to load template: {path}")

    def detect_objects(self, frame: np.ndarray) -> Dict[str, List[Any]]:
        """
        Detect Pac-Man, Ghosts, and Pellets in the frame.
        """
        results = {
            'pacman': None,
            'ghosts': [],
            'pellets': []
        }
        
        if not self.templates:
            return results

        # 1. Detect Pac-Man
        if 'pacman' in self.templates:
            pacman_locs = self._match_template(frame, self.templates['pacman'], threshold=0.7)
            results['pacman'] = pacman_locs

        # 2. Detect Ghosts (if template exists)
        if 'ghost' in self.templates:
            ghost_locs = self._match_template(frame, self.templates['ghost'], threshold=0.8)
            results['ghosts'] = ghost_locs

        return results

    def _match_template(self, frame, template, threshold=0.8):
        """
        Helper to perform template matching.
        Returns list of (x, y, w, h) tuples.
        """
        # Convert to grayscale for faster/robust matching? 
        # For now, let's stick to BGR if colors matter (ghosts are different colors).
        # Actually, Pac-Man rotates, so simple template matching might fail if he faces a different way.
        # We might need templates for each direction or use color detection.
        
        res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        
        matches = []
        h, w = template.shape[:2]
        
        # Zip the results and format
        for pt in zip(*loc[::-1]):
            matches.append((pt[0], pt[1], w, h))
            
        # Non-maximum suppression could go here to remove duplicate detections of the same object
        # For MVP, we just return all high-confidence matches
        return matches
