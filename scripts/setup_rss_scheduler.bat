@echo off
chcp 65001 >nul
REM =====================================================
REM  KB-System RSS Fetcher - Task Scheduler Setup
REM  Run as Administrator
REM =====================================================

echo.
echo === KB-System RSS Fetcher Scheduler Setup ===
echo.

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..
set PYTHON=%PROJECT_DIR%venv\Scripts\python.exe
set RSS_SCRIPT=%SCRIPT_DIR%rss_fetcher.py

echo Python : %PYTHON%
echo Script : %RSS_SCRIPT%
echo.

REM --- RSS Fetch: 4 times a day (03:00 / 09:00 / 15:00 / 21:00) ---
echo [1/4] Registering RSS Fetcher 03:00...
schtasks /create /tn "KB-System\RSS-Fetcher-03" ^
    /tr "\"%PYTHON%\" \"%RSS_SCRIPT%\"" ^
    /sc daily /st 03:00 ^
    /f
if %ERRORLEVEL% equ 0 (echo   OK) else (echo   NG: Run as Administrator)

echo [2/4] Registering RSS Fetcher 09:00...
schtasks /create /tn "KB-System\RSS-Fetcher-09" ^
    /tr "\"%PYTHON%\" \"%RSS_SCRIPT%\"" ^
    /sc daily /st 09:00 ^
    /f
if %ERRORLEVEL% equ 0 (echo   OK) else (echo   NG)

echo [3/4] Registering RSS Fetcher 15:00...
schtasks /create /tn "KB-System\RSS-Fetcher-15" ^
    /tr "\"%PYTHON%\" \"%RSS_SCRIPT%\"" ^
    /sc daily /st 15:00 ^
    /f
if %ERRORLEVEL% equ 0 (echo   OK) else (echo   NG)

echo [4/4] Registering RSS Fetcher 21:00...
schtasks /create /tn "KB-System\RSS-Fetcher-21" ^
    /tr "\"%PYTHON%\" \"%RSS_SCRIPT%\"" ^
    /sc daily /st 21:00 ^
    /f
if %ERRORLEVEL% equ 0 (echo   OK) else (echo   NG)

echo.
echo === Setup Complete ===
echo.
echo Registered tasks:
schtasks /query /fo table /tn "KB-System\*" 2>nul
echo.
pause
