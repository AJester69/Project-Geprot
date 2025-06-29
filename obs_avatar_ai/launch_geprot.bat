@echo off
setlocal enabledelayedexpansion

:: Show choices
echo Select Geprot's Personality:
echo -----------------------------
set i=0
for %%F in (personalities\*.yaml) do (
    set /a i+=1
    echo  !i!: %%~nxF
    set "choice[!i!]=%%F"
)
echo -----------------------------
set /p user_choice=Enter choice:

:: Validate and resolve filename
set "selected="
for /L %%j in (1,1,!i!) do (
    if "!user_choice!"=="%%j" set "selected=!choice[%%j]!"
)
if not defined selected (
    echo Invalid choice.
    pause
    exit /b
)

:: Run overlay_server in background
start "" /min pythonw gui_app.pyw !selected! 2> error.log

pause
