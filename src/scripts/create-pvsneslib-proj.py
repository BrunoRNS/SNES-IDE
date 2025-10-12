from typing_extensions import NoReturn
from pathlib import Path
from re import match
import subprocess
import shutil
import sys
import os

class ProjectCreator:

    def __init__(self) -> None:
        """Init the class' atributes with terminal parameters"""

        self.project_name: str = sys.argv[1]
        self.full_path: Path = Path(sys.argv[2])

    @staticmethod
    def get_executable_path() -> str:
        """Get the path of the executable or script based on whether the script is frozen 
        (PyInstaller) or not."""

        if getattr(sys, 'frozen', False):
            # PyInstaller executable
            print("executable path mode chosen")

            return str(Path(sys.executable).parent)
        
        else:
            # Normal script
            print("Python script path mode chosen")

            return str(Path(__file__).absolute().parent)

    def get_home_path(self) -> str:
        """Get snes-ide home directory, can raise subprocess.CalledProcessError"""

        command: list[str] = ["get-snes-ide-home.exe" if os.name == "nt" else "get-snes-ide-home"]
        cwd: str = self.get_executable_path()

        return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True).stdout


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
            template_path: Path = Path(self.get_home_path()) / "libs" / "pvsneslib" / "template"

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
