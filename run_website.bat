@echo off
title PyLab Studio - Website
cd /d "%~dp0"

REM --- Is the website already running? ---
curl -s -o nul -w "%%{http_code}" http://127.0.0.1:5001/health 2>nul | findstr "200" >nul
if not errorlevel 1 (
    echo PyLab Studio is already running. Opening browser...
    start "http://127.0.0.1:5001"
    exit /b 0
)

echo ============================================================
echo   PyLab Studio
echo   Every Python program, one click away
echo ============================================================
echo   Programs : 133
echo   Starting server on port 5001 ...
echo   Open:  http://127.0.0.1:5001
echo   Stop:  close this window or press Ctrl+C
echo ============================================================
echo.

start "" "http://127.0.0.1:5001"
py webapp\app.py

echo.
echo Server stopped.
pause