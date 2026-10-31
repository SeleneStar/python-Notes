@echo off
REM TTS Toolkit - Windows Build Script
REM This script packages the application into Windows executable files

echo ============================================================
echo            TTS Toolkit - Windows Build Script
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.7+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
echo.

REM Check and install PyInstaller
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not installed. Installing...
    pip install pyinstaller
)

REM Verify PyInstaller installation
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install PyInstaller
    pause
    exit /b 1
)

REM Check and install edge-tts
python -c "import edge_tts" >nul 2>&1
if %errorlevel% neq 0 (
    echo edge-tts not installed. Installing...
    pip install edge-tts
)

REM Verify edge-tts installation
python -c "import edge_tts" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install edge-tts
    pause
    exit /b 1
)

REM Check and install PyQt5
python -c "import PyQt5" >nul 2>&1
if %errorlevel% neq 0 (
    echo PyQt5 not installed. Installing...
    pip install PyQt5
)

REM Check and install Pillow (for icon conversion)
python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pillow not installed. Installing for icon conversion...
    pip install Pillow
)

echo.
echo All dependencies installed successfully!
echo.
echo [2/3] Starting build process...
echo.

REM Run build script
python "%~dp0build_exe.py"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed
    pause
    exit /b 1
)

echo.
echo [3/3] Build completed!
echo.
echo Output location: %~dp0..\release\
echo.
echo ============================================================
pause
