# Automation with PyAutoGUI & OpenCV for GitHub Copilot

[![Python Version](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/) [![License](https://img.shields.io/badge/license-MIT-green)](#license)

Automate clicks on the "Continue" button in GitHub Copilot conversations using template matching. No more manual intervention—just supply a detailed prompt and let the script run uninterrupted.

## 🚀 Features

- **Reconocimiento Multi-Botón**: Busca y detecta varios tipos de botones con diferentes plantillas
- **Filtrado Inteligente**: Evita hacer clic en botones similares pero no deseados
- **Template Matching** con OpenCV para detectar botones en la pantalla
- **Clics Automatizados** vía PyAutoGUI cuando aparece un botón
- **Instalación Simplificada** con scripts de configuración automática (Windows)
- **Adaptación al Tema**: Se adapta al tema claro/oscuro del sistema
- **Configurable**: umbral de detección y intervalo de escaneo ajustables
- **Compatibilidad Multiplataforma** (Windows, macOS, Linux)## ▶️ Usage

### Windows (Método Fácil)

Simplemente haz doble clic en uno de estos archivos en el directorio raíz:

- `run.bat` - Script batch que configura automáticamente el entorno y ejecuta la aplicación
- `RunWithPowerShell.bat` - Ejecuta la versión PowerShell del script, con mejor manejo de errores

Estos scripts automáticamente:

1. Verifican si Python está instalado
2. Crean un entorno virtual si no existe
3. Instalan todas las dependencias necesarias
4. Ejecutan la aplicación

### Método Manual (Todas las plataformas)

```bash
# Activar entorno virtual
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# Ejecutar la aplicación
python start.py
```

### Instrucciones de uso

1. Prepara tu prompt de Copilot con instrucciones claras y detalladas.
2. Ejecuta la aplicación; detectará y hará clic automáticamente en el botón "Continuar" sin necesidad de intervención manual.[![Python Version](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/) [![License](https://img.shields.io/badge/license-MIT-green)](#license)

Automate clicks on the “Continue” button in GitHub Copilot conversations using template matching. No more manual intervention—just supply a detailed prompt and let the script run uninterrupted.

## 🚀 Features

- **Template Matching** with OpenCV to detect the “Continue” button on-screen
- **Automated Clicks** via PyAutoGUI when the button appears
- **Configurable** detection threshold and scan interval
- **Cross-Platform** support (Windows, macOS, Linux)

## 🔧 Requirements

- Python 3.x
- Libraries:
  - `opencv-python`
  - `numpy`
  - `pyautogui`
  - `Pillow` (Windows only)

## 🛠️ Installation

### Método Rápido (Windows)

1. **Descarga el Repositorio**  
   Descarga el código como ZIP o clónalo:

   ```bash
   git clone https://github.com/ValentinZmeu/CopilotClicker
   cd CopilotClicker
   ```

2. **Ejecuta el Script de Instalación**  
   Simplemente haz doble clic en `run.bat` o `RunWithPowerShell.bat` en el directorio raíz.
   Estos scripts configurarán automáticamente todo lo necesario.

### Método Manual

1. **Clona el Repositorio**

   ```bash
   git clone https://github.com/ValentinZmeu/CopilotClicker
   cd CopilotClicker
   ```

2. **Configura el Entorno Virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Instala las Dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

### Imágenes de Botones

El programa ahora carga dinámicamente las imágenes de botones:

- **Botones a detectar**: Coloca cualquier imagen en la carpeta `assets/click/`
- **Botones a evitar**: Coloca cualquier imagen en la carpeta `assets/avoid/`

No es necesario editar ningún archivo de configuración - las imágenes se cargan automáticamente al iniciar el programa. Simplemente agrega o elimina imágenes de estos directorios según sea necesario.

### Parámetros de Detección

Ajusta los parámetros de detección en `config.py`:

```python
MATCH_THRESHOLD = 0.7       # Confianza de coincidencia (0-1)
SCAN_INTERVAL   = 2.0       # Segundos entre escaneos
```

## ▶️ Usage

```bash
python start.py
```

1. Prepare your Copilot prompt with clear, step-by-step instructions.
2. Run the script; it will auto-detect and click “Continue” without pausing.

## 📈 SEO Keywords

`pyautogui automation`, `OpenCV template matching`, `GitHub Copilot script`, `automate button click`, `python screen automation`

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to branch (`git push origin feature-name`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
