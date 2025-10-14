@echo off
color 0B
echo ============================================================
echo            URL ATTACK DETECTION SYSTEM
echo                 CLI Analysis Mode
echo ============================================================
echo.

if "%~1"=="" (
    echo Usage: analyze_url.bat "URL_TO_ANALYZE" [--validate]
    echo.
    echo Examples:
    echo   analyze_url.bat "http://example.com/login?user=' OR '1'='1"
    echo   analyze_url.bat "https://google.com" --validate
    echo.
    echo Options:
    echo   --validate    Also check if URL actually exists (requires internet)
    echo.
    echo This will analyze the provided URL for security threats.
    echo ============================================================
    pause
    exit /b 1
)

echo Analyzing URL: %~1
if "%~2"=="--validate" (
    echo with URL validation enabled
) else (
    echo (pattern analysis only - no URL validation)
)
echo ============================================================
echo.

REM Change to src directory and run CLI analysis
cd /d "%~dp0\src"
if "%~2"=="--validate" (
    python main.py --mode cli --url "%~1" --validate-url
) else (
    python main.py --mode cli --url "%~1"
)

echo.
echo ============================================================
echo Analysis complete. Press any key to exit...
pause >nul