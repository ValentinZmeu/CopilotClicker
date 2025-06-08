import tkinter as tk
import platform
import os
from . import config

# Global variables for the user interface
running = True
paused = False
esc_count = 0
last_esc_time = 0
confirm_window = None
status_label = None

def set_icon(window, icon_path):
    """Sets the application icon in a way compatible with multiple platforms."""
    if os.path.exists(icon_path):
        try:
            # On Windows
            if platform.system() == "Windows":
                window.iconbitmap(icon_path)
                # Also set the icon in the taskbar
                try:
                    from ctypes import windll
                    windll.shell32.SetCurrentProcessExplicitAppUserModelID(config.APP_ID)
                except:
                    pass  # If it fails, continue without the taskbar icon
            # On macOS or Linux
            elif platform.system() in ["Darwin", "Linux"]:
                # Try to load the icon as an image and set it
                try:
                    import PIL.Image
                    import PIL.ImageTk
                    img = PIL.Image.open(icon_path)
                    icon = PIL.ImageTk.PhotoImage(img)
                    window.tk.call('wm', 'iconphoto', window._w, icon)
                except:
                    pass  # If it fails, continue without icon
        except:
            pass  # If any part fails, continue without the icon

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def show_confirm_dialog():
    """Shows a confirmation dialog to stop the application."""
    global paused, confirm_window, running
    
    # Pause execution while showing the dialog
    paused = True
    
    # Avoid creating multiple confirmation windows
    if confirm_window is not None:
        return
    
    # Create confirmation window
    confirm_window = tk.Toplevel()
    confirm_window.title(f"{config.APP_NAME} - Confirmation")
    
    # Configure window size
    window_width = 300
    window_height = 150
    
    # Center window
    center_window(confirm_window, window_width, window_height)
    
    # Set application icon
    set_icon(confirm_window, config.ICON_PATH)
    
    confirm_window.attributes("-topmost", True)
    confirm_window.configure(bg=config.UI_BACKGROUND_COLOR)
    
    # Confirmation message
    confirm_label = tk.Label(
        confirm_window,
        text="Do you want to stop CopilotClicker?",
        fg=config.UI_TEXT_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 12)
    )
    confirm_label.pack(pady=20)
    
    # Frame for buttons
    button_frame = tk.Frame(confirm_window, bg=config.UI_BACKGROUND_COLOR)
    button_frame.pack(pady=10)
    
    # Function to confirm and stop
    def confirm_exit():
        global running, paused, confirm_window
        running = False
        paused = False
        confirm_window.destroy()
        confirm_window = None
    
    # Function to cancel and continue
    def cancel_exit():
        global paused, confirm_window
        paused = False
        confirm_window.destroy()
        confirm_window = None
    
    # Confirmation buttons
    yes_button = tk.Button(
        button_frame,
        text="Yes",
        command=confirm_exit,
        width=10
    )
    yes_button.pack(side=tk.LEFT, padx=10)
    
    no_button = tk.Button(
        button_frame,
        text="No",
        command=cancel_exit,
        width=10
    )
    no_button.pack(side=tk.LEFT, padx=10)
    
    # Focus on Yes button
    yes_button.focus_set()
    
    # Handle window close with X button
    confirm_window.protocol("WM_DELETE_WINDOW", cancel_exit)

def create_info_window():
    """Creates and manages the main information window."""
    global status_label, paused
    
    window = tk.Tk()
    window.title(config.APP_NAME)
    
    # Configure and center the window
    center_window(window, config.UI_WINDOW_WIDTH, config.UI_WINDOW_HEIGHT)
    
    # Set application icon
    set_icon(window, config.ICON_PATH)
    
    window.attributes("-alpha", 1.0)   # No transparency
    window.attributes("-topmost", True)  # Always visible
    window.configure(bg=config.UI_BACKGROUND_COLOR)
    
    # Title with information text
    title_label = tk.Label(
        window, 
        text=config.APP_NAME,
        fg=config.UI_TEXT_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 16, "bold")
    )
    title_label.pack(pady=(15, 5))
    
    # Application description
    desc_label = tk.Label(
        window, 
        text="Automation for GitHub Copilot",
        fg=config.UI_SECONDARY_TEXT_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 10)
    )
    desc_label.pack(pady=(0, 10))
    
    # Status label
    status_label = tk.Label(
        window, 
        text="Running - Searching for continue button...",
        fg=config.UI_RUNNING_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 9)
    )
    status_label.pack(pady=(0, 10))
    
    # Frame for buttons
    button_frame = tk.Frame(window, bg=config.UI_BACKGROUND_COLOR)
    button_frame.pack(pady=10)
    
    # Function for pause/resume button
    def toggle_pause():
        global paused
        paused = not paused
        if paused:
            pause_button.config(text="▶ Resume")
            status_label.config(text="Paused", fg=config.UI_PAUSED_COLOR)
        else:
            pause_button.config(text="⏸ Pause")
            status_label.config(text="Running - Searching for continue button...", fg=config.UI_RUNNING_COLOR)
    
    # Function for stop button
    def stop_app():
        show_confirm_dialog()
    
    # Pause/resume button
    pause_button = tk.Button(
        button_frame,
        text="⏸ Pause",
        command=toggle_pause,
        width=12,
        bg=config.UI_BUTTON_PAUSE_COLOR,
        fg=config.UI_TEXT_COLOR,
        relief=tk.FLAT
    )
    pause_button.pack(side=tk.LEFT, padx=5)
    
    # Stop button
    stop_button = tk.Button(
        button_frame,
        text="⏹ Stop",
        command=stop_app,
        width=12,
        bg=config.UI_BUTTON_STOP_COLOR,
        fg=config.UI_TEXT_COLOR,
        relief=tk.FLAT
    )
    stop_button.pack(side=tk.LEFT, padx=5)
    
    # Help information
    help_label = tk.Label(
        window, 
        text=f"Press ESC {config.ESC_COUNT_THRESHOLD} times to stop",
        fg=config.UI_HELP_TEXT_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 9)
    )
    help_label.pack(pady=(5, 0))
    
    # Function to handle window close
    def on_close():
        show_confirm_dialog()
    
    window.protocol("WM_DELETE_WINDOW", on_close)
    
    # Update status
    def update_status():
        if running:
            window.after(500, update_status)
        else:
            window.destroy()
    
    update_status()
    window.mainloop()

def is_paused():
    """Returns whether the application is paused."""
    return paused

def is_running():
    """Returns whether the application is running."""
    return running

def check_esc(current_time):
    """Keyboard event handler to detect ESC."""
    global esc_count, last_esc_time
    
    # Reset counter if more than X seconds have passed
    if current_time - last_esc_time > config.ESC_DETECTION_WINDOW:
        esc_count = 0
    
    esc_count += 1
    last_esc_time = current_time
    
    if esc_count >= config.ESC_COUNT_THRESHOLD:
        show_confirm_dialog()
        return True
    
    return False
