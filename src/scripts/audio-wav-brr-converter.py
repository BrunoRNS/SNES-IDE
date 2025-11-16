"""
SNES-IDE - audio-wav-brr-converter.py
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
import os

from get_file_path import get_file_path

def get_executable_path() -> str:
    """
    Get Script Path, by using the path of the script itself.
    """

    return str(Path(__file__).resolve().parent)


def get_home_path() -> str:
    """Get snes-ide home directory"""

    return str(Path(get_executable_path()).parent)


def convert() -> Literal[-1, 0]:
    """Convert WAV files to BRR using snesbrr converter."""

    snesbrr: Path

    if os.name == "nt":
        snesbrr = Path(get_home_path()) / "bin" / \
            "pvsneslib" / "tools" / "snesbrr.exe"

    elif os.name == "posix":
        snesbrr = Path(get_home_path()) / "bin" / \
            "pvsneslib" / "tools" / "snesbrr"

    try:

        if not snesbrr.exists():
            print("snesbrr does not exist")
            return -1

        input_file: Path = Path(str(
            get_file_path(
                "Select a WAV file", [("WAV files", "*.wav")],
                multiple=False, directory=False
            )
        ))

        if not input_file or not input_file.exists() or not str(input_file).endswith(".wav"):

            print("Input file does not exist or is not a brr file")
            return -1

        run([snesbrr, "-e", input_file, str(input_file).split('.')[0] + ".brr"])

    except CalledProcessError as e:

        print(f"Error while executing snesbrr to convert your wav file: {e}")
        return -1

    print("Success!")
    return 0


if __name__ == "__main__":

    exit(convert())
