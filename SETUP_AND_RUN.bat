@echo off
title Multi Program - All in One Setup & Run
cd /d "%~dp0"

echo Checking Python...
py --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Make sure this project's own modules are importable, not a stale venv.
set PYTHONPATH=%~dp0;%PYTHONPATH%

echo Starting Multi Program - All in One...
py "%~dp0main.py"

echo.
echo Program exited.
pause