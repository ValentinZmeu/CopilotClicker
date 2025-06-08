import cv2
import numpy as np
import pyautogui
import time
from . import config

class ButtonDetector:
    """Clase para detectar botones en la pantalla usando template matching."""
    
    def __init__(self):
        """Inicializa el detector de botones."""
        # Carga la imagen del botón
        self.template = cv2.imread(config.BUTTON_TEMPLATE_PATH, cv2.IMREAD_COLOR)
        if self.template is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen del botón: {config.BUTTON_TEMPLATE_PATH}")
        
        self.h, self.w = self.template.shape[:2]
    
    def find_and_click_button(self):
        """Busca el botón en la pantalla y hace clic si lo encuentra."""
        try:
            # Captura la pantalla y convierte a formato OpenCV
            screenshot = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Búsqueda por template matching
            result = cv2.matchTemplate(img, self.template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # Si la coincidencia supera umbral, mover el ratón y clic
            if max_val >= config.MATCH_THRESHOLD:
                center_x = max_loc[0] + self.w // 2
                center_y = max_loc[1] + self.h // 2
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()
                return True
            
            return False
        except Exception as e:
            print(f"Error al buscar el botón: {e}")
            return False
