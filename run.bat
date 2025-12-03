@echo off
REM BalrogNPC Launcher
REM Simple launcher for BalrogNPC rAthena Script Editor

echo Starting BalrogNPC...
python BalrogNPC.py

if errorlevel 1 (
    echo.
    echo Error: Python not found or script failed to run.
    echo Please ensure Python 3.8+ is installed and in PATH.
    pause
)
