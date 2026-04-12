@echo off
REM =====================================================
REM  Telegram Bot 起動スクリプト
REM  タスクスケジューラで「ログオン時に実行」に設定する
REM =====================================================

cd /d "%~dp0..\bot"

REM Python仮想環境を使う場合
if exist "..\venv\Scripts\activate.bat" (
    call "..\venv\Scripts\activate.bat"
)

echo [%date% %time%] Telegram Bot を起動します... >> "..\logs\bot_startup.log"
python telegram_receiver.py
echo [%date% %time%] Telegram Bot が終了しました (exit code: %ERRORLEVEL%) >> "..\logs\bot_startup.log"

pause
