@echo off

:: Change to the directory of this script
cd /d "%~dp0"

:: Check if python is installed

where python >nul 2>nul

if errorlevel 1 (

    echo Python is not installed.
    exit /b 1

)

:: Run build.py if it exists, passing the first argument if provided
if exist "build.py" (

    python .\build.py %*

) else (

    echo build.py not found.
    exit /b 1

)
