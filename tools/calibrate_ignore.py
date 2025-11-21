import sys
import os
# Add parent directory to path to find config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import re
from pynput import mouse
import config

print("--- Ignore Region Wizard ---")
print("This tool will help you define areas to IGNORE (like the lives counter).")
print("1. Click the TOP-LEFT of the area to ignore.")
print("2. Click the BOTTOM-RIGHT of the area to ignore.")
print("Press ESC to cancel.")

clicks = []

def update_config_ignore(ignore_rect):
    """Reads config.py and appends to IGNORE_AREAS."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.py')
    config_path = os.path.abspath(config_path)
    
    if not os.path.exists(config_path):
        print(f"Error: Could not find {config_path}")
        return

    with open(config_path, 'r') as f:
        content = f.read()
        
    # Check if IGNORE_AREAS exists
    if "IGNORE_AREAS" not in content:
        # Add it to the end
        new_content = content + f"\n\n# Areas to ignore detections in (relative to game region)\n# format: (x, y, w, h)\nIGNORE_AREAS = [{ignore_rect}]"
    else:
        # Replace existing or append? Let's just replace for now to be simple, or try to append.
        # Regex to find the list
        match = re.search(r"IGNORE_AREAS\s*=\s*\[(.*?)\]", content, re.DOTALL)
        if match:
            current_list = match.group(1).strip()
            if current_list:
                new_list = current_list + f", {ignore_rect}"
            else:
                new_list = f"{ignore_rect}"
            
            new_content = re.sub(
                r"IGNORE_AREAS\s*=\s*\[.*?\]", 
                f"IGNORE_AREAS = [{new_list}]", 
                content, 
                flags=re.DOTALL
            )
        else:
             new_content = content + f"\nIGNORE_AREAS = [{ignore_rect}]"

    with open(config_path, 'w') as f:
        f.write(new_content)
    
    print(f"\n[SUCCESS] Added {ignore_rect} to IGNORE_AREAS in config.py")

def on_click(x, y, button, pressed):
    if not pressed:
        return
    
    # We need coordinates relative to the capture region!
    # Load current capture region
    cap = config.CAPTURE_REGION
    cap_x = cap['left']
    cap_y = cap['top']
    
    # Adjust click to be relative
    rel_x = int(x) - cap_x
    rel_y = int(y) - cap_y
    
    print(f"Click {len(clicks)+1}: Global({int(x)}, {int(y)}) -> Relative({rel_x}, {rel_y})")
    clicks.append((rel_x, rel_y))
    
    if len(clicks) == 1:
        print("--> Now click the BOTTOM-RIGHT of the ignore area.")
    elif len(clicks) == 2:
        tl = clicks[0]
        br = clicks[1]
        
        w = br[0] - tl[0]
        h = br[1] - tl[1]
        
        # Handle negative
        if w < 0: w = -w; tl = (tl[0] - w, tl[1])
        if h < 0: h = -h; tl = (tl[0], tl[1] - h)
            
        rect = (tl[0], tl[1], w, h)
        print(f"Calculated Ignore Rect: {rect}")
        
        update_config_ignore(rect)
        return False

# Collect events
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
