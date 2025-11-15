"""
SNES-IDE - compile-dotnetsnes-proj.py
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

from typing import Union, List, NoReturn, Optional, Tuple
from subprocess import CompletedProcess
from tkinter import Tk, filedialog
from pathlib import Path
import subprocess
import platform
import sys
import os


def get_file_path(
    title: str = "Select file",
    file_types: List[Tuple[str, str]] = [("All files", "*.*")],
    multiple: bool = False,
    directory: bool = False
) -> Union[str, List[str], Tuple[str, ...], NoReturn]:
    """
    Replaces sys.argv with a graphical file/directory selection interface.

    Args:
        title: Dialog window title
        file_types: List of tuples with description and extension [(desc, *.ext)]
        multiple: Whether to allow multiple file selection
        directory: Whether to select directories instead of files

    Returns:
        str or List[str]: Selected path(s)
        NoReturn: Exits program if user cancels or error occurs

    Raises:
        SystemExit: Always exits program on cancellation or error
    """
    root: Optional[Tk] = None

    try:
        root = Tk()
        root.withdraw()

        try:
            root.attributes('-topmost', True)  # type: ignore
        except:
            ...

        selected_path: Union[str, List[str], Tuple[str, ...], None] = None

        if directory:
            selected_path = filedialog.askdirectory(title=title)

        elif multiple:
            selected_path = filedialog.askopenfilenames(
                title=title,
                filetypes=file_types
            )
            if selected_path:
                selected_path = list(selected_path)
        else:
            selected_path = filedialog.askopenfilename(
                title=title,
                filetypes=file_types
            )

        if root:
            root.destroy()
            root = None

        if not selected_path or (isinstance(selected_path, list) and len(selected_path) == 0):
            print("No file/directory selected. Application terminated.")
            sys.exit(1)

        if isinstance(selected_path, str) and not os.path.exists(selected_path):
            print(f"Selected path does not exist: {selected_path}")
            sys.exit(1)

        return selected_path

    except Exception as e:
        if root:
            try:
                root.destroy()
            except:
                ...

        print(f"Error in file dialog: {e}")
        sys.exit(1)


def get_executable_path() -> str:
    """Get the Script Path, by using the path of the script itself."""

    return str(Path(__file__).resolve().parent)


def get_home_path() -> str:
    """Get snes-ide home directory"""

    return str(Path(get_executable_path()).parent)


def main() -> NoReturn:
    """Main logic of the compilation of the dotnetsnes project"""

    home_path: str = get_home_path()

    pvsneslib_home: Path = Path(home_path) / "bin" / "pvsneslib"
    dntc_home: Path = Path(home_path) / "libs" / "DntcTranspiler"
    dotnetsnes_home: Path = Path(home_path) / "libs" / "DotnetSnesLib" / "src"
    makefile_defaults: Path = dotnetsnes_home / "Makefile.defaults"

    dotnet_home: Path = Path(home_path) / "bin" / "dotnet8"
    make: Path = Path(home_path) / "bin" / "make" / \
        ("make" if os.name == "posix" else "make.exe")

    if platform.system().lower() == "darwin":
        dotnet_home = dotnet_home / "dotnet-sdk-8.0.415-osx-arm64" / "dotnet"

    elif platform.system().lower() == "windows":
        dotnet_home = dotnet_home / "dotnet-sdk-8.0.415-win-x64" / "dotnet.exe"

    else:
        dotnet_home = dotnet_home / "dotnet-sdk-8.0.415-linux-x64" / "dotnet"

    os.environ["PVSNESLIB_HOME"] = str(pvsneslib_home)
    os.environ["DNTC_HOME"] = str(dntc_home)
    os.environ["DOTNETSNES_HOME"] = str(dotnetsnes_home)
    os.environ["MAKEFILE_DEFAULTS"] = str(makefile_defaults)
    os.environ["DOTNET"] = str(dotnet_home)

    dotsnes_proj_path: Path = Path(str(get_file_path(
        "Select DotnetSnes project directory", file_types=[("Directories", "*")],
        multiple=False, directory=True
    )))

    if not (dotsnes_proj_path / "Makefile").exists():
        print("No Makefile to build project found, exiting...")
        exit(-1)

    make_output: CompletedProcess[str]

    make_output = subprocess.run(
        [str(make)], cwd=dotsnes_proj_path, shell=True, capture_output=True,
        env=os.environ, text=True
    )

    if make_output.returncode != 0:
        print(
            f"Error while compiling the software {make_output.stderr}, exiting...")
        exit(-1)

    exit(0)


if __name__ == "__main__":
    main()
