"""
SNES-IDE - open-emulator.py
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
from typing import NoReturn
from pathlib import Path
import platform
import sys
import os

def get_executable_path() -> Path:
        """Get the path of the executable or script based on whether the script is frozen 
        (PyInstaller) or not."""

        if getattr(sys, 'frozen', False):
            print("executable path mode chosen")
            return Path(sys.executable).resolve().parent
        
        else:
            print("Python script path mode chosen")
            return Path(__file__).resolve().parent

def main() -> NoReturn:
    """Main logic to open a snes emulator in snes-ide"""

    home_path: Path

    try:
        home_path = Path(
            run(
                ["get-snes-ide-home.exe"] if os.name == "nt" 
                else ["./get-snes-ide-home"], shell=True, text=True,
                cwd=get_executable_path(), check=True
            ).stdout
        )
    except CalledProcessError as e:
        print(f"Error while getting snes-ide home folder: {e}, exiting...")
        exit(-1)
    except Exception as e:
        print(f"Unknown error while getting snes-ide home folder: {e}, exiting...")
        exit(-1)

    snes_emulator: Path = home_path / "bin" / "snes-emulator"

    if platform.system().lower() == "windows":
        snes_emulator = snes_emulator / "lakesnes.exe"

    elif platform.system().lower() == "darwin":
        snes_emulator = snes_emulator / "bsnes.app"

    else:
        snes_emulator = snes_emulator / "lakesnes"

    try:
        
        if platform.system().lower() == "darwin":
            run(["open", "-a", str(snes_emulator)], check=True)
        
        else:
            run([str(snes_emulator)], check=True)

    except CalledProcessError as e:

        print(f"Error while executing {snes_emulator}: {e}")
        exit(-1)

    exit(0)

if __name__ == "__main__":
    main()
