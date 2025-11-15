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

def get_executable_path() -> str:
    """Get Script Path, by using the path of the script itself."""

    return str(Path(__file__).resolve().parent)


def get_home_path() -> str:
    """Get snes-ide home directory"""

    return str(Path(get_executable_path()).parent)

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
