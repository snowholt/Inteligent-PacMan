"""
Pac-Man AI Agent - Main Entry Point

Architecture:
1. Capture: Grab screen region.
2. Vision: Detect objects and update state.
3. Agent: Decide action based on state.
4. Control: Execute action.
5. Loop: Repeat at target FPS.
"""

import time
import cv2
import numpy as np
import config
from capture.screen_capture import ScreenCapturer
from control.keyboard_controller import KeyboardController
from vision.object_detection_cv import ObjectDetectorCV
from vision.state_estimator import StateEstimator
from agent.policy_simple import SimplePolicyAgent

def main():
    print("Initializing Pac-Man AI Agent...")
    
    # 1. Initialize Modules
    capturer = ScreenCapturer(region=config.CAPTURE_REGION)
    controller = KeyboardController()
    detector = ObjectDetectorCV()
    estimator = StateEstimator()
    agent = SimplePolicyAgent()
    
    print(f"Target FPS: {config.TARGET_FPS}")
    print("Press Ctrl+C to stop.")
    
    frame_duration = 1.0 / config.TARGET_FPS
    
    try:
        while True:
            loop_start = time.time()
            
            # --- 1. Capture ---
            frame = capturer.capture()
            
            if frame is None:
                print("Failed to capture frame.")
                continue

            # --- 2. Vision (Detection & State) ---
            # TODO: In the future, we might skip detection on some frames for performance
            detections = detector.detect_objects(frame)
            game_state = estimator.update(detections)
            
            # --- 3. Agent (Decision) ---
            action = agent.decide_action(game_state)
            
            # --- 4. Control (Action) ---
            # For MVP, we just print the action and simulate a key press
            # In real game, we would check if we actually need to change direction
            if config.DEBUG_MODE:
                # Draw on frame for debugging
                cv2.putText(frame, f"Action: {action}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            controller.press_key(action, duration=config.KEY_PRESS_DURATION)
            
            # --- 5. Visualization ---
            if config.SHOW_CV_WINDOW:
                cv2.imshow("Pac-Man AI Vision", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # --- 6. FPS Control ---
            loop_end = time.time()
            elapsed = loop_end - loop_start
            sleep_time = frame_duration - elapsed
            
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                if config.DEBUG_MODE:
                    print(f"Warning: Lagging behind target FPS. Loop took {elapsed:.4f}s")

    except KeyboardInterrupt:
        print("\nStopping agent...")
    finally:
        cv2.destroyAllWindows()
        print("Agent stopped.")

if __name__ == "__main__":
    main()
