@echo off
title Steam AI Companion Launcher
color 0A
echo ========================================
echo    🎮 STEAM AI COMPANION LAUNCHER
echo ========================================
echo.

:: Check if Ollama is running
tasklist | find /i "ollama.exe" >nul
if errorlevel 1 (
    echo Starting Ollama in background...
    start /min "" "ollama" serve
    timeout /t 5 /nobreak >nul
)

:: Check Python dependencies
pip install psutil pywin32 requests --quiet 2>nul

:: Start the Steam companion
echo Starting Steam AI Companion...
echo.
echo This will run minimized. Press Win+G to show/hide.
echo Companion log: steam_companion_log.txt
echo.

:: Create shortcut for Game Bar (Win+G)
powershell -Command "New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\GameDVR' -Name 'AppCaptureEnabled' -Value 1 -PropertyType DWord -Force" >nul 2>&1

:: Run the companion
python steam_companion.py

pause