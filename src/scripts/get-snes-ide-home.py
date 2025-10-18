"""
SNES-IDE - get-snes-ide-home.py
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

from pathlib import Path
import sys

def get_executable_path() -> Path:
        """Get the path of the executable or script based on whether the script is frozen 
        (PyInstaller) or not."""

        if getattr(sys, 'frozen', False):
            print("executable path mode chosen")
            return Path(sys.executable).resolve().parent
        
        else:
            print("Python script path mode chosen")
            return Path(__file__).resolve().parent

if __name__ == "__main__":

    snes_ide_home: Path = get_executable_path().parent
    print(snes_ide_home)
