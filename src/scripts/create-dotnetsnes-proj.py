"""
SNES-IDE - create-dotnetsnes-proj.py
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
from pathlib import Path
import shutil

from get_file_path import get_file_path

def get_executable_path() -> str:
    """
    Get Script Path, by using the path of the script itself.
    """

    return str(Path(__file__).resolve().parent)


def get_home_path() -> str:
    """Get snes-ide home directory"""

    return str(Path(get_executable_path()).parent)


def main() -> NoReturn:
    """Main logic to create dotnetsnes project"""

    home_path: str = get_home_path()

    dotnetsnes_proj: Path = (
        Path(home_path) / "libs" / "DotnetSnesLib" /
        "template" / "DotnetSnes.Example.HelloWorld"
    )

    output_path: Path = Path(str(get_file_path(
        "Select directory to your project", [("Directories", "*")],
        multiple=False, directory=True
    )))

    project_name: str = output_path.name

    try:
        shutil.copytree(dotnetsnes_proj, output_path / project_name)

    except Exception as e:
        print(
            f"Failed to copy dotnetsnes template {dotnetsnes_proj} to {output_path / project_name} duel to {e}."
        )
        exit(-1)

    exit(0)


if __name__ == "__main__":
    main()
