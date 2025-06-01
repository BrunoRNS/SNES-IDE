@echo off
setlocal

:: Change to the directory of this script
cd /d "%~dp0"

:: Check for 'linux' argument
set "is_linux=0"
if /i "%~1"=="linux" set "is_linux=1"

:: Set the path of the executable files
set "text_editor_exe=%~dp0libs\notepad++\notepad++.exe"

if "%is_linux%"=="1" (
    set "audio_exe=%~dp0tools\audio-tools.bat"
    set "gfx_exe=%~dp0tools\gfx-tools.bat"
    set "other_exe=%~dp0tools\externTools.bat"
    set "project_exe=%~dp0tools\create-new-project.bat"
    set "compiler_exe=%~dp0tools\automatizer-batch.bat"
    set "snes-ide=%~dp0snes-ide.bat"
) else (
    set "audio_exe=%~dp0tools\audio-tools.exe"
    set "gfx_exe=%~dp0tools\gfx-tools.exe"
    set "other_exe=%~dp0tools\externTools.exe"
    set "project_exe=%~dp0tools\create-new-project.exe"
    set "compiler_exe=%~dp0tools\automatizer-batch.bat"
    set "snes-ide=%~dp0snes-ide.exe" 
)

set "emulator_exe=%~dp0libs\bsnes\bsnes.exe"

:: Set the path for the shortcuts
set "shortcut_dir=%userprofile%\Desktop\snes-ide"

if not exist "%shortcut_dir%" (
    mkdir "%shortcut_dir%"
    echo installing... %shortcut_dir%
) else (
    echo installing... %shortcut_dir%
)

:: Create the shortcuts
call :CreateShortcut "text-editor" "%text_editor_exe%"
call :CreateShortcut "audio-tools" "%audio_exe%"
call :CreateShortcut "graphic-tools" "%gfx_exe%"
call :CreateShortcut "other-tools" "%other_exe%"
call :CreateShortcut "create-new-project" "%project_exe%"
call :CreateShortcut "compiler" "%compiler_exe%"
call :CreateShortcut "emulator" "%emulator_exe%"

if "%is_linux%"=="1" (
    copy "%snes-ide%" "%shortcut_dir%\snes-ide.bat"
) else (
    copy "%snes-ide%" "%shortcut_dir%\snes-ide.exe"
)

:: Success message
echo SNES-IDE installed successfully! Check the snes-ide folder on your desktop.

:: Wait for the user to exit the prompt
pause
exit /b

:CreateShortcut
set "shortcut_name=%~1"
set "shortcut_path=%shortcut_dir%\%shortcut_name%.bat"
echo @echo off > "%shortcut_path%"
echo "%~2" >> "%shortcut_path%"
exit /b 0
