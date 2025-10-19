"""
SNES-IDE - gfx-png-bmp-editor.py
Copyright (C) 2025 BrunoRNS

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from subprocess import run, CalledProcessError
from typing_extensions import Literal
from pathlib import Path
import platform
import sys
import os

def get_executable_path() -> str:
    """Get the path of the executable or script based on whether the script is frozen 
    (PyInstaller) or not."""

    if getattr(sys, 'frozen', False):
        print("executable path mode chosen")
        return str(Path(sys.executable).parent)
        
    else:
        print("Python script path mode chosen")
        return str(Path(__file__).resolve().parent)


def get_home_path() -> str:
    """Get snes-ide home directory, can raise subprocess.CalledProcessError"""

    command: list[str] = ["get-snes-ide-home.exe" if os.name == "nt" else "./get-snes-ide-home"]
    cwd: str = get_executable_path()

    return run(command, cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def convert() -> Literal[-1, 0]:
    """Init libresprite png/bmp sprite/map editor."""

    libresprite: Path
    
    if platform.system().lower() == "windows":
        libresprite = Path(get_home_path()) / "bin" / "sprite-editor" / "libresprite.exe"
    
    elif platform.system().lower() == "darwin":
        libresprite = Path(get_home_path()) / "bin" / "sprite-editor" / "libresprite.app"

    else:
        libresprite = Path(get_home_path()) / "bin" / "sprite-editor" / "libresprite.AppImage"

    if not libresprite or not libresprite.exists():

        print(f"Failed, libresprite not found in: {libresprite}")
        return -1

    try:
        
        if platform.system().lower() == "darwin":
            run(["open", "-a", str(libresprite)], shell=True, check=True)
        
        else:
            run([str(libresprite)], shell=True, check=True)

    except CalledProcessError as e:

        print(f"Error while executing {libresprite}: {e}")
        return -1

    print("Success")
    return 0

if __name__ == "__main__":
    exit(convert())
