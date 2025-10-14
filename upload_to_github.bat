@echo off
echo ============================================================
echo URL ATTACK DETECTION SYSTEM - GitHub Upload
echo ============================================================
echo.
echo This script will help you upload your project to GitHub
echo.
echo Prerequisites:
echo 1. Install Git: https://git-scm.com/download/win
echo 2. Create GitHub repository: https://github.com/new
echo.
pause
echo.
echo Initializing Git repository...
git init
echo.
echo Adding all files...
git add .
echo.
echo Creating first commit...
git commit -m "Initial commit: URL Attack Detection System for NTRO"
echo.
echo Please enter your GitHub repository URL:
echo Example: https://github.com/YOUR_USERNAME/url-attack-detector.git
set /p repo_url="Repository URL: "
echo.
echo Adding remote origin...
git remote add origin %repo_url%
echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main
echo.
echo ============================================================
echo Upload Complete!
echo Your project is now on GitHub: %repo_url%
echo ============================================================
pause