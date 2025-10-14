@echo off
title URL Attack Detection System - Quick Start
color 0A

echo ============================================================
echo               QUICK START - BACKEND ONLY
echo ============================================================
echo.
echo Starting Flask server directly...
echo URL: http://127.0.0.1:5000
echo.

REM Go directly to src and start
cd /d "%~dp0src"
python main.py --mode web

echo.
echo Server stopped.
pause