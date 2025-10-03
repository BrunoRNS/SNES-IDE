@echo off

:: Change to the directory of this script
cd /d "%~dp0"

:: Run build.py if it exists, passing the first argument if provided
if exist "build.py" (
    %PYTHON_EXE% .\build.py %*
) else (
    echo build.py not found.
    exit /b 1
)
