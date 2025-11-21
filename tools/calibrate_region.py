import time
import re
import os
from pynput import mouse

print("--- Setup Wizard ---")
print("This tool will help you configure the screen locations.")
print("\nSTEP 1: Game Capture Region")
print("  1. Click the TOP-LEFT corner of the Pac-Man game.")
print("  2. Click the BOTTOM-RIGHT corner of the Pac-Man game.")
print("\nSTEP 2: AI Window Position")
print("  3. Click where you want the TOP-LEFT corner of the AI Vision window to be.")
print("\nPress ESC to cancel.")

clicks = []

def update_config_file(region, ai_pos):
    """Reads config.py, updates values using regex, and saves it."""
    # Resolve path relative to this script
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.py')
    config_path = os.path.abspath(config_path)
    
    if not os.path.exists(config_path):
        print(f"Error: Could not find {config_path}")
        return

    with open(config_path, 'r') as f:
        content = f.read()
        
    # Update CAPTURE_REGION
    # Matches: CAPTURE_REGION = { ... }
    # We use repr(region) to format the dict, but we might need to ensure it looks nice
    new_region_str = f"CAPTURE_REGION = {region}"
    content = re.sub(
        r"CAPTURE_REGION\s*=\s*\{[^}]+\}", 
        new_region_str, 
        content
    )
    
    # Update CV_WINDOW_POSITION
    # Matches: CV_WINDOW_POSITION = ( ... )
    new_pos_str = f"CV_WINDOW_POSITION = {ai_pos}"
    content = re.sub(
        r"CV_WINDOW_POSITION\s*=\s*\([^)]+\)", 
        new_pos_str, 
        content
    )
    
    with open(config_path, 'w') as f:
        f.write(content)
    
    print(f"\n[SUCCESS] Updated {config_path}")
    print(f"  - {new_region_str}")
    print(f"  - {new_pos_str}")

def on_click(x, y, button, pressed):
    if not pressed:
        return
    
    x, y = int(x), int(y)
    clicks.append((x, y))
    print(f"Click {len(clicks)}: ({x}, {y})")
    
    if len(clicks) == 1:
        print("--> Now click the BOTTOM-RIGHT of the game.")
    elif len(clicks) == 2:
        print("--> Now click where you want the AI Window (TOP-LEFT).")
    elif len(clicks) == 3:
        # Process
        game_tl = clicks[0]
        game_br = clicks[1]
        ai_tl = clicks[2]
        
        # Calculate width/height
        width = game_br[0] - game_tl[0]
        height = game_br[1] - game_tl[1]
        
        # Handle negative width/height if user clicked wrong
        if width < 0:
            width = -width
            game_tl = (game_tl[0] - width, game_tl[1])
        if height < 0:
            height = -height
            game_tl = (game_tl[0], game_tl[1] - height)
            
        region = {'top': game_tl[1], 'left': game_tl[0], 'width': width, 'height': height}
        
        print("\nProcessing...")
        update_config_file(region, ai_tl)
        return False # Stop listener

# Collect events until released
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
