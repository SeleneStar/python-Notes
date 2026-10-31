@echo off
REM Windows Installation Script

echo ============================================
echo    TTS Toolkit Installer
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not detected
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Detecting Python environment...
python --version

echo.
echo [2/3] Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Installation failed, trying with China mirror...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)

echo.
echo [3/3] Installing TTS Toolkit...
pip install -e .

echo.
echo ============================================
echo    Installation Complete!
echo ============================================
echo.
echo Usage:
echo   CLI: tts-cli -t "Hello" -o output.mp3
echo   GUI: tts-gui
echo   Python: python -m tts_toolkit.cli --help
echo.
echo Documentation:
echo   README.md
echo   docs/usage.md
echo.
pause
