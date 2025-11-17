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
from typing_extensions import NoReturn
from pathlib import Path
import platform

from get_file_path import get_file_path


def get_executable_path() -> Path:
    """Returns the path of the executable"""

    return Path(__file__).resolve().parent


def get_home_path() -> str:
    """Get snes-ide home directory"""

    return str(Path(get_executable_path()).parent)


def main() -> NoReturn:
    """Main logic to open a snes emulator in snes-ide"""

    home_path: Path = Path(get_home_path())

    snes_emulator: Path = home_path / "bin" / "snes-emulator"

    if platform.system().lower() == "windows":
        snes_emulator = snes_emulator / "lakesnes.exe"

    elif platform.system().lower() == "darwin":
        snes_emulator = snes_emulator / "bsnes.app"

    else:
        snes_emulator = snes_emulator / "lakesnes"

    rom_path: Path = Path(str(get_file_path(
        "Select your ROM", [("ROM files", "*.sfc")], multiple=False,
        directory=False
    )))

    try:

        if platform.system().lower() == "darwin":
            run(["open", "-a", str(snes_emulator), str(rom_path)], check=True)

        else:
            run([str(snes_emulator), str(rom_path)], check=True)

    except CalledProcessError as e:

        print(f"Error while executing {snes_emulator}: {e}")
        exit(-1)

    exit(0)


if __name__ == "__main__":
    main()
