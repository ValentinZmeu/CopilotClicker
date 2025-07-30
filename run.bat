@echo off
echo ==============================================
echo CopilotClicker Launcher
echo ==============================================
echo.

:: Verificar si Python está instalado
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python no se encuentra instalado en este sistema.
    echo Por favor, instala Python 3.x desde https://www.python.org/downloads/
    echo Asegúrate de marcar la opción "Add Python to PATH" durante la instalación.
    echo.
    pause
    exit /b 1
)

:: Mostrar la versión de Python
python --version
echo.

:: Comprobar si existe la carpeta venv
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Error al crear el entorno virtual.
        pause
        exit /b 1
    )
    echo Entorno virtual creado correctamente.
) else (
    echo Usando entorno virtual existente.
)

:: Activar el entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Error al activar el entorno virtual.
    pause
    exit /b 1
)

:: Comprobar si pip está actualizado
echo Actualizando pip...
python -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
    echo Advertencia: No se pudo actualizar pip, pero continuamos.
)

:: Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error al instalar las dependencias.
    pause
    exit /b 1
)

:: Ejecutar la aplicación
echo.
echo ==============================================
echo Iniciando CopilotClicker...
echo ==============================================
echo.
python start.py
if %ERRORLEVEL% neq 0 (
    echo La aplicación terminó con un código de error: %ERRORLEVEL%
    pause
)

:: Desactivar el entorno virtual al finalizar
call venv\Scripts\deactivate.bat

pause
