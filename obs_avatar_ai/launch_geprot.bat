@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Change to the working directory
cd /d %~dp0

echo Select Geprot's Personality:
echo -----------------------------
set i=0

for %%f in (personalities\*.yaml) do (
    set /a i+=1
    set "option[!i!]=%%f"
    echo   !i!: %%~nxf
)

echo -----------------------------
set /p choice=Enter choice:

:: Validate input
set "file="
for /l %%j in (1,1,%i%) do (
    if "!choice!"=="%%j" set "file=!option[%%j]!"
)

if not defined file (
    echo Invalid choice. Exiting...
    pause
    exit /b
)

:: Run the Geprot AI with selected personality
echo Launching Geprot with !file!
python project_geprot.py "!file!"

pause
