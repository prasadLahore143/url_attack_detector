@echo off
title URL Attack Detection System - Launcher
color 0F

:MENU
cls
echo ============================================================
echo            URL ATTACK DETECTION SYSTEM
echo                 NTRO Cybersecurity Project
echo ============================================================
echo.
echo Please select an option:
echo.
echo [1] Start Web Interface (Recommended)
echo [2] Interactive URL Analysis 
echo [3] Analyze Single URL
echo [4] Generate Sample Data
echo [5] View System Information
echo [6] Exit
echo.
echo ============================================================

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto WEB
if "%choice%"=="2" goto INTERACTIVE
if "%choice%"=="3" goto SINGLE
if "%choice%"=="4" goto GENERATE
if "%choice%"=="5" goto INFO
if "%choice%"=="6" goto EXIT

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto MENU

:WEB
echo.
echo Starting Web Interface...
echo Open your browser to: http://127.0.0.1:5000
echo.
call "%~dp0start.bat"
goto MENU

:INTERACTIVE
echo.
echo Starting Interactive Analysis Mode...
echo.
call "%~dp0interactive_analysis.bat"
goto MENU

:SINGLE
echo.
set /p url="Enter URL to analyze: "
if "%url%"=="" (
    echo No URL provided. Returning to menu...
    timeout /t 2 >nul
    goto MENU
)
call "%~dp0analyze_url.bat" "%url%"
goto MENU

:GENERATE
echo.
echo Starting Sample Data Generator...
echo.
call "%~dp0generate_data.bat"
goto MENU

:INFO
cls
echo ============================================================
echo            SYSTEM INFORMATION
echo ============================================================
echo.
echo URL Attack Detection System
echo Version: 1.0
echo Author: NTRO Cybersecurity Project
echo.
echo Supported Attack Types:
echo   • SQL Injection
echo   • Cross-Site Scripting (XSS)
echo   • Directory Traversal
echo   • Command Injection
echo   • Server-Side Request Forgery (SSRF)
echo   • Local/Remote File Inclusion
echo   • Credential Stuffing
echo   • Typosquatting
echo.
echo Features:
echo   • Real-time URL analysis
echo   • Web-based dashboard
echo   • Database storage
echo   • Export functionality
echo   • Batch processing
echo.
echo System Requirements:
echo   • Python 3.7+
echo   • Flask framework
echo   • SQLite database
echo.
echo ============================================================
echo.
pause
goto MENU

:EXIT
echo.
echo Thank you for using the URL Attack Detection System!
echo.
timeout /t 2 >nul
exit