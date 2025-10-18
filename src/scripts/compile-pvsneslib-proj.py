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

from typing import Union, List, NoReturn, Optional, Tuple
from subprocess import CompletedProcess
from tkinter import Tk, filedialog
from pathlib import Path
import subprocess
import platform
import shutil
import sys
import os

def check_if_path(program: str) -> bool:
    """
    Check if a program is available in the system PATH.
    
    Args:
        program (str): The name of the program to check (e.g., 'make', 'tiled')
        
    Returns:
        bool: True if the program is found in PATH, False otherwise
    """
    return shutil.which(program) is not None

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
        except: ...

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
                pass
        
        print(f"Error in file dialog: {e}")
        sys.exit(1)


def get_executable_path() -> str:
    """Get the path of the executable or script based on whether the script is frozen 
    (PyInstaller) or not."""

    if getattr(sys, 'frozen', False):
        print("executable path mode chosen")
        return str(Path(sys.executable).parent)
        
    else:
        print("Python script path mode chosen")
        return str(Path(__file__).resolve().parent)


def main() -> NoReturn:
    """Main logic of the compilation of the pvsneslib project"""

    output: CompletedProcess[str] = subprocess.run(
        [".\\get-snes-ide-home.exe" if os.name == "nt" else "./get-snes-ide-home"],
        cwd=get_executable_path(), shell=True, capture_output=True, text=True
    )

    if output.returncode != 0:
        print(
            f"get-snes-ide-home failed to execute duel to {output.stderr}, exiting..."
        )
        exit(-1)

    pvsneslib_home: Path = Path(output.stdout.strip()) / "bin" / "pvsneslib"

    os.environ["PVSNESLIB_HOME"] = str(pvsneslib_home)

    pvsneslib_proj: Path = Path(str(get_file_path(
        "Select PvSnesLib project directory", file_types=[("Directories", "*")],
        multiple=False, directory=True
    )))

    if not (pvsneslib_proj / "Makefile").exists():
        print("No Makefile to build project found, exiting...")
        exit(-1)

    if not check_if_path("make") and not platform.system().lower() == "darwin":
        print("Make not found in PATH, exiting...")
        exit(-1)
    elif not check_if_path("gmake") and platform.system().lower() == "darwin":
        print("Gmake not found in PATH, exiting...")
        exit(-1)

    make_output: CompletedProcess[bytes]

    if platform.system().lower() == "darwin":
        make_output = subprocess.run(
            ["gmake"], cwd=pvsneslib_proj, shell=True, capture_output=True,
            env=os.environ
        )
        
    else:
        make_output = subprocess.run(
            ["make"], cwd=pvsneslib_proj, shell=True, capture_output=True,
            env=os.environ
        )

    if make_output.returncode != 0:
        print(f"Error while compiling the software {make_output.stderr}, exiting...")
        exit(-1)

    exit(0)

if __name__ == "__main__":
    main()
