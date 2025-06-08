import cv2
import numpy as np
import pyautogui
import time
import tkinter as tk
import threading
import keyboard
import os
import sys
import platform

# Variables globales
running = True
paused = False
esc_count = 0
last_esc_time = 0
confirm_window = None
status_label = None

# Función para crear y gestionar la ventana de información
def create_info_window():
    global status_label, paused
    
    window = tk.Tk()
    window.title("CopilotClicker")
    
    # Configurar el tamaño de la ventana
    window_width = 300
    window_height = 200
    
    # Obtener dimensiones de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
      # Calcular posición para centrar la ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2    # Configurar geometría y ubicación
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Establecer el icono de la aplicación
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
    if os.path.exists(icon_path):
        try:
            # En Windows
            if platform.system() == "Windows":
                window.iconbitmap(icon_path)
                # También establecer el icono en la barra de tareas
                try:
                    from ctypes import windll
                    windll.shell32.SetCurrentProcessExplicitAppUserModelID("CopilotClicker")
                except:
                    pass  # Si falla, continuamos sin el icono en la barra de tareas
            # En macOS o Linux
            elif platform.system() in ["Darwin", "Linux"]:
                # Intentar cargar el icono como imagen y establecerlo (no funciona en todos los gestores de ventanas)
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
    
    window.attributes("-alpha", 1.0)   # Sin transparencia (completamente opaco)
    window.attributes("-topmost", True)  # Siempre visible
    window.configure(bg="#333333")
    
    # Título con el texto de información
    title_label = tk.Label(
        window, 
        text="CopilotClicker",
        fg="white",
        bg="#333333",
        font=("Arial", 16, "bold")
    )
    title_label.pack(pady=(15, 5))
    
    # Descripción de la aplicación
    desc_label = tk.Label(
        window, 
        text="Automatización para GitHub Copilot",
        fg="#cccccc",
        bg="#333333",
        font=("Arial", 10)
    )
    desc_label.pack(pady=(0, 10))
    
    # Etiqueta de estado
    status_label = tk.Label(
        window, 
        text="Ejecutando - Buscando botón de continuar...",
        fg="#00ff00",
        bg="#333333",
        font=("Arial", 9)
    )
    status_label.pack(pady=(0, 10))
    
    # Frame para los botones
    button_frame = tk.Frame(window, bg="#333333")
    button_frame.pack(pady=10)
    
    # Función para el botón de pausa/reanudar
    def toggle_pause():
        global paused
        paused = not paused
        if paused:
            pause_button.config(text="▶ Reanudar")
            status_label.config(text="Pausado", fg="#ffcc00")
        else:
            pause_button.config(text="⏸ Pausar")
            status_label.config(text="Ejecutando - Buscando botón de continuar...", fg="#00ff00")
    
    # Función para el botón detener
    def stop_app():
        show_confirm_dialog()
    
    # Botón de pausa/reanudar
    pause_button = tk.Button(
        button_frame,
        text="⏸ Pausar",
        command=toggle_pause,
        width=12,
        bg="#444444",
        fg="white",
        relief=tk.FLAT
    )
    pause_button.pack(side=tk.LEFT, padx=5)
    
    # Botón de detener
    stop_button = tk.Button(
        button_frame,
        text="⏹ Detener",
        command=stop_app,
        width=12,
        bg="#aa3333",
        fg="white",
        relief=tk.FLAT
    )
    stop_button.pack(side=tk.LEFT, padx=5)
    
    # Información de ayuda
    help_label = tk.Label(
        window, 
        text="Presiona ESC 3 veces para detener",
        fg="#aaaaaa",
        bg="#333333",
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

# Manejador de evento de teclado para detectar ESC
def check_esc():
    global esc_count, last_esc_time, running
    
    current_time = time.time()
    # Resetear contador si ha pasado más de 2 segundos
    if current_time - last_esc_time > 2:
        esc_count = 0
    
    esc_count += 1
    last_esc_time = current_time
    
    if esc_count >= 3:
        show_confirm_dialog()
        return True
    
    return False

# Función para mostrar diálogo de confirmación
def show_confirm_dialog():
    global paused, confirm_window, running
    
    # Pausar la ejecución mientras se muestra el diálogo
    paused = True
    
    # Evitar crear múltiples ventanas de confirmación
    if confirm_window is not None:
        return      # Crear ventana de confirmación
    confirm_window = tk.Toplevel()
    confirm_window.title("CopilotClicker - Confirmación")
    
    # Configurar el tamaño de la ventana
    window_width = 300
    window_height = 150
    
    # Obtener dimensiones de la pantalla
    screen_width = confirm_window.winfo_screenwidth()
    screen_height = confirm_window.winfo_screenheight()
      # Calcular posición para centrar la ventana
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2    # Configurar geometría y ubicación
    confirm_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Establecer el icono de la aplicación
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
    if os.path.exists(icon_path):
        try:
            # En Windows
            if platform.system() == "Windows":
                confirm_window.iconbitmap(icon_path)
            # En macOS o Linux
            elif platform.system() in ["Darwin", "Linux"]:
                # Intentar cargar el icono como imagen y establecerlo
                try:
                    import PIL.Image
                    import PIL.ImageTk
                    img = PIL.Image.open(icon_path)
                    icon = PIL.ImageTk.PhotoImage(img)
                    confirm_window.tk.call('wm', 'iconphoto', confirm_window._w, icon)
                except:
                    pass  # Si falla, continuamos sin icono
        except:
            pass  # Si falla cualquier parte, seguimos sin el icono
    
    confirm_window.attributes("-topmost", True)
    confirm_window.configure(bg="#333333")
    
    # Mensaje de confirmación
    confirm_label = tk.Label(
        confirm_window,
        text="¿Desea detener CopilotClicker?",
        fg="white",
        bg="#333333",
        font=("Arial", 12)
    )
    confirm_label.pack(pady=20)
    
    # Frame para los botones
    button_frame = tk.Frame(confirm_window, bg="#333333")
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

# Configuración de la detección de tecla ESC
keyboard.on_press_key('esc', lambda _: check_esc())

# Carga la imagen del botón
template = cv2.imread(os.path.join(os.path.dirname(__file__), 'assets', 'button.png'), cv2.IMREAD_COLOR)
h, w = template.shape[:2]

# Iniciar ventana de información en un hilo separado
info_thread = threading.Thread(target=create_info_window)
info_thread.daemon = True
info_thread.start()

# Bucle principal
while running:
    try:
        # Si está pausado, esperar y continuar al siguiente ciclo
        if paused:
            time.sleep(0.1)
            continue
            
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

        time.sleep(0.5)  # Reducido para que sea más responsivo
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)

print("CopilotClicker se ha detenido.")
