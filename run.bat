@echo off
title CardioDiab-AI : IBM watsonx.ai Disease Prediction Model
color 0b
echo =====================================================================
echo    CardioDiab-AI : Dual Disease Risk Prediction Model
echo    Using IBM watsonx.ai Studio / Watson AutoAI Pipeline
echo    Second Year Engineering College Project (IBM Subject)
echo =====================================================================
echo.
echo [*] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH! Please install Python 3.9+ or add it to PATH.
    pause
    exit /b
)

echo [*] Starting Flask Healthcare AI Server...
echo [*] Opening Web Dashboard at http://127.0.0.1:5000 in your browser...
echo.

start "" "http://127.0.0.1:5000"
python app.py

pause
