# Configuration for Pac-Man AI Agent

# --- Capture Settings ---
# Region of the screen to capture.
# format: {'top': int, 'left': int, 'width': int, 'height': int}
# Calibrated by user
CAPTURE_REGION = {'top': 159, 'left': 953, 'width': 959, 'height': 446}

# Target Frames Per Second for the main loop
TARGET_FPS = 30

# --- Control Settings ---
# Key mappings for the game
KEY_MAP = {
    'UP': 'up',
    'DOWN': 'down',
    'LEFT': 'left',
    'RIGHT': 'right',
    'STOP': 'q'  # Emergency stop key (handled in main loop logic if needed)
}

# Duration to hold a key press (seconds)
KEY_PRESS_DURATION = 0.05

# --- Vision Settings ---
# Path to template images
TEMPLATE_DIR = 'assets/templates'

# Thresholds for template matching
MATCH_THRESHOLD = 0.8

# --- Debugging ---
DEBUG_MODE = True
SHOW_CV_WINDOW = True  # Show the computer vision view window
# Position of the CV window on screen (x, y)
CV_WINDOW_POSITION = (53, 52)
# Size of the CV window (width, height) - None means auto-size
CV_WINDOW_SIZE = (600, 400)

# Grid Dimensions (Width, Height)
# Standard Pac-Man is 28x31. Adjust if needed.
GRID_SIZE = (28, 31)

# Grid Padding (pixels to shave off the capture region before gridding)
# Useful if the capture includes borders or headers
GRID_PADDING = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}

LOG_LEVEL = 'INFO'

# --- Google AI ---
# API Key for Gemini (Load from environment variable)
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file if present

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Areas to ignore detections in (relative to game region)
# format: (x, y, w, h)
IGNORE_AREAS = [(24, 366, 52, 22), (14, 359, 67, 36)]

# --- Game Colors (BGR) ---
# Converted from user provided Hex
GAME_COLORS = {
    'WALLS': [
        (107, 0, 37),   # #25006b
        (22, 0, 166),   # #a60016 (Approx BGR for #a60016 is 22, 0, 166? No. R=166, G=0, B=22 -> BGR=22,0,166)
        (0, 135, 0),    # #008700
        (0, 112, 101)   # #657000 (R=101, G=112, B=0 -> BGR=0, 112, 101)
    ],
    'PATH': (0, 0, 0),
    'GHOSTS': [
        (44, 210, 255), # #ffd22c (Cyan/Gold?) -> BGR
        (204, 123, 255),# #ff7bcc
        (255, 255, 0),  # #00ffff (Cyan) -> BGR(255, 255, 0)
        (0, 0, 255)     # #ff0000 (Red) -> BGR(0, 0, 255)
    ]
}
