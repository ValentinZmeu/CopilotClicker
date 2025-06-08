import tkinter as tk
import platform
import os
from . import config

# Variables globales para la interfaz de usuario
running = True
paused = False
esc_count = 0
last_esc_time = 0
confirm_window = None
status_label = None

def set_icon(window, icon_path):
    """Establece el icono de la aplicación de forma compatible con múltiples plataformas."""
    if os.path.exists(icon_path):
        try:
            # En Windows
            if platform.system() == "Windows":
                window.iconbitmap(icon_path)
                # También establecer el icono en la barra de tareas
                try:
                    from ctypes import windll
                    windll.shell32.SetCurrentProcessExplicitAppUserModelID(config.APP_ID)
                except:
                    pass  # Si falla, continuamos sin el icono en la barra de tareas
            # En macOS o Linux
            elif platform.system() in ["Darwin", "Linux"]:
                # Intentar cargar el icono como imagen y establecerlo
                try:
                    import PIL.Image
                    import PIL.ImageTk
                    img = PIL.Image.open(icon_path)
                    icon = PIL.ImageTk.PhotoImage(img)
                    window.tk.call('wm', 'iconphoto', window._w, icon)
                except:
                    pass  # Si falla, continuamos sin icono
        except:
            pass  # Si falla cualquier parte, seguimos sin el icono

def center_window(window, width, height):
    """Centra la ventana en la pantalla."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def show_confirm_dialog():
    """Muestra un diálogo de confirmación para detener la aplicación."""
    global paused, confirm_window, running
    
    # Pausar la ejecución mientras se muestra el diálogo
    paused = True
    
    # Evitar crear múltiples ventanas de confirmación
    if confirm_window is not None:
        return
    
    # Crear ventana de confirmación
    confirm_window = tk.Toplevel()
    confirm_window.title(f"{config.APP_NAME} - Confirmación")
    
    # Configurar el tamaño de la ventana
    window_width = 300
    window_height = 150
    
    # Centrar ventana
    center_window(confirm_window, window_width, window_height)
    
    # Establecer el icono de la aplicación
    set_icon(confirm_window, config.ICON_PATH)
    
    confirm_window.attributes("-topmost", True)
    confirm_window.configure(bg=config.UI_BACKGROUND_COLOR)
    
    # Mensaje de confirmación
    confirm_label = tk.Label(
        confirm_window,
        text="¿Desea detener CopilotClicker?",
        fg=config.UI_TEXT_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 12)
    )
    confirm_label.pack(pady=20)
    
    # Frame para los botones
    button_frame = tk.Frame(confirm_window, bg=config.UI_BACKGROUND_COLOR)
    button_frame.pack(pady=10)
    
    # Función para confirmar y detener
    def confirm_exit():
        global running, paused, confirm_window
        running = False
        paused = False
        confirm_window.destroy()
        confirm_window = None
    
    # Función para cancelar y continuar
    def cancel_exit():
        global paused, confirm_window
        paused = False
        confirm_window.destroy()
        confirm_window = None
    
    # Botones de confirmación
    yes_button = tk.Button(
        button_frame,
        text="Sí",
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
    
    # Dar foco al botón Sí
    yes_button.focus_set()
    
    # Manejar cierre de ventana con el botón X
    confirm_window.protocol("WM_DELETE_WINDOW", cancel_exit)

def create_info_window():
    """Crea y gestiona la ventana principal de información."""
    global status_label, paused
    
    window = tk.Tk()
    window.title(config.APP_NAME)
    
    # Configurar y centrar la ventana
    center_window(window, config.UI_WINDOW_WIDTH, config.UI_WINDOW_HEIGHT)
    
    # Establecer el icono de la aplicación
    set_icon(window, config.ICON_PATH)
    
    window.attributes("-alpha", 1.0)   # Sin transparencia
    window.attributes("-topmost", True)  # Siempre visible
    window.configure(bg=config.UI_BACKGROUND_COLOR)
    
    # Título con el texto de información
    title_label = tk.Label(
        window, 
        text=config.APP_NAME,
        fg=config.UI_TEXT_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 16, "bold")
    )
    title_label.pack(pady=(15, 5))
    
    # Descripción de la aplicación
    desc_label = tk.Label(
        window, 
        text="Automatización para GitHub Copilot",
        fg=config.UI_SECONDARY_TEXT_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 10)
    )
    desc_label.pack(pady=(0, 10))
    
    # Etiqueta de estado
    status_label = tk.Label(
        window, 
        text="Ejecutando - Buscando botón de continuar...",
        fg=config.UI_RUNNING_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 9)
    )
    status_label.pack(pady=(0, 10))
    
    # Frame para los botones
    button_frame = tk.Frame(window, bg=config.UI_BACKGROUND_COLOR)
    button_frame.pack(pady=10)
    
    # Función para el botón de pausa/reanudar
    def toggle_pause():
        global paused
        paused = not paused
        if paused:
            pause_button.config(text="▶ Reanudar")
            status_label.config(text="Pausado", fg=config.UI_PAUSED_COLOR)
        else:
            pause_button.config(text="⏸ Pausar")
            status_label.config(text="Ejecutando - Buscando botón de continuar...", fg=config.UI_RUNNING_COLOR)
    
    # Función para el botón detener
    def stop_app():
        show_confirm_dialog()
    
    # Botón de pausa/reanudar
    pause_button = tk.Button(
        button_frame,
        text="⏸ Pausar",
        command=toggle_pause,
        width=12,
        bg=config.UI_BUTTON_PAUSE_COLOR,
        fg=config.UI_TEXT_COLOR,
        relief=tk.FLAT
    )
    pause_button.pack(side=tk.LEFT, padx=5)
    
    # Botón de detener
    stop_button = tk.Button(
        button_frame,
        text="⏹ Detener",
        command=stop_app,
        width=12,
        bg=config.UI_BUTTON_STOP_COLOR,
        fg=config.UI_TEXT_COLOR,
        relief=tk.FLAT
    )
    stop_button.pack(side=tk.LEFT, padx=5)
    
    # Información de ayuda
    help_label = tk.Label(
        window, 
        text=f"Presiona ESC {config.ESC_COUNT_THRESHOLD} veces para detener",
        fg=config.UI_HELP_TEXT_COLOR,
        bg=config.UI_BACKGROUND_COLOR,
        font=("Arial", 9)
    )
    help_label.pack(pady=(5, 0))
    
    # Función para manejar el cierre de la ventana
    def on_close():
        show_confirm_dialog()
    
    window.protocol("WM_DELETE_WINDOW", on_close)
    
    # Actualizar estado
    def update_status():
        if running:
            window.after(500, update_status)
        else:
            window.destroy()
    
    update_status()
    window.mainloop()

def is_paused():
    """Retorna si la aplicación está pausada."""
    return paused

def is_running():
    """Retorna si la aplicación está en ejecución."""
    return running

def check_esc(current_time):
    """Manejador de evento de teclado para detectar ESC."""
    global esc_count, last_esc_time
    
    # Resetear contador si ha pasado más de X segundos
    if current_time - last_esc_time > config.ESC_DETECTION_WINDOW:
        esc_count = 0
    
    esc_count += 1
    last_esc_time = current_time
    
    if esc_count >= config.ESC_COUNT_THRESHOLD:
        show_confirm_dialog()
        return True
    
    return False
