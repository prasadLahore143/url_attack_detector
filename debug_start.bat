@echo off
echo ============================================================
echo           DEBUG MODE - URL ATTACK DETECTION SYSTEM
echo ============================================================
echo.

echo DEBUG: Current directory is: %CD%
echo DEBUG: Script location is: %~dp0
echo.

echo Checking if Python is available...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    pause
    exit /b 1
)
echo.

echo Checking if src directory exists...
if exist "%~dp0src" (
    echo SUCCESS: src directory found
) else (
    echo ERROR: src directory not found at %~dp0src
    pause
    exit /b 1
)
echo.

echo Checking if main.py exists...
if exist "%~dp0src\main.py" (
    echo SUCCESS: main.py found
) else (
    echo ERROR: main.py not found at %~dp0src\main.py
    pause
    exit /b 1
)
echo.

echo Changing to src directory...
cd /d "%~dp0src"
echo Current directory after cd: %CD%
echo.

echo Contents of src directory:
dir
echo.

echo Attempting to run Flask application...
echo Command: python main.py --mode web --host 127.0.0.1 --port 5000
echo.
python main.py --mode web --host 127.0.0.1 --port 5000

echo.
echo Application finished.
pause