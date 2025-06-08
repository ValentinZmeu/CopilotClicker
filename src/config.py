import os

# Application settings
APP_NAME = "CopilotClicker"
APP_ID = "CopilotClicker"  # For Windows (AppUserModelID)

# User interface settings
UI_BACKGROUND_COLOR = "#333333"
UI_TEXT_COLOR = "#FFFFFF"
UI_SECONDARY_TEXT_COLOR = "#CCCCCC"
UI_HELP_TEXT_COLOR = "#AAAAAA"
UI_RUNNING_COLOR = "#00FF00"
UI_PAUSED_COLOR = "#FFCC00"
UI_BUTTON_PAUSE_COLOR = "#444444"
UI_BUTTON_STOP_COLOR = "#AA3333"
UI_WINDOW_WIDTH = 300
UI_WINDOW_HEIGHT = 200

# Detection settings
MATCH_THRESHOLD = 0.8  # Threshold for considering a match (0-1)
SCAN_INTERVAL = 0.5  # Time between scans in seconds

# Key settings
ESC_DETECTION_WINDOW = 2  # Seconds in which ESC keys must be pressed
ESC_COUNT_THRESHOLD = 3  # Number of ESC presses to show dialog

# Resource paths
def get_assets_path(filename):
    """Gets the full path to a file in the assets folder."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', filename)

ICON_PATH = get_assets_path('icon.ico')
BUTTON_TEMPLATE_PATH = get_assets_path('button.png')
