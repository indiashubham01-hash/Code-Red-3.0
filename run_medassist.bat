@echo off
TITLE MedAssist Launcher
echo ==================================================
echo       Starting MedAssist AI System
echo ==================================================
echo.

:: 0. Clean up previous instances
echo [0/3] Cleaning up old processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul

:: 1. Start Backend
echo [1/3] Starting Backend Server (Port 6969)...
start "MedAssist Backend" /MIN python app.py

:: Wait for backend to initialize
echo       Waiting for backend to warm up (5s)...
timeout /t 5 /nobreak >nul

:: 2. Start Frontend (React)
echo [2/3] Starting On-Prem React Frontend...
cd frontend
:: Using absolute path to npm to ensure execution
start "MedAssist Frontend" "C:\Program Files\nodejs\npm.cmd" run dev
cd ..

:: 3. Open Browser
echo [3/3] Opening Web Browser...
timeout /t 5 /nobreak >nul
start http://localhost:5173

echo.
echo ==================================================
echo       System Running!
echo       Backend: http://127.0.0.1:6969
echo       Frontend: http://localhost:5173
echo ==================================================
echo.
echo Press any key to stop all servers and exit...
pause >nul

:: Cleanup on exit
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
echo System Stopped.
