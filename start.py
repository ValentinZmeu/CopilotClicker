import cv2
import numpy as np
import pyautogui
import time

# Carga la imagen del botón (guárdala como "button.png" en el mismo directorio)
template = cv2.imread('button.png', cv2.IMREAD_COLOR)
h, w = template.shape[:2]

while True:
    # Captura la pantalla y convierte a formato OpenCV
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Búsqueda por template matching
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Si la coincidencia supera umbral, mover el ratón y clic
    if max_val >= 0.8:
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()

    time.sleep(2)
