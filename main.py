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
from utils.data_logger import DataLogger

def main():
    print("Initializing Pac-Man AI Agent...")
    
    # Initialize modules
    capturer = ScreenCapturer(region=config.CAPTURE_REGION)
    detector = ObjectDetectorCV(template_dir=config.TEMPLATE_DIR)
    estimator = StateEstimator()
    controller = KeyboardController()
    agent = SimplePolicyAgent()
    logger = DataLogger()
    
    # --- Mapping Phase ---
    print("--- MAPPING PHASE ---")
    print("Please ensure the game is visible and running.")
    print("Do NOT move the window.")
    time.sleep(1) # Give user a sec
    
    from vision.map_extractor import MapExtractor
    map_extractor = MapExtractor()
    map_extractor.capture_frames(capturer, duration=3.0)
    clean_map = map_extractor.extract_clean_map()
    
    if clean_map is not None:
        print("Map extracted successfully!")
        estimator.initialize_from_map(clean_map)
        # Save it for debug
        import cv2
        cv2.imwrite("logs/clean_map_debug.png", clean_map)
    else:
        print("WARNING: Map extraction failed. Using dynamic updates.")

    print(f"Starting Pac-Man AI Agent... (Target FPS: {config.TARGET_FPS})")
    print("Press 'q' to quit. Press 's' to save a snapshot.")

    frame_duration = 1.0 / config.TARGET_FPS
    last_time = time.time()
    
    try:
        while True:
            loop_start = time.time()
            
            # --- 1. Capture ---
            frame = capturer.capture()
            if frame is None:
                print("Failed to capture frame.")
                time.sleep(0.1)
                continue

            # --- 2. Vision (Detection & State) ---
            # TODO: In the future, we might skip detection on some frames for performance
            detections = detector.detect_objects(frame)
            game_state = estimator.update(detections, frame)
            
            # --- 3. Agent (Decision) ---
            action = agent.decide_action(game_state)
            
            # --- 4. Control (Action) ---
            controller.execute_action(action)
            
            # --- 5. Logging ---
            if config.ENABLE_LOGGING:
                # Check for interesting events (e.g., ghost detected)
                metadata = {"interesting": len(detections.get('ghosts', [])) > 0}
                logger.log_step(frame, game_state, action, metadata)

            if config.DEBUG_MODE:
                # Draw detections
                for (x, y, w, h) in detections['pacman']:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.putText(frame, "PAC", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                
                if game_state['pacman_pos']:
                    gx, gy = game_state['pacman_pos']
                    cv2.putText(frame, f"Grid: ({gx}, {gy})", (10, 60), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    
                    # Draw local grid for verification
                    # Draw a small circle on the center of the current grid cell
                    h, w = frame.shape[:2]
                    gw, gh = config.GRID_SIZE
                    pad = getattr(config, 'GRID_PADDING', {'top': 0, 'bottom': 0, 'left': 0, 'right': 0})
                    
                    eff_w = w - pad['left'] - pad['right']
                    eff_h = h - pad['top'] - pad['bottom']
                    
                    if eff_w > 0 and eff_h > 0:
                        cell_w = eff_w / gw
                        cell_h = eff_h / gh
                        
                        cx = int(pad['left'] + (gx + 0.5) * cell_w)
                        cy = int(pad['top'] + (gy + 0.5) * cell_h)
                        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                        
                        # Draw walls (ALL of them for debug)
                        grid = game_state['grid']
                        
                        # Draw Grid Lines for alignment check
                        for c in range(gw + 1): # Vertical lines
                            x = int(pad['left'] + c * cell_w)
                            cv2.line(frame, (x, pad['top']), (x, h - pad['bottom']), (50, 50, 50), 1)
                        for r in range(gh + 1): # Horizontal lines
                            y = int(pad['top'] + r * cell_h)
                            cv2.line(frame, (pad['left'], y), (w - pad['right'], y), (50, 50, 50), 1)

                        for r in range(gh):
                            for c in range(gw):
                                if grid[r, c] == 1:
                                    wx = int(pad['left'] + c * cell_w)
                                    wy = int(pad['top'] + r * cell_h)
                                    cv2.rectangle(frame, (wx, wy), (int(wx+cell_w), int(wy+cell_h)), (0, 0, 100), 1)
                                elif grid[r, c] == 2: # Pellet
                                    cx = int(pad['left'] + (c + 0.5) * cell_w)
                                    cy = int(pad['top'] + (r + 0.5) * cell_h)
                                    # Draw larger Green circle for visibility
                                    cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)
                
                for (x, y, w, h) in detections['ghosts']:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

                # HUD: Pellet Stats
                total = game_state.get('pellets_total', 0)
                remaining = game_state.get('pellets_remaining', 0)
                eaten = game_state.get('pellets_eaten', 0)
                
                hud_text = [
                    f"Action: {action}",
                    f"Pellets: {remaining}/{total}",
                    f"Eaten: {eaten}"
                ]
                
                for i, line in enumerate(hud_text):
                    cv2.putText(frame, line, (10, 30 + i*30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            controller.press_key(action, duration=config.KEY_PRESS_DURATION)
            
            # --- 5. Visualization ---
            if config.SHOW_CV_WINDOW:
                window_name = "Pac-Man AI Vision"
                # Create window if it doesn't exist (implicitly handled by imshow, but needed for moveWindow)
                # We do this once or check if it's the first frame
                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                
                # Move window only once to avoid fighting user (hacky check)
                if 'window_moved' not in locals():
                    cv2.moveWindow(window_name, config.CV_WINDOW_POSITION[0], config.CV_WINDOW_POSITION[1])
                    if config.CV_WINDOW_SIZE:
                        cv2.resizeWindow(window_name, config.CV_WINDOW_SIZE[0], config.CV_WINDOW_SIZE[1])
                    window_moved = True

                cv2.imshow(window_name, frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Save snapshot for template creation
                    timestamp = int(time.time())
                    filename = f"assets/templates/snapshot_{timestamp}.png"
                    cv2.imwrite(filename, frame)
                    print(f"Snapshot saved to {filename}")
            
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
