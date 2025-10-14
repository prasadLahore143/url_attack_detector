@echo off
color 0A
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
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)
echo Python is available ✓
echo.
echo Starting Flask web server...
echo Web interface will be available at: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Change to src directory and run the application
cd /d "%~dp0\src"
python main.py --mode web --host 0.0.0.0 --port 5000

echo.
echo ============================================================
echo Server stopped. Thank you for using the system!
echo ============================================================
echo Press any key to exit...
pause >nul
