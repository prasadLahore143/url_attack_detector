@echo off
color 0D
echo ============================================================
echo            URL ATTACK DETECTION SYSTEM
echo              Sample Data Generator
echo ============================================================
echo.

set /p num_records="Enter number of records to generate (default 1000): "
if "%num_records%"=="" set num_records=1000

echo.
echo Generating %num_records% sample attack records...
echo This will populate the database with test data for demonstration.
echo.
echo ============================================================
echo.

REM Change to src directory and run data generation
cd /d "%~dp0\src"
python main.py --mode generate --num-records %num_records%

echo.
echo ============================================================
echo Data generation complete. Press any key to exit...
pause >nul