@echo off
color 0A
title URL Attack Detection System - Starting...
echo ============================================================
echo            URL ATTACK DETECTION SYSTEM
echo                 NTRO Cybersecurity Project
echo ============================================================
echo.
echo System Features:
echo   * SQL Injection Detection
echo   * Cross-Site Scripting (XSS) Detection
echo   * Directory Traversal Detection
echo   * Command Injection Detection
echo   * SSRF Detection
echo   * File Inclusion Detection
echo   * Credential Stuffing Detection
echo   * Typosquatting Detection
echo.
echo ============================================================
echo.
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    echo Download from: https://python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION% is available
echo.
echo [2/5] Checking project structure...
if not exist "%~dp0src\main.py" (
    echo ❌ ERROR: main.py not found in src directory
    echo Current directory: %~dp0
    echo Expected file: %~dp0src\main.py
    pause
    exit /b 1
)
echo ✅ Project files found
echo.
echo [3/5] Checking dependencies...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Flask not installed
    echo Installing Flask...
    pip install flask
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Flask
        pause
        exit /b 1
    )
)
echo ✅ Dependencies ready
echo.
echo [4/5] Starting Flask web server...
echo 🌐 Web interface will be available at:
echo    - Local:    http://127.0.0.1:5000
echo    - Network:  http://%COMPUTERNAME%:5000 (if firewall allows)
echo.
echo 🔥 Server starting with debug mode enabled
echo 🛑 Press Ctrl+C to stop the server
echo ============================================================
echo.
title URL Attack Detection System - Running on :5000

REM Change to src directory and run the application
echo [5/5] Launching application...
cd /d "%~dp0src"
echo Current directory: %CD%
echo Running: python main.py --mode web --host 0.0.0.0 --port 5000
echo.
python main.py --mode web --host 0.0.0.0 --port 5000

REM This runs when server stops
echo.
echo ============================================================
echo 🔴 Server stopped at %DATE% %TIME%
echo Thank you for using the URL Attack Detection System!
echo ============================================================
echo.
echo Press any key to exit...
title URL Attack Detection System - Stopped
pause >nul
