@echo off
setlocal

:: Set the path of the executable files
set "main_exe=%~dp0main\notepad++.exe"
set "audio_exe=%~dp0tools\audio-tools.exe"
set "gfx_exe=%~dp0tools\gfx-tools.exe"
set "export_exe=%~dp0tools\export.exe"
set "other_exe=%~dp0tools\externTools.exe"
set "project_exe=%~dp0tools\create-new-project.exe"
set "compiler_exe=%~dp0tools\automatizer-batch.bat"

:: Set the path for the shortcuts
set "shortcut_dir=%userprofile%\Desktop\snes-ide"

if not exist "%shortcut_dir%" (
    mkdir "%shortcut_dir%"
    echo installing... %shortcut_dir%
) else (
    echo installing... %shortcut_dir%
)

:: Create the shortcuts
call :CreateShortcut "text-editor" "%main_exe%"
call :CreateShortcut "audio-tools" "%audio_exe%"
call :CreateShortcut "graphic-tools" "%gfx_exe%"
call :CreateShortcut "export-rom" "%export_exe%"
call :CreateShortcut "other-tools" "%other_exe%"
call :CreateShortcut "create-new-project" "%project_exe%"
call :CreateShortcut "compiler" "%compiler_exe%"

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
exit /b
