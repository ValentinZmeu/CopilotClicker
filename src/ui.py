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
main_window = None
reset_timer_id = None

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
    
    # Make the window appear as an alert
    confirm_window.attributes("-topmost", True)
    confirm_window.lift()  # Bring window to the front
    confirm_window.focus_force()  # Force focus
    confirm_window.grab_set()  # Make the window modal
    confirm_window.configure(bg=config.UI_BACKGROUND_COLOR)
    
    # Play alert sound
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        elif platform.system() == "Darwin":  # macOS
            os.system("afplay /System/Library/Sounds/Sosumi.aiff")
        elif platform.system() == "Linux":
            os.system("paplay /usr/share/sounds/freedesktop/stereo/dialog-warning.oga")
    except Exception as e:
        print(f"Could not play alert sound: {e}")
    
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
        width=10,
        bg=config.UI_BUTTON_PAUSE_COLOR,
        fg=config.UI_TEXT_COLOR,
        relief=tk.FLAT
    )
    yes_button.pack(side=tk.LEFT, padx=10)
    
    no_button = tk.Button(
        button_frame,
        text="No",
        command=cancel_exit,
        width=10,
        bg=config.UI_BUTTON_PAUSE_COLOR,
        fg=config.UI_TEXT_COLOR,
        relief=tk.FLAT
    )
    no_button.pack(side=tk.LEFT, padx=10)
      # Focus on Yes button
    yes_button.focus_set()
      # Handle keyboard navigation between buttons
    def handle_key(event):
        if event.keysym in ['Left', 'Right']:
            # Switch focus between Yes and No buttons
            if confirm_window.focus_get() == yes_button:
                no_button.focus_set()
            else:
                yes_button.focus_set()
        elif event.keysym == 'Return':
            # Execute the action of the button that has focus
            if confirm_window.focus_get() == yes_button:
                confirm_exit()
            elif confirm_window.focus_get() == no_button:
                cancel_exit()
        
    # Bind left/right arrow keys to handle_key function
    confirm_window.bind('<Left>', handle_key)
    confirm_window.bind('<Right>', handle_key)
    confirm_window.bind('<Return>', handle_key)
    
    # Handle window close with X button
    confirm_window.protocol("WM_DELETE_WINDOW", cancel_exit)

def create_tooltip(widget, text):
    """Creates a tooltip for a given widget."""
    tooltip_window = None
    
    def show_tooltip(event):
        nonlocal tooltip_window
        # Create a new window for the tooltip
        tooltip_window = tk.Toplevel(main_window)
        tooltip_window.wm_overrideredirect(True)  # No window decorations
        tooltip_window.configure(bg=config.UI_TOOLTIP_BACKGROUND_COLOR)
        
        # Make tooltip appear in front of all windows
        tooltip_window.attributes("-topmost", True)
        tooltip_window.lift()
        
        # Add text to the tooltip
        label = tk.Label(
            tooltip_window,
            text=text,
            fg=config.UI_TOOLTIP_TEXT_COLOR,
            bg=config.UI_TOOLTIP_BACKGROUND_COLOR,
            font=("Arial", 10)
        )
        label.pack(padx=5, pady=5)
        
        # Position the tooltip window
        x = event.x_root + 10
        y = event.y_root + 10
        tooltip_window.wm_geometry(f"+{x}+{y}")
    
    def hide_tooltip(event):
        nonlocal tooltip_window
        if tooltip_window:
            tooltip_window.destroy()
            tooltip_window = None
    
    # Bind mouse events to show/hide the tooltip
    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)

def create_info_window():
    """Creates and manages the main information window."""
    global status_label, paused, main_window
    
    main_window = tk.Tk()
    window = main_window
    window.title(config.APP_NAME)
      # Configure and center the window
    center_window(window, config.UI_WINDOW_WIDTH, config.UI_WINDOW_HEIGHT)
    
    # Set minimum window size to ensure all elements are visible
    window.minsize(config.UI_WINDOW_MIN_WIDTH, config.UI_WINDOW_MIN_HEIGHT)
    
    # Set application icon
    set_icon(window, config.ICON_PATH)
    
    window.attributes("-alpha", 1.0)   # No transparency
    window.attributes("-topmost", True)  # Always visible
    window.configure(bg=config.UI_BACKGROUND_COLOR)
    
    # Top frame for title
    top_frame = tk.Frame(window, bg=config.UI_BACKGROUND_COLOR)
    top_frame.pack(fill=tk.X, pady=(10, 0))
      # Title with information text
    title_label = tk.Label(
        top_frame, 
        text=config.APP_NAME,
        fg=config.UI_TEXT_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 16, "bold")
    )
    title_label.pack(expand=True)  # Center the title
    
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
    
    # Frame for main buttons
    button_frame = tk.Frame(window, bg=config.UI_BACKGROUND_COLOR)
    button_frame.pack(pady=10)
    
    # Function to update UI colors when theme changes
    def update_ui_theme():
        # Update all widgets with new theme colors
        window.configure(bg=config.UI_BACKGROUND_COLOR)
        top_frame.configure(bg=config.UI_BACKGROUND_COLOR)
        title_label.configure(
            fg=config.UI_TEXT_COLOR,
            bg=config.UI_BACKGROUND_COLOR
        )
        desc_label.configure(
            fg=config.UI_SECONDARY_TEXT_COLOR,
            bg=config.UI_BACKGROUND_COLOR
        )
        status_label.configure(
            bg=config.UI_BACKGROUND_COLOR
        )
        button_frame.configure(bg=config.UI_BACKGROUND_COLOR)
        help_label.configure(
            fg=config.UI_HELP_TEXT_COLOR,
            bg=config.UI_BACKGROUND_COLOR
        )
        bottom_frame.configure(bg=config.UI_BACKGROUND_COLOR)
        
        # Update buttons
        pause_button.configure(
            bg=config.UI_BUTTON_PAUSE_COLOR,
            fg=config.UI_TEXT_COLOR
        )
        stop_button.configure(
            fg=config.UI_TEXT_COLOR
        )
        
        # Update theme toggle button icon
        theme_toggle_button.configure(
            text=config.LIGHT_THEME_ICON if config.DARK_MODE else config.DARK_THEME_ICON,
            bg=config.UI_BACKGROUND_COLOR,
            fg=config.UI_TEXT_COLOR
        )
    
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
    
    # Function to toggle theme
    def toggle_theme_handler():
        config.toggle_theme()
        update_ui_theme()
    
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
    
    # Create tooltip for pause button
    create_tooltip(pause_button, "Pause/resume the automatic clicking")
    
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
    
    # Create tooltip for stop button
    create_tooltip(stop_button, "Stop the application")
    
    # Help information
    help_label = tk.Label(
        window, 
        text=f"Press ESC {config.ESC_COUNT_THRESHOLD} times to stop",
        fg=config.UI_HELP_TEXT_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 9)
    )
    help_label.pack(pady=(5, 0))
    
    # Bottom frame for theme toggle
    bottom_frame = tk.Frame(window, bg=config.UI_BACKGROUND_COLOR)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)    # Theme toggle button at the bottom
    theme_toggle_button = tk.Button(
        bottom_frame,
        text=config.LIGHT_THEME_ICON if config.DARK_MODE else config.DARK_THEME_ICON,
        command=toggle_theme_handler,
        font=("Arial", 12),
        bg=config.UI_BACKGROUND_COLOR,
        fg=config.UI_TEXT_COLOR,
        relief=tk.SOLID,  # Solid border
        borderwidth=1,    # Thin border
        highlightthickness=0,
        padx=5,           # Small horizontal padding
        pady=0,           # No vertical padding for 8px height
        width=2,          # Make button smaller by setting fixed width
        height=0,         # Set to 0 to control height manually
        cursor="hand2"    # Hand cursor on hover
    )
    # Configure button to have exactly 8px height
    theme_toggle_button.configure(font=("Arial", 8))
    theme_toggle_button.pack(side=tk.RIGHT, padx=10)
    
    # Make the button corners rounded (on Windows)
    if platform.system() == "Windows":
        try:
            from ctypes import windll, byref, sizeof, Structure, c_int
            
            class POINT(Structure):
                _fields_ = [("x", c_int), ("y", c_int)]
            
            # Round the corners of the button (Windows-specific)
            hwnd = windll.user32.GetParent(windll.user32.GetDlgItem(theme_toggle_button.winfo_id(), 0))
            windll.user32.SetWindowRgn(hwnd, windll.gdi32.CreateRoundRectRgn(0, 0, 30, 30, 15, 15), True)
        except:
            pass  # If this fails, the button will have normal corners
    
    # Create tooltip for theme toggle button
    create_tooltip(theme_toggle_button, "Toggle between light and dark mode")
    
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
    global esc_count, last_esc_time, reset_timer_id, main_window
    
    # Reset counter if more than X seconds have passed since the last press
    if current_time - last_esc_time > config.ESC_DETECTION_WINDOW:
        esc_count = 0
    
    # Cancel any existing reset timer
    if reset_timer_id and main_window:
        main_window.after_cancel(reset_timer_id)
        reset_timer_id = None
    
    esc_count += 1
    last_esc_time = current_time
    
    # Start timer to reset counter if threshold not reached within timeout period
    if main_window and esc_count < config.ESC_COUNT_THRESHOLD:
        def reset_counter_if_not_reached():
            global esc_count, reset_timer_id
            # Only reset if counter hasn't reached threshold after timeout
            if 0 < esc_count < config.ESC_COUNT_THRESHOLD:
                print(f"ESC counter reset after {config.ESC_RESET_TIMEOUT} seconds timeout")
                esc_count = 0
            reset_timer_id = None
        
        # Schedule reset after timeout period
        reset_timer_id = main_window.after(config.ESC_RESET_TIMEOUT * 1000, reset_counter_if_not_reached)
    
    if esc_count >= config.ESC_COUNT_THRESHOLD:
        show_confirm_dialog()
        # Reset counter after showing dialog
        esc_count = 0
        return True
    
    return False
