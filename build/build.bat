@echo off

:: Change to the directory of this script
cd /d "%~dp0"

:: Prefer venv python if available
if exist "..\.venv\Scripts\python.exe" (
    set PYTHON_EXE=..\venv\Scripts\python.exe
) else (
    set PYTHON_EXE=python
)

:: Check if python is installed
where %PYTHON_EXE% >nul 2>nul

if errorlevel 1 (
    echo Python is not installed.
    exit /b 1
)

:: Run build.py if it exists, passing the first argument if provided
if exist "build.py" (
    %PYTHON_EXE% .\build.py %*
) else (
    echo build.py not found.
    exit /b 1
)