﻿# -*- coding: utf-8 -*-
import time
import threading
import keyboard
import os
import sys

# Make sure the main directory is in the path
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import application modules
from src import ui, detector, config


def main():
    """Main function that starts the application."""
    # Create the button detector
    button_detector = detector.ButtonDetector()

    # Configure ESC key detection
    keyboard.on_press_key("esc", lambda _: ui.check_esc(time.time()))

    # Start information window in a separate thread
    info_thread = threading.Thread(target=ui.create_info_window)
    info_thread.daemon = True
    info_thread.start()

    # Main loop
    while ui.is_running():
        try:
            # If paused, wait and continue to the next cycle
            if ui.is_paused():
                time.sleep(0.1)
                continue

            # Find and click the button if found
            button_detector.find_and_click_button()

            # Wait before the next check
            time.sleep(config.SCAN_INTERVAL)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

    print(f"{config.APP_NAME} has stopped.")


if __name__ == "__main__":
    main()