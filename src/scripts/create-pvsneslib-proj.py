"""
SNES-IDE - create-pvsneslib-proj.py
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
from re import match
import subprocess
import shutil

from get_file_path import get_file_path


class ProjectCreator:

    def __init__(self) -> None:

        self.full_path: Path = Path(str(
            get_file_path(
                "Select the directory of your project", [("Directories", "*")],
                directory=True
            )
        ))
        self.project_name: str = self.full_path.name

    @staticmethod
    def get_executable_path() -> str:
        """
        Get Script Path, by using the path of the script itself.
        """

        return str(Path(__file__).resolve().parent)

    def get_home_path(self) -> str:
        """Get snes-ide home directory"""

        return str(Path(self.get_executable_path()).parent)

    def validate(self) -> None:
        """Check class attributes given as terminal parameters"""

        if not (
            Path(self.full_path).is_dir() and
            Path(self.full_path).exists() and
            match(r"^[A-Za-z0-9_-]+$", self.project_name)
        ):

            print("Illegal parameter was given to create-pvsneslib-proj")
            exit(-1)

    def run(self) -> NoReturn:
        """Run the project creation process."""

        target_path: Path = self.full_path / self.project_name

        try:
            template_path: Path = Path(
                self.get_home_path()) / "libs" / "pvsneslib" / "template"

        except subprocess.CalledProcessError:

            print("Error while getting path to templates")
            exit(-1)

        try:
            shutil.copytree(template_path, target_path)

        except Exception as e:
            print(f"Error while copying the template: {e}")
            exit(-1)

        print("Successfully copied template to target path, exiting...")
        exit(0)


if __name__ == "__main__":

    ProjectCreator().run()
