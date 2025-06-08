import cv2
import numpy as np
import pyautogui
import time
from . import config

class ButtonDetector:
    """Class for detecting buttons on the screen using template matching."""
    
    def __init__(self):
        """Initialize the button detector."""
        # Load the button image
        self.template = cv2.imread(config.BUTTON_TEMPLATE_PATH, cv2.IMREAD_COLOR)
        if self.template is None:
            raise FileNotFoundError(f"Could not load the button image: {config.BUTTON_TEMPLATE_PATH}")
        
        self.h, self.w = self.template.shape[:2]
    
    def find_and_click_button(self):
        """Find the button on the screen and click it if found."""
        try:
            # Capture the screen and convert to OpenCV format
            screenshot = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Search using template matching
            result = cv2.matchTemplate(img, self.template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            # If the match exceeds threshold, move the mouse and click
            if max_val >= config.MATCH_THRESHOLD:
                center_x = max_loc[0] + self.w // 2
                center_y = max_loc[1] + self.h // 2
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()
                return True
            
            return False
        except Exception as e:
            print(f"Error while searching for the button: {e}")
            return False
