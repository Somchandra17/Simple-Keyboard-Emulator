@echo off
title Keyboard Emulator
cd /d "%~dp0"
python keyboard.py
if errorlevel 1 (
    echo.
    echo Error: Python or required packages not found.
    echo Please install Python 3 and run: pip install -r requirements.txt
    echo.
    pause
)
