# This script is used to build the project.

from pathlib import Path
import traceback
import sys
import shutil as pyshutil
import locale

import subprocess


def main(python_file: str | Path, target_dir: str | Path) -> int:
    """
    Main function to convert a Python script into a standalone Windows executable (.exe) using PyInstaller.
    This function performs the following steps:
    1. Validates command-line arguments for the Python file and target directory.
    2. Checks if the specified Python file exists.
    3. Ensures that pip and PyInstaller are installed.
    4. Builds the PyInstaller command to generate a single-file executable with a custom icon.
    5. Runs the PyInstaller process and checks for errors.
    6. Moves the generated .exe file to the specified target directory.
    7. Cleans up build artifacts (build and dist directories, and the .spec file).
    8. Prints status messages and handles errors appropriately.
    Exits the program with an error message if any step fails.
    """

    python_file, target_dir = map(
        
            lambda x: Path(x).absolute(), 
            (python_file, target_dir)
    
    )


    if not python_file.exists():

        sys.stderr.write(f"**Error: File '{python_file}' not found.**\n")
        return 1

    if not ensure_pip():

        return 1

    exe_name = python_file.stem + ".exe"
    icon_path = (Path(__file__).parent.parent.parent.parent / "assets" / "icons" / "icon.ico").absolute()

    print(f"Converting '{python_file}' to '{exe_name}'...")

    # Build command for pyinstaller

    cmd = [

        sys.executable, "-m", "PyInstaller",
        "--onefile",
        f"--icon={icon_path}",
        str(python_file)

    ]

    try:

        result = subprocess.run(cmd)

    except Exception as e:

        print(f"Trying to install pyinstaller due to {e}...")
        
        import pip
        pip.main(["install", "PyInstaller"])
        
        result = subprocess.run(cmd)

    if result.returncode != 0:

        sys.stderr.write(f"**Error: Failed to convert '{python_file}' to .exe.**\n")
        
        return 1

    # Move the generated .exe to the target directory
    dist_dir = Path("dist")
    exe_path = dist_dir / exe_name
    target_dir.mkdir(parents=True, exist_ok=True)

    try:

        shutil.move(str(exe_path), str(target_dir / exe_name))

    except Exception as e:

        sys.stderr.write(f"**Error: Failed to move the generated .exe file to '{target_dir}'.**\n")
        print(e)

        return 1

    # Clean up build artifacts
    try:

        shutil.rmtree("build")
        shutil.rmtree("dist")

    except Exception as e:

        print(f"WARNING: {e}")

    spec_file = python_file.with_suffix(".spec")

    if spec_file.exists():

        spec_file.unlink()

    print(f"Conversion successful! '{exe_name}' created in '{target_dir}'.")

    return 0

# This is just to make the CI prettier
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_OK = Fore.GREEN + Style.BRIGHT
    COLOR_FAIL = Fore.RED + Style.BRIGHT
    COLOR_STEP = Fore.CYAN + Style.BRIGHT
    COLOR_RESET = Style.RESET_ALL
except ImportError:
    COLOR_OK = COLOR_FAIL = COLOR_STEP = COLOR_RESET = ""

def _supports_unicode():
    encoding = getattr(sys.stdout, "encoding", None)
    if not encoding:
        encoding = locale.getpreferredencoding(False)
    try:
        "✔".encode(encoding)
        "✖".encode(encoding)
        return True
    except Exception:
        return False

USE_UNICODE = _supports_unicode()

OK_SYMBOL = "✔" if USE_UNICODE else "[OK]"
FAIL_SYMBOL = "✖" if USE_UNICODE else "[FAIL]"
STEP_SYMBOL = "==>"  # Always ASCII

def print_step(msg):
    print(f"{COLOR_STEP}{STEP_SYMBOL} {msg}{COLOR_RESET}")

def print_ok(msg):
    print(f"{COLOR_OK}{OK_SYMBOL} {msg}{COLOR_RESET}")

def print_fail(msg):
    print(f"{COLOR_FAIL}{FAIL_SYMBOL} {msg}{COLOR_RESET}")

def print_summary(success, failed_steps):
    print("\n" + "="*40)
    if success:
        print_ok("BUILD SUCCESSFUL")
    else:
        print_fail("BUILD FAILED")
        print_fail(f"Failed steps: {', '.join(failed_steps)}")
    print("="*40 + "\n")


class shutil:
    """Reimplementation of class shutil to avoid errors in Wine"""

    @staticmethod
    def copy(src: str|Path, dst: str|Path) -> None:
        src, dst = map(lambda x: Path(x).resolve(), (src, dst))
        pyshutil.copy2(src, dst)

    @staticmethod
    def copytree(src: str|Path, dst: str|Path) -> None:
        src, dst = map(lambda x: Path(x).resolve(), (src, dst))
        pyshutil.copytree(src, dst, dirs_exist_ok=True)

    @staticmethod
    def rmtree(path: str|Path) -> None:
        path = Path(path).resolve()
        pyshutil.rmtree(path)

    @staticmethod
    def move(src: str|Path, dst: str|Path) -> None:
        src, dst = map(lambda x: Path(x).resolve(), (src, dst))
        pyshutil.move(src, dst)

# Copy all files from root to the SNES-IDE-out directory

ROOT = Path(__file__).parent.parent.resolve().absolute()

SNESIDEOUT = ROOT / "SNES-IDE-out"

def clean_all() -> None:
    """
    Clean the SNES-IDE-out directory.
    """

    if SNESIDEOUT.exists():
        shutil.rmtree(SNESIDEOUT)

    return None


def copy_root() -> None:
    """
    Copy all files from the root directory to the SNES-IDE-out directory.
    """
    SNESIDEOUT.mkdir(exist_ok=True)

    for file in ROOT.glob("*"):

        if file.is_dir():

            continue

        shutil.copy(file, SNESIDEOUT / file.name)
    
    return None


def copy_lib() -> None:
    """
    Copy all files from the lib directory to the SNES-IDE-out directory.
    """

    (SNESIDEOUT / 'libs').mkdir(exist_ok=True)

    for file in (ROOT / 'libs').rglob("*"):

        if file.is_dir():
            continue

        rel_path = file.relative_to(ROOT / 'libs')
        dest_path = SNESIDEOUT / 'libs' / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file, dest_path)
    
    return None


def copy_docs() -> None:
    """
    Copy the docs directory to the SNES-IDE-out directory.
    """

    (SNESIDEOUT / 'docs').mkdir(exist_ok=True)

    for file in (ROOT / 'docs').rglob("*"):

        if file.is_dir():
            continue

        rel_path = file.relative_to(ROOT / 'docs')
        dest_path = SNESIDEOUT / 'docs' / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file, dest_path)
    
    return None

def copy_bat() -> None:
    """
    Copy the bat files to the SNES-IDE-out directory.
    """

    (SNESIDEOUT / 'tools').mkdir(exist_ok=True)

    for file in (ROOT / 'src' / 'tools' ).rglob("*.bat"):

        if file.is_dir():

            continue

        rel_path = file.relative_to(ROOT / 'src' / 'tools')

        dest_path = SNESIDEOUT / 'tools' / rel_path

        dest_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy(file, dest_path)
    
    return None

def copy_dlls() -> None:
    """
    Copy the dlls from tools dir
    """

    (SNESIDEOUT / 'tools').mkdir(exist_ok=True)

    for file in (ROOT / 'tools').rglob("*.dll"):

        if file.is_dir():

            continue

        rel_path = file.relative_to(ROOT / 'tools')

        dest_path = SNESIDEOUT / 'tools' / rel_path

        dest_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy(file, dest_path)
    
    return None

def compile() -> None:
    """
    Compile the project.
    """

    src_dir = ROOT / "src"

    # Compile Python files

    for file in src_dir.rglob("*.py"):

        rel_path = file.relative_to(src_dir)
        out_path = SNESIDEOUT / rel_path.with_suffix(".exe")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if len(sys.argv) > 1 and sys.argv[1] == "linux":
            # On Linux, copy the .py file and create a .bat file to call it with python

            py_out = SNESIDEOUT / rel_path
            py_out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(file, py_out)

            bat_path = out_path.with_suffix(".bat")

            with open(bat_path, "w") as bat_file:

                bat_file.write(f'@echo off\npython "{Path(py_out).resolve().absolute()}" %*\n')

        else:

            from buildModules.buildPy import main as mpy

            out: int = mpy(file, out_path.parent)

            if out != 0:
                
                raise Exception(f"ERROR while compiling python files: -{abs(out)}")
            

    sys.stdout.write("Success compiling Python files.\n")
    
def copyTracker() -> None:
    
    src_dir = ROOT / "src" / "tools" / "soundsnes" / "tracker"
    dest_dir = ROOT / "SNES-IDE-out" / "tools" / "soundsnes" / "tracker"
    
    shutil.copytree(src_dir, dest_dir)

# Pretty formatting for CI logs
def run_step(step_name, func):
    print_step(f"{step_name}...")
    try:
        func()
        print_ok(f"{step_name} completed.")
        return True
    except Exception as e:
        print_fail(f"{step_name} failed: {e}")
        traceback.print_exception(e)
        return False

def main() -> int:
    """
    Main function to run the build process.
    """
    steps = [
        ("Cleaning SNES-IDE-out", clean_all),
        ("Copying root files", copy_root),
        ("Copying libs", copy_lib),
        ("Copying docs", copy_docs),
        ("Copying bat files", copy_bat),
        ("Copying dlls", copy_dlls),
        ("Copying tracker", copyTracker),
        ("Compiling python files", compile),
    ]
    failed_steps = []
    for name, func in steps:
        if not run_step(name, func):
            failed_steps.append(name)
    print_summary(len(failed_steps) == 0, failed_steps)
    return 0 if not failed_steps else -1

if __name__ == "__main__":
    """
    Run the main function.
    """
    sys.exit(main())