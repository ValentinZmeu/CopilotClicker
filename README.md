# Proyecto de Automatización con pyautogui y OpenCV

Este proyecto permite buscar un botón en la pantalla mediante template matching y realizar un clic en él cuando se detecta.

## Requisitos

- Python 3.x
- Las siguientes librerías de Python:
  - opencv-python
  - numpy
  - pyautogui
  - pillow (requerido por pyautogui en Windows)

## Configuración del Entorno Virtual

1. Abre una terminal y navega al directorio del proyecto:

   ```cmd
   cd c:\Users\vadim\Desktop\continue_script
   ```

2. Crea un entorno virtual:

   ```cmd
   python -m venv venv
   ```

3. Activa el entorno virtual:

   ```cmd
   venv\Scripts\activate
   ```

## Instalación de Dependencias

Con el entorno virtual activo, instala las dependencias ejecutando:

```cmd
pip install -r install.txt
```

O bien, instala los paquetes individualmente:

```cmd
pip install opencv-python numpy pyautogui pillow
```

## Ejecución del Script

Con el entorno virtual activo y las dependencias instaladas, ejecuta el script principal:

```cmd
python start.py
```

## Notas

- Asegúrate de tener la imagen `button.png` en el mismo directorio que `start.py`.
- La búsqueda del botón se realiza cada 2 segundos.  
- Puedes modificar el umbral de coincidencia en el script si es necesario.

¡Disfruta automatizando!
