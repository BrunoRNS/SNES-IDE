"""
SNES-IDE - gfx-tmx-editor.py
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
import shutil


def check_if_path(program: str) -> bool:
    """
    Check if a program is available in the system PATH.

    Args:
        program (str): The name of the program to check (e.g., 'make', 'tiled')

    Returns:
        bool: True if the program is found in PATH, False otherwise
    """
    return shutil.which(program) is not None


def get_executable_path() -> str:
    """
    Get Script Path, by using the path of the script itself.
    """

    return str(Path(__file__).resolve().parent)


def get_home_path() -> str:
    """Get snes-ide home directory"""

    return str(Path(get_executable_path()).parent)


def main() -> NoReturn:
    """Main logic to init tiled -> default tmx_editor"""

    tmx_editor: Path

    if platform.system().lower() == "windows":
        tmx_editor = Path(get_home_path()) / "bin" / "tmx-editor" / "tiled.exe"

    elif platform.system().lower() == "darwin":
        tmx_editor = Path(get_home_path()) / "bin" / "tmx-editor" / "Tiled.app"

    else:
        tmx_editor = Path(get_home_path()) / "bin" / \
            "tmx-editor" / "tiled.AppImage"

    if not tmx_editor or not tmx_editor.exists():
        print(f"Failed, tiled does not exist in: {tmx_editor}")
        exit(-1)

    try:

        if platform.system().lower() == "darwin":
            run(["open", "-a", str(tmx_editor)], shell=True, check=True)

        else:
            run([str(tmx_editor)], shell=True, check=True)

    except CalledProcessError as e:

        print(f"Error while executing {tmx_editor}: {e}")
        exit(-1)

    print("Success")
    exit(0)


if __name__ == "__main__":
    main()
