import os
import json
import cv2
import time
import datetime
from typing import Dict, Any

class DataLogger:
    """
    Logs game data (frames and state) for analysis and training.
    """
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = os.path.join(self.log_dir, self.session_id)
        
        # Create directories
        os.makedirs(os.path.join(self.session_dir, "frames"), exist_ok=True)
        
        self.log_file = os.path.join(self.session_dir, "data.jsonl")
        self.frame_count = 0
        self.last_decision = None
        
    def log_step(self, frame, game_state: Dict[str, Any], action: str, metadata: Dict[str, Any] = None):
        """
        Log a single step of the game.
        
        Args:
            frame: The game frame (numpy array).
            game_state: The perceived game state.
            action: The action taken by the agent.
            metadata: Additional info (e.g., "interesting_event": True).
        """
        self.frame_count += 1
        
        # Determine if we should log this frame
        should_log = False
        reason = []
        
        # 1. Every 10th frame
        if self.frame_count % 10 == 0:
            should_log = True
            reason.append("periodic")
            
        # 2. Decision changed
        if action != self.last_decision:
            should_log = True
            reason.append("decision_change")
            
        # 3. Interesting event (passed in metadata)
        if metadata and metadata.get("interesting", False):
            should_log = True
            reason.append("interesting")
            
        if should_log:
            self._save_log(frame, game_state, action, reason)
            
        self.last_decision = action
        
    def _save_log(self, frame, game_state, action, reason):
        timestamp = time.time()
        frame_filename = f"frame_{self.frame_count:06d}.jpg"
        frame_path = os.path.join(self.session_dir, "frames", frame_filename)
        
        # Save image
        cv2.imwrite(frame_path, frame)
        
        # Prepare log entry
        # Convert numpy types to python types for JSON serialization
        serializable_state = self._make_serializable(game_state)
        
        entry = {
            "frame_id": self.frame_count,
            "timestamp": timestamp,
            "image_file": f"frames/{frame_filename}",
            "action": action,
            "reasons": reason,
            "state": serializable_state
        }
        
        # Append to JSONL file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
            
    def _make_serializable(self, data):
        """Recursively convert numpy types to python types."""
        if hasattr(data, 'tolist'):
            return data.tolist()
        if isinstance(data, dict):
            return {k: self._make_serializable(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self._make_serializable(v) for v in data]
        if isinstance(data, tuple):
            return tuple(self._make_serializable(v) for v in data)
        return data
