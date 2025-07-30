import cv2
import numpy as np
import pyautogui
import time
import os
from . import config

class ButtonDetector:
    """Class for detecting buttons on the screen using template matching."""
    
    def __init__(self):
        """Initialize the button detector."""
        # Load the button templates
        self.templates = []
        self.templates_sizes = []
        self.template_names = []
        
        for template_path in config.BUTTON_TEMPLATES:
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                print(f"Warning: Could not load the button image: {template_path}")
                continue
                
            self.templates.append(template)
            self.templates_sizes.append(template.shape[:2])  # (height, width)
            self.template_names.append(os.path.basename(template_path))
            
        if not self.templates:
            raise FileNotFoundError("Could not load any button templates")
        
        print(f"Loaded {len(self.templates)} button templates to click: {', '.join(self.template_names)}")
            
        # Load templates of buttons to avoid
        self.avoid_templates = []
        self.avoid_templates_sizes = []
        self.avoid_template_names = []
        
        for avoid_path in config.AVOID_BUTTON_TEMPLATES:
            avoid_template = cv2.imread(avoid_path, cv2.IMREAD_COLOR)
            if avoid_template is None:
                print(f"Warning: Could not load the avoid button image: {avoid_path}")
                continue
                
            self.avoid_templates.append(avoid_template)
            self.avoid_templates_sizes.append(avoid_template.shape[:2])  # (height, width)
            self.avoid_template_names.append(os.path.basename(avoid_path))
        
        if self.avoid_templates:
            print(f"Loaded {len(self.avoid_templates)} button templates to avoid: {', '.join(self.avoid_template_names)}")
        else:
            print("No avoid button templates loaded.")
    
    def is_avoid_button_present(self, img, x, y, w, h):
        """Check if any of the avoid buttons are present at the given location."""
        # Define a region around the detected button to check for avoid buttons
        # Use a slightly larger region to account for positioning differences
        region_x = max(0, x - 10)
        region_y = max(0, y - 10)
        region_w = w + 20
        region_h = h + 20
        
        # Make sure the region doesn't exceed image dimensions
        img_h, img_w = img.shape[:2]
        region_w = min(region_w, img_w - region_x)
        region_h = min(region_h, img_h - region_y)
        
        # Extract the region of interest
        roi = img[region_y:region_y+region_h, region_x:region_x+region_w]
        
        # Check each avoid template
        for idx, avoid_template in enumerate(self.avoid_templates):
            # Skip if the template is larger than the ROI
            if avoid_template.shape[0] > roi.shape[0] or avoid_template.shape[1] > roi.shape[1]:
                continue
                
            # Template matching in the ROI
            result = cv2.matchTemplate(roi, avoid_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            
            # If a close match is found, consider it as an avoid button
            if max_val >= config.MATCH_THRESHOLD:
                print(f"Avoid button detected! Match value: {max_val:.2f}")
                return True
                
        return False
    
    def find_and_click_button(self):
        """Find the button on the screen and click it if found."""
        try:
            # Capture the screen and convert to OpenCV format
            screenshot = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            best_match = None
            best_val = 0
            best_loc = None
            best_template_idx = -1

            # Search using template matching for each template
            for idx, template in enumerate(self.templates):
                result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)
                
                if max_val > best_val:
                    best_val = max_val
                    best_loc = max_loc
                    best_template_idx = idx

            # If the best match exceeds threshold, check if it should be avoided
            if best_val >= config.MATCH_THRESHOLD and best_template_idx >= 0:
                h, w = self.templates_sizes[best_template_idx]
                x, y = best_loc
                
                # Check if this button should be avoided
                if self.avoid_templates and self.is_avoid_button_present(img, x, y, w, h):
                    print(f"Found a button that should be avoided. Skipping click.")
                    return False
                
                # Button is safe to click
                center_x = x + w // 2
                center_y = y + h // 2
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()
                return True
            
            return False
        except Exception as e:
            print(f"Error while searching for the button: {e}")
            return False
