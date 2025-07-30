# CopilotClicker Launcher PowerShell Script
# Este script configura un entorno virtual, instala dependencias y ejecuta la aplicación

# Configuración para mostrar errores
$ErrorActionPreference = "Stop"

Write-Host "=============================================="
Write-Host "CopilotClicker Launcher" -ForegroundColor Cyan
Write-Host "=============================================="
Write-Host ""

try {
    # Verificar si Python está instalado
    $pythonVersion = (python --version 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw "Python no se encuentra instalado en este sistema.`nPor favor, instala Python 3.x desde https://www.python.org/downloads/`nAsegúrate de marcar la opción 'Add Python to PATH' durante la instalación."
    }
    
    Write-Host "Usando $pythonVersion" -ForegroundColor Green
    
    # Comprobar si existe la carpeta venv
    if (-not (Test-Path -Path "venv")) {
        Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
        python -m venv venv
        if ($LASTEXITCODE -ne 0) {
            throw "Error al crear el entorno virtual."
        }
        Write-Host "Entorno virtual creado correctamente." -ForegroundColor Green
    } else {
        Write-Host "Usando entorno virtual existente." -ForegroundColor Green
    }
    
    # Activar el entorno virtual
    Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
    
    # Comprobar si pip está actualizado
    Write-Host "Actualizando pip..." -ForegroundColor Yellow
    & python -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Advertencia: No se pudo actualizar pip, pero continuamos." -ForegroundColor Yellow
    }
    
    # Instalar dependencias
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    & pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        throw "Error al instalar las dependencias."
    }
    
    # Ejecutar la aplicación
    Write-Host ""
    Write-Host "=============================================="
    Write-Host "Iniciando CopilotClicker..." -ForegroundColor Cyan
    Write-Host "=============================================="
    Write-Host ""
    
    & python start.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "La aplicación terminó con un código de error: $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
} finally {
    # Si estamos en un entorno virtual, desactivarlo
    if (Test-Path Function:\deactivate) {
        deactivate
    }
    
    Write-Host "Presione cualquier tecla para salir..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
