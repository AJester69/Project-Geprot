@echo off
chcp 65001 >nul
cd /d "%~dp0"

:: Start overlay
start "" pythonw overlay_server.py

:: Launch main via the unified entrypoint
start "" python main.py

exit
