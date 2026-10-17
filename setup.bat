@echo off
title PyLab Studio - Setup
cd /d "%~dp0"

REM ---------------------------------------------------------------
REM  PyLab Studio - one-command setup.
REM  Creates .venv, installs packages, verifies every program.
REM ---------------------------------------------------------------

py --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo   Python was not found.
    echo   Install Python 3.8+ from https://www.python.org/downloads/
    echo   and tick "Add python.exe to PATH" during installation.
    echo.
    pause
    exit /b 1
)

py setup.py %*
set EXITCODE=%ERRORLEVEL%

echo.
if %EXITCODE%==0 (
    echo   All done. Start with:  run.bat   or   run_website.bat
) else (
    echo   Setup finished with warnings. See the messages above.
)
echo.
pause
exit /b %EXITCODE%