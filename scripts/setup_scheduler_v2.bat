@echo off
REM =====================================================
REM  KB-System Task Scheduler Setup (v2)
REM  Includes: inbox processing, weekly digest, morning digest
REM  Run as Administrator for Bot auto-start
REM =====================================================

echo.
echo === KB-System Task Scheduler Setup ===
echo.

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..

REM --- 1. Telegram Bot: auto-start on logon ---
echo [1/4] Registering Telegram Bot auto-start...
schtasks /create /tn "KB-System\TelegramBot" ^
    /tr "\"%SCRIPT_DIR%start_bot.bat\"" ^
    /sc onlogon ^
    /rl highest ^
    /f
if %ERRORLEVEL% equ 0 (
    echo   OK: Bot will start on logon
) else (
    echo   NG: Run as Administrator, or use startup folder instead
)

REM --- 2. Inbox processing: daily 9:00 and 21:00 ---
echo.
echo [2/4] Registering inbox processing schedule...
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

REM --- 3. Morning digest: daily 7:30 ---
echo.
echo [3/4] Registering morning digest schedule...
schtasks /create /tn "KB-System\MorningDigest" ^
    /tr "python \"%PROJECT_DIR%\scripts\morning_digest.py\"" ^
    /sc daily /st 07:30 ^
    /f
if %ERRORLEVEL% equ 0 (
    echo   OK: Daily 7:30
) else (
    echo   NG: Registration failed
)

REM --- 4. Weekly digest: Monday 8:00 ---
echo.
echo [4/4] Registering weekly digest schedule...
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
echo Schedule summary:
echo   07:30 daily  - Morning digest (Telegram)
echo   09:00 daily  - Process inbox
echo   21:00 daily  - Process inbox
echo   08:00 Monday - Weekly digest
echo.
echo To modify: open Task Scheduler (taskschd.msc)
echo.
pause
