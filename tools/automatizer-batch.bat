@echo off
set /p userDirectory=Enter the desired directory (e.g., C:\Users\anonymous\Desktop\game_folder):
set /p MemoryMap=HIROM or LOROM (if you don't know, choose LOROM)?:
set /p Speed=Speed: use all SNES speed (FAST) or use the recommended one (SLOW)? Write FAST or SLOW:

:: Set the path to the directory above "tools"
set "toolsDirectory=%~dp0.."

:: Set the full path to automatizer.exe
set "automatizerPath=%toolsDirectory%\libs\pvsneslib\devkitsnes\automatizer.exe"

:: Check if automatizer.exe exists
if exist "%automatizerPath%" (
    :: Change to the user-specified directory
    cd /d "%userDirectory%"

    :: Execute automatizer.exe with the userDirectory as an argument
    "%automatizerPath%" "%userDirectory%" "%MemoryMap%" "%Speed%"
    echo Execution successful!
) else (
    echo Error: automatizer.exe not found.
)

:: Pause at the end of the script
pause
