@echo off
title Push CardioDiab-AI to GitHub
color 0a
echo =====================================================================
echo    Pushing CardioDiab-AI to GitHub
echo =====================================================================
echo.
echo [*] Pushing branch 'main' to origin...
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo =====================================================================
    echo [SUCCESS] Your project is now live on GitHub!
    echo URL: https://github.com/Farhan130612/watsonx-disease-prediction
    echo =====================================================================
) else (
    echo [!] If repository was not found:
    echo 1. Go to https://github.com/new
    echo 2. Repository name: watsonx-disease-prediction
    echo 3. Click 'Create repository' (leave it empty)
    echo 4. Run this file again!
)
echo.
pause
