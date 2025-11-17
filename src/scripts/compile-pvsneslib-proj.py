"""
SNES-IDE - compile-pvsneslib-proj.py
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

from typing_extensions import NoReturn
from subprocess import CompletedProcess
from pathlib import Path
import subprocess
import os

from get_file_path import get_file_path

def get_executable_path() -> str:
    """
    Get the path of the directory containing the script executable.

    Returns:
        str: Path of the executable directory
    """

    return str(Path(__file__).resolve().parent)


def get_home_path() -> str:
    """Get snes-ide home directory"""

    return str(Path(get_executable_path()).parent)


def main() -> NoReturn:
    """Main logic of the compilation of the pvsneslib project"""

    home_path = get_home_path()

    pvsneslib_home: Path = Path(home_path) / "bin" / "pvsneslib"

    os.environ["PVSNESLIB_HOME"] = str(pvsneslib_home)

    pvsneslib_proj: Path = Path(str(get_file_path(
        "Select PvSnesLib project directory", file_types=[("Directories", "*")],
        multiple=False, directory=True
    )))

    if not (pvsneslib_proj / "Makefile").exists():
        print("No Makefile to build project found, exiting...")
        exit(-1)

    make: Path = Path(home_path) / "bin" / "make" / \
        ("make" if os.name == "posix" else "make.exe")

    make_output: CompletedProcess[str]

    make_output = subprocess.run(
        [str(make)], cwd=pvsneslib_proj, shell=True, capture_output=True,
        env=os.environ, text=True
    )

    if make_output.returncode != 0:
        print(
            f"Error while compiling the software {make_output.stderr}, exiting...")
        exit(-1)

    exit(0)


if __name__ == "__main__":
    main()
