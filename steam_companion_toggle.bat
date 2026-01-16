@echo off
chcp 65001 >nul
echo.
echo ░██████╗████████╗███████╗░█████╗░███╗░░░███╗
echo ██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗░████║
echo ╚█████╗░░░░██║░░░█████╗░░███████║██╔████╔██║
echo ░╚═══██╗░░░██║░░░██╔══╝░░██╔══██║██║╚██╔╝██║
echo ██████╔╝░░░██║░░░███████╗██║░░██║██║░╚═╝░██║
echo ╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝
echo.
echo [1] Start Companion (Hidden)
echo [2] Start Companion (Minimized Window)
echo [3] Stop Companion
echo [4] View Log
echo [5] Exit
echo.
choice /c:12345 /n /m "Select: "
if errorlevel 5 goto exit
if errorlevel 4 goto viewlog
if errorlevel 3 goto stop
if errorlevel 2 goto minimized
if errorlevel 1 goto hidden

:hidden
echo Starting completely hidden...
start steam_companion_hidden.vbs
echo Started! Running in background.
echo Check Task Manager for python.exe to stop.
pause
goto exit

:minimized
echo Starting minimized window...
start /min python steam_companion_fixed.py
echo Started in minimized window!
pause
goto exit

:stop
echo Stopping companion...
taskkill /f /im python.exe 2>nul
echo Companion stopped.
pause
goto exit

:viewlog
if exist companion_log.txt (
    echo.
    echo Last 10 log entries:
    echo --------------------
    tail -10 companion_log.txt 2>nul || type companion_log.txt | find /n /v "" | more +100
) else (
    echo No log file found.
)
pause
goto exit

:exit