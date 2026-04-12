@echo off
chcp 65001 >nul
REM =====================================================
REM  KB-System Task Scheduler Setup
REM  Run as Administrator
REM =====================================================

echo.
echo === KB-System Task Scheduler Setup ===
echo.

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..

REM --- 1. Telegram Bot: auto-start on logon ---
echo [1/3] Registering Telegram Bot auto-start...
schtasks /create /tn "KB-System\TelegramBot" ^
    /tr "\"%SCRIPT_DIR%start_bot.bat\"" ^
    /sc onlogon ^
    /rl highest ^
    /f
if %ERRORLEVEL% equ 0 (
    echo   OK: Bot will start on logon
) else (
    echo   NG: Run as Administrator
)

REM --- 2. Inbox processing: daily 9:00 and 21:00 ---
echo.
echo [2/3] Registering inbox processing schedule...
schtasks /create /tn "KB-System\ProcessInbox-AM" ^
    /tr "python \"%PROJECT_DIR%\scripts\process_inbox.py\"" ^
    /sc daily /st 09:00 ^
    /f
schtasks /create /tn "KB-System\ProcessInbox-PM" ^
    /tr "python \"%PROJECT_DIR%\scripts\process_inbox.py\"" ^
    /sc daily /st 21:00 ^
    /f
if %ERRORLEVEL% equ 0 (
    echo   OK: Daily 9:00 and 21:00
) else (
    echo   NG: Registration failed
)

REM --- 3. Weekly digest: Monday 8:00 ---
echo.
echo [3/3] Registering weekly digest schedule...
schtasks /create /tn "KB-System\WeeklyDigest" ^
    /tr "python \"%PROJECT_DIR%\scripts\generate_digest.py\"" ^
    /sc weekly /d MON /st 08:00 ^
    /f
if %ERRORLEVEL% equ 0 (
    echo   OK: Monday 8:00
) else (
    echo   NG: Registration failed
)

echo.
echo === Setup Complete ===
echo.
echo Registered tasks:
schtasks /query /fo table /tn "KB-System\*" 2>nul
echo.
echo To modify: open Task Scheduler (taskschd.msc)
echo.
pause