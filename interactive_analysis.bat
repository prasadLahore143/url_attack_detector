@echo off
color 0E
echo ============================================================
echo            URL ATTACK DETECTION SYSTEM
echo               Interactive Analysis Mode
echo ============================================================
echo.
echo This mode allows you to analyze multiple URLs interactively.
echo Enter URLs one by one and get immediate results.
echo Type 'quit' or 'exit' to stop.
echo.
echo Sample malicious URLs to test:
echo   http://example.com/login?user=' OR '1'='1
echo   http://site.com/search?q=^<script^>alert('XSS')^</script^>
echo   http://app.com/file?path=../../../etc/passwd
echo.
echo ============================================================
echo.

REM Change to src directory and run interactive analysis
cd /d "%~dp0\src"
python main.py --mode analyze

echo.
echo ============================================================
echo Interactive session ended. Press any key to exit...
pause >nul