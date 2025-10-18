"""
SNES-IDE - build.py
Copyright (C) 2025 BrunoRNS and Atomic-Germ

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

from colorama import init, Fore, Style

from typing import Any, List, Tuple, Callable
from typing_extensions import Literal

from subprocess import CompletedProcess
from pathlib import Path
import subprocess
import traceback
import platform
import shutil
import locale
import stat
import sys
import os

"""
Print functions
"""
def _supports_unicode() -> bool:
    encoding: Any | None = getattr(sys.stdout, "encoding", None)

    if not encoding:
        encoding = locale.getpreferredencoding(False)
    try:
        "✔".encode(encoding)
        "✖".encode(encoding)
        return True

    except Exception:
        return False

def print_step(msg: str) -> None:
    print(f"{COLOR_STEP}{STEP_SYMBOL} {msg}{COLOR_RESET}")

def print_ok(msg: str) -> None:
    print(f"{COLOR_OK}{OK_SYMBOL} {msg}{COLOR_RESET}")

def print_fail(msg: str) -> None:
    print(f"{COLOR_FAIL}{FAIL_SYMBOL} {msg}{COLOR_RESET}")

def print_summary(success: bool, failed_steps: List[str]) -> None:
    print("\n" + "="*40)
    if success:
        print_ok("BUILD SUCCESSFUL")
    else:
        print_fail("BUILD FAILED")
        print_fail(f"Failed steps: {', '.join(failed_steps)}")
    print("="*40 + "\n")

"""
Definitions
"""
init(autoreset=True)

COLOR_OK: str = Fore.GREEN + Style.BRIGHT
COLOR_FAIL: str = Fore.RED + Style.BRIGHT
COLOR_STEP: str = Fore.CYAN + Style.BRIGHT
COLOR_RESET: str = Style.RESET_ALL

USE_UNICODE: bool = _supports_unicode()

OK_SYMBOL: Literal['✔', '[OK]'] = "✔" if USE_UNICODE else "[OK]"
FAIL_SYMBOL: Literal['✖', '[FAIL]'] = "✖" if USE_UNICODE else "[FAIL]"
STEP_SYMBOL: Literal['==>'] = "==>"

ROOT: Path = Path(__file__).parent.parent.resolve()
SNESIDEOUT: Path = ROOT / "SNES-IDE-out"

"""
Build python script
"""

def compile_python(
    python_file_path: Path, target_file_path: Path, windowed: bool,
    icon_path: Path, do_chmod_x: bool, clean_tmp_exec: bool
) -> int:
    """
    Compile a Python script to executable using PyInstaller.
    
    Args:
        python_file_path: Path to the source Python file
        target_file_path: Path where the executable should be placed
        windowed: Whether to run without console (windowed mode)
        icon_path: Path to icon file for the executable
        do_chmod_x: Whether to make executable with chmod +x (Unix-like systems)
        clean_tmp_exec: Whether to clean temporary build files
    
    Returns:
        int: Return code (0 for success, non-zero for failure)
    """
    
    if not python_file_path.exists():
        print(f"Error: Python file not found: {python_file_path}")
        return 1

    file_path: Path = target_file_path
    
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    system: str = platform.system()
    cmd: List[str] = ["pyinstaller", "--onefile"]
    
    if system == "Darwin":
        if windowed:
            cmd.remove("--onefile")
            cmd.append("--windowed")
            if not file_path.name.endswith(".app"):
                file_path: Path = file_path.parent / f"{file_path.stem}.app"
        else:
            cmd.append("--console")
            
    elif system == "Windows":
        if windowed:
            cmd.append("--windowed")
        else:
            cmd.append("--console")

        if not file_path.name.endswith(".exe"):
            file_path = file_path.parent / f"{file_path.stem}.exe"
            
    else:
        if windowed:
            cmd.append("--noconsole")
        else:
            cmd.append("--console")
    
    if icon_path and icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
    
    cmd.append(str(python_file_path))
    
    try:
        print(f"Running PyInstaller with command: {' '.join(cmd)}")
        result: CompletedProcess[str] = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"PyInstaller failed with return code: {result.returncode}")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
            return result.returncode
        
        dist_dir: Path = Path("dist")
        if not dist_dir.exists():
            print("Error: PyInstaller dist directory not found")
            return 1
        
        exec_name: str = python_file_path.stem

        generated_item: Path
        item_type: str

        if system == "Darwin" and windowed:
            generated_item = dist_dir / f"{exec_name}.app"
            item_type = "app bundle"
        elif system == "Windows":
            generated_item = dist_dir / f"{exec_name}.exe"
            item_type = "executable"
        else:
            generated_item = dist_dir / exec_name
            item_type = "executable"
        
        if not generated_item.exists():
            print(f"Error: Generated {item_type} not found: {generated_item}")
            return 1
        
        if generated_item.is_dir():
            if file_path.exists():
                if file_path.is_dir():
                    shutil.rmtree(file_path)
                else:
                    file_path.unlink()
            shutil.copytree(generated_item, file_path)
            shutil.rmtree(generated_item)
        else:
            shutil.move(str(generated_item), str(file_path))
        
        print(f"{item_type.capitalize()} created at: {file_path}")
        
        if do_chmod_x and system != "Windows":
            if system == "Darwin" and windowed:
                actual_executable: Path = file_path / "Contents" / "MacOS" / exec_name
                if actual_executable.exists():
                    actual_executable.chmod(actual_executable.stat().st_mode | stat.S_IEXEC)
                    print(f"Set executable permissions on: {actual_executable}")
            else:
                file_path.chmod(file_path.stat().st_mode | stat.S_IEXEC)
                print(f"Set executable permissions on: {file_path}")
        
        if clean_tmp_exec:
            cleanup_files: List[str] = ["build", "dist", f"{exec_name}.spec"]
            for item in cleanup_files:
                path: Path = Path(item)
                if path.exists():
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                    print(f"Cleaned up: {item}")
        
        return 0
    
    except Exception as e:
        print(f"Error during compilation: {e}")
        return 1

"""
Build Steps
"""
def clean_all() -> None:
    """
    Clean the SNES-IDE-out directory.
    """

    if SNESIDEOUT.exists():
        shutil.rmtree(SNESIDEOUT)

    return


def copy_root() -> None:
    """
    Copy all files from the root directory to the SNES-IDE-out directory.
    """
    SNESIDEOUT.mkdir(exist_ok=True)
    (SNESIDEOUT / 'SNES-IDE').mkdir(exist_ok=True)

    for file in ROOT.glob("*.*"):
        if file.is_dir():
            continue

        shutil.copy(file, SNESIDEOUT / file.name)
        shutil.copy(file, SNESIDEOUT / 'SNES-IDE' / file.name)
    
    return


def copy_lib() -> None:
    """
    Copy all files from the lib directory to the SNES-IDE-out directory.
    """

    (SNESIDEOUT / 'SNES-IDE' / 'libs').mkdir(exist_ok=True)

    for file in (ROOT / 'resources' / 'libs').rglob("*"):

        if file.is_dir():
            continue

        rel_path: Path = file.relative_to(ROOT / 'resources' / 'libs')
        dest_path: Path = SNESIDEOUT / 'SNES-IDE' / 'libs' / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file, dest_path)
    
    return


def copy_docs() -> None:
    """
    Copy the docs directory to the SNES-IDE-out directory.
    """

    (SNESIDEOUT / 'SNES-IDE' / 'docs').mkdir(exist_ok=True)

    for file in (ROOT / 'docs').rglob("*"):

        if file.is_dir():
            continue

        rel_path: Path = file.relative_to(ROOT / 'docs')
        dest_path: Path = SNESIDEOUT / 'SNES-IDE' / 'docs' / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file, dest_path)
    
    return

def copy_bin() -> None:
    """
    Copy the bin files to the SNES-IDE-out directory.
    """

    (SNESIDEOUT / 'SNES-IDE' / 'bin').mkdir(exist_ok=True)

    system: str = platform.system().lower()

    if system == 'darwin':
        system = 'macos'

    for file in (ROOT / 'resources' / 'bin' / system).rglob("*"):

        if file.is_dir():
            continue

        rel_path: Path = file.relative_to(ROOT / 'resources' / 'bin' / system)
        dest_path: Path = SNESIDEOUT / 'SNES-IDE' / 'bin' / rel_path

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file, dest_path)
    
    return

def compile_and_copy_installer() -> None:
    """
    Copy the installer to SNES-IDE-out directory
    """

    for file in (ROOT / 'installer').rglob("*"):

        if file.is_dir():
            continue

        rel_path: Path = file.relative_to(ROOT / 'installer')
        dest_path: Path = SNESIDEOUT / "SNES-IDE" / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if file.suffix == ".py":
            compile_python(
                file, dest_path.parent /
                (file.stem + ".exe" if os.name == "nt" else ""),
                icon_path=ROOT/"icon.png",
                windowed=True, do_chmod_x=os.name=="posix", clean_tmp_exec=True
            )
        else:
            shutil.copy(file, dest_path)
    
    return

def compile_and_copy_source() -> None:
    """
    Compile and copy the project's main source code.
    """

    for file in (ROOT / 'src').rglob("*"):

        if file.is_dir():
            continue

        rel_path: Path = file.relative_to(ROOT / 'src')
        dest_path: Path = SNESIDEOUT / "SNES-IDE" / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if file.name == "snes-ide.py":
            compile_python(
                file, dest_path.parent /
                (file.stem + ".exe" if os.name == "nt" else ""),
                icon_path=ROOT/"icon.png",
                windowed=True, do_chmod_x=os.name=="posix", clean_tmp_exec=True
            )
        elif file.suffix == ".py":
            compile_python(
                file, dest_path.parent /
                (file.stem + ".exe" if os.name == "nt" else ""),
                icon_path=ROOT/"icon.png",
                windowed=False, do_chmod_x=os.name=="posix", clean_tmp_exec=True
            )
        else:
            shutil.copy(file, dest_path)
    
    return

def run_step(step_name: str, func: Callable[..., None]) -> bool:
    """Pretty formatting for CI logs"""

    print_step(f"{step_name}...")

    try:
        func()
        print_ok(f"{step_name} completed.")
        return True

    except Exception as e:
        print_fail(f"{step_name} failed: {e}")
        traceback.print_exception(Exception, e, None)
        return False

def main() -> int:
    """
    Main function to run the build process.
    """

    steps: List[Tuple[str, Callable[..., None]]] = [
        ("Cleaning SNES-IDE-out", clean_all),
        ("Copying root files", copy_root),
        ("Copying libs", copy_lib),
        ("Copying docs", copy_docs),
        ("Copying binary files", copy_bin),
        ("Compiling and copying installer", compile_and_copy_installer),
        ("Compiling and copying source", compile_and_copy_source),
    ]

    failed_steps: List[str] = []
    for name, func in steps:
        if not run_step(name, func):
            failed_steps.append(name)

    print_summary(len(failed_steps) == 0, failed_steps)

    return 0 if not failed_steps else -1

if __name__ == "__main__":
    """
    Run the main function.
    """
    exit(main())
