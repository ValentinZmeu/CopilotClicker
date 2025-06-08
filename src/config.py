import os

# Configuración de la aplicación
APP_NAME = "CopilotClicker"
APP_ID = "CopilotClicker"  # Para Windows (AppUserModelID)

# Configuración de la interfaz de usuario
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

# Configuración de la detección
MATCH_THRESHOLD = 0.8  # Umbral para considerar coincidencia (0-1)
SCAN_INTERVAL = 0.5  # Tiempo entre escaneos en segundos

# Configuración de teclas
ESC_DETECTION_WINDOW = 2  # Segundos en los que deben pulsarse las teclas ESC
ESC_COUNT_THRESHOLD = 3  # Número de pulsaciones ESC para mostrar diálogo

# Rutas de recursos
def get_assets_path(filename):
    """Obtiene la ruta completa a un archivo en la carpeta assets."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', filename)

ICON_PATH = get_assets_path('icon.ico')
BUTTON_TEMPLATE_PATH = get_assets_path('button.png')
