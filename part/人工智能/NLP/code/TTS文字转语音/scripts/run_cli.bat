@echo off
REM TTS CLI Runner - Windows

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Run TTS CLI with provided arguments
if "%~1"=="" (
    echo Usage: run_cli.bat "text" output.mp3 [voice] [rate]
    echo Example: run_cli.bat "Hello World" output.mp3
    echo Example: run_cli.bat "Hello" output.mp3 zh-CN-XiaoxiaoNeural +20%%
    pause
    exit /b 1
)

python -m tts_toolkit.cli -t "%~1" -o "%~2" %3 %4 %5

if %errorlevel% neq 0 (
    echo.
    echo Failed. Please check your input.
    pause
)
