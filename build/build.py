# This script is used to build the project.

from pathlib import Path
import traceback
import sys
import shutil as pyshutil
import os
import locale

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