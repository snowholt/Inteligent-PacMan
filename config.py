# Configuration for Pac-Man AI Agent

# --- Capture Settings ---
# Region of the screen to capture.
# format: {'top': int, 'left': int, 'width': int, 'height': int}
# TODO: These need to be calibrated to your specific screen and browser window position.
CAPTURE_REGION = {'top': 100, 'left': 100, 'width': 800, 'height': 600}

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
LOG_LEVEL = 'INFO'

# --- Google AI ---
# API Key for Gemini (Load from environment variable)
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file if present

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
