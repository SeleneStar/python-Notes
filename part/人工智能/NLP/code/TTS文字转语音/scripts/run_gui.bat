@echo off
REM TTS GUI Launcher - Windows

echo =====================================
echo  TTS Toolkit - PyQt5 GUI
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python not detected. Please install Python first.
    pause
    exit /b 1
)

REM Launch GUI
python run_gui.py

if %errorlevel% neq 0 (
    echo.
    echo Launch failed. Dependencies may be missing.
    echo Please run: pip install -r requirements.txt
    pause
)
