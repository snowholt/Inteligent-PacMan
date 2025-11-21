import cv2
import numpy as np
import sys
import os
import time

# Add parent directory to path to find config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from capture.screen_capture import ScreenCapturer

def save_config(padding):
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.py')
    config_path = os.path.abspath(config_path)
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    import re
    # Replace GRID_PADDING line
    new_line = f"GRID_PADDING = {padding}"
    if "GRID_PADDING =" in content:
        content = re.sub(r"GRID_PADDING = .*", new_line, content)
    else:
        content += f"\n{new_line}"
        
    with open(config_path, 'w') as f:
        f.write(content)
    print(f"[SUCCESS] Saved padding to {config_path}")

def main():
    print("--- Grid Calibration Tool ---")
    print("Adjust the grid to match the maze corridors.")
    print("Controls:")
    print("  W / S : Increase/Decrease TOP padding")
    print("  Z / X : Increase/Decrease BOTTOM padding")
    print("  A / D : Increase/Decrease LEFT padding")
    print("  Q / E : Increase/Decrease RIGHT padding")
    print("  ENTER : Save and Exit")
    print("  ESC   : Cancel")

    cap = ScreenCapturer()
    
    # Load initial padding
    pad = config.GRID_PADDING.copy()
    
    grid_w, grid_h = config.GRID_SIZE

    while True:
        frame = cap.capture()
        if frame is None:
            continue
            
        h, w = frame.shape[:2]
        
        # Calculate effective grid area
        eff_w = w - pad['left'] - pad['right']
        eff_h = h - pad['top'] - pad['bottom']
        
        # Draw Padding Border (Red)
        cv2.rectangle(frame, (0, 0), (w, pad['top']), (0, 0, 255), -1) # Top
        cv2.rectangle(frame, (0, h-pad['bottom']), (w, h), (0, 0, 255), -1) # Bottom
        cv2.rectangle(frame, (0, 0), (pad['left'], h), (0, 0, 255), -1) # Left
        cv2.rectangle(frame, (w-pad['right'], 0), (w, h), (0, 0, 255), -1) # Right
        
        # Draw Grid Lines (Green)
        if eff_w > 0 and eff_h > 0:
            cell_w = eff_w / grid_w
            cell_h = eff_h / grid_h
            
            start_x = pad['left']
            start_y = pad['top']
            
            for c in range(grid_w + 1):
                x = int(start_x + c * cell_w)
                cv2.line(frame, (x, start_y), (x, start_y + eff_h), (0, 255, 0), 1)
                
            for r in range(grid_h + 1):
                y = int(start_y + r * cell_h)
                cv2.line(frame, (start_x, y), (start_x + eff_w, y), (0, 255, 0), 1)

        # Draw Info
        info = f"T:{pad['top']} B:{pad['bottom']} L:{pad['left']} R:{pad['right']}"
        cv2.putText(frame, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Calibrate Grid", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 27: # ESC
            break
        elif key == 13: # Enter
            save_config(pad)
            break
            
        # Adjustments
        step = 1
        if key == ord('w'): pad['top'] += step
        if key == ord('s'): pad['top'] = max(0, pad['top'] - step)
        
        if key == ord('z'): pad['bottom'] += step
        if key == ord('x'): pad['bottom'] = max(0, pad['bottom'] - step)
        
        if key == ord('a'): pad['left'] += step
        if key == ord('d'): pad['left'] = max(0, pad['left'] - step)
        
        if key == ord('q'): pad['right'] += step
        if key == ord('e'): pad['right'] = max(0, pad['right'] - step)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
