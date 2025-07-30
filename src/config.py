import os
import platform
import ctypes

# Application settings
APP_NAME = "CopilotClicker"
APP_ID = "CopilotClicker"  # For# Resource paths
def get_assets_path(filename):
    """Gets the full path to a file in the assets folder."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', filename)

def get_click_path(filename=None):
    """Gets the full path to a file in the assets/click folder.
    If filename is None, returns the path to the click folder."""
    if filename:
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'click', filename)
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'click')

def get_avoid_path(filename=None):
    """Gets the full path to a file in the assets/avoid folder.
    If filename is None, returns the path to the avoid folder."""
    if filename:
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'avoid', filename)
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'avoid')

def get_all_images_in_directory(directory):
    """Gets all image files in a directory."""
    if not os.path.exists(directory):
        return []
    
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    return [os.path.join(directory, f) for f in os.listdir(directory) 
            if os.path.isfile(os.path.join(directory, f)) and 
            os.path.splitext(f)[1].lower() in image_extensions]

ICON_PATH = get_assets_path('icon.ico')

# Dynamically load all button templates
BUTTON_TEMPLATES = get_all_images_in_directory(get_click_path())

# Dynamically load all button templates to avoid
AVOID_BUTTON_TEMPLATES = get_all_images_in_directory(get_avoid_path())

# Theme icons (Unicode symbols)serModelID)

# Theme control variables
MANUAL_THEME_OVERRIDE = False
MANUAL_DARK_MODE = False

# Function to detect system theme (dark/light)
def is_dark_theme():
    """Detects if the system is using a dark theme."""
    try:
        if platform.system() == "Windows":
            # For Windows
            try:
                # Windows 10 and above
                registry_key = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
                key = OpenKey(HKEY_CURRENT_USER, registry_key)
                value, _ = QueryValueEx(key, "AppsUseLightTheme")
                return value == 0  # 0 means dark theme
            except:
                return False  # Default to light theme if cannot detect
        elif platform.system() == "Darwin":  # macOS
            try:
                # Check macOS dark mode
                import subprocess
                result = subprocess.run(
                    ["defaults", "read", "-g", "AppleInterfaceStyle"],
                    capture_output=True, text=True
                )
                return "Dark" in result.stdout
            except:
                return False
        elif platform.system() == "Linux":
            # Try to detect GTK theme
            try:
                import subprocess
                result = subprocess.run(
                    ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
                    capture_output=True, text=True
                )
                return "dark" in result.stdout.lower()
            except:
                return False
    except:
        return False  # Default to light theme if any error

# Set colors based on system theme
if MANUAL_THEME_OVERRIDE:
    DARK_MODE = MANUAL_DARK_MODE
else:
    DARK_MODE = is_dark_theme()

# UI color settings
if DARK_MODE:
    # Dark theme colors
    UI_BACKGROUND_COLOR = "#333333"
    UI_TEXT_COLOR = "#FFFFFF"
    UI_SECONDARY_TEXT_COLOR = "#CCCCCC"
    UI_HELP_TEXT_COLOR = "#AAAAAA"
    UI_TOOLTIP_BACKGROUND_COLOR = "#555555"
    UI_TOOLTIP_TEXT_COLOR = "#FFFFFF"
else:
    # Light theme colors
    UI_BACKGROUND_COLOR = "#F0F0F0"
    UI_TEXT_COLOR = "#000000"
    UI_SECONDARY_TEXT_COLOR = "#333333"
    UI_HELP_TEXT_COLOR = "#555555"
    UI_TOOLTIP_BACKGROUND_COLOR = "#FFFFCC"
    UI_TOOLTIP_TEXT_COLOR = "#000000"

# Colors that remain the same regardless of theme
UI_RUNNING_COLOR = "#00AA00"
UI_PAUSED_COLOR = "#AA8800"
UI_BUTTON_PAUSE_COLOR = "#444444" if DARK_MODE else "#DDDDDD"
UI_BUTTON_STOP_COLOR = "#AA3333"

# UI dimensions
UI_WINDOW_WIDTH = 420
UI_WINDOW_HEIGHT = 280
UI_WINDOW_MIN_WIDTH = 380
UI_WINDOW_MIN_HEIGHT = 340

# Function to toggle theme
def toggle_theme():
    """Toggles between dark and light theme."""
    global MANUAL_THEME_OVERRIDE, MANUAL_DARK_MODE
    global UI_BACKGROUND_COLOR, UI_TEXT_COLOR, UI_SECONDARY_TEXT_COLOR, UI_HELP_TEXT_COLOR, UI_BUTTON_PAUSE_COLOR, DARK_MODE
    global UI_TOOLTIP_BACKGROUND_COLOR, UI_TOOLTIP_TEXT_COLOR
    
    MANUAL_THEME_OVERRIDE = True
    MANUAL_DARK_MODE = not DARK_MODE
    DARK_MODE = MANUAL_DARK_MODE
    
    # Update theme colors
    if DARK_MODE:
        # Dark theme colors
        UI_BACKGROUND_COLOR = "#333333"
        UI_TEXT_COLOR = "#FFFFFF"
        UI_SECONDARY_TEXT_COLOR = "#CCCCCC"
        UI_HELP_TEXT_COLOR = "#AAAAAA"
        UI_BUTTON_PAUSE_COLOR = "#444444"
        UI_TOOLTIP_BACKGROUND_COLOR = "#555555"
        UI_TOOLTIP_TEXT_COLOR = "#FFFFFF"
    else:
        # Light theme colors
        UI_BACKGROUND_COLOR = "#F0F0F0"
        UI_TEXT_COLOR = "#000000"
        UI_SECONDARY_TEXT_COLOR = "#333333"
        UI_HELP_TEXT_COLOR = "#555555"
        UI_BUTTON_PAUSE_COLOR = "#DDDDDD"
        UI_TOOLTIP_BACKGROUND_COLOR = "#FFFFCC"
        UI_TOOLTIP_TEXT_COLOR = "#000000"
    
    return DARK_MODE

# Detection settings
MATCH_THRESHOLD = 0.6  # Threshold for considering a match (0-1)
SCAN_INTERVAL = 2  # Time between scans in seconds

# Key settings
ESC_DETECTION_WINDOW = 2  # Seconds in which ESC keys must be pressed
ESC_COUNT_THRESHOLD = 3  # Number of ESC presses to show dialog
ESC_RESET_TIMEOUT = 5  # Seconds after which the ESC counter resets if not reaching threshold

# Resource paths
def get_assets_path(filename):
    """Gets the full path to a file in the assets folder."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', filename)

ICON_PATH = get_assets_path('icon.ico')
# List of button templates to search for
BUTTON_TEMPLATES = [
    get_assets_path('button.png'),
    get_assets_path('button2.png')
    # Add more button templates as needed
]

# Theme icons (Unicode symbols)
DARK_THEME_ICON = "🌙"  # Moon for dark mode
LIGHT_THEME_ICON = "☀️"  # Sun for light mode
