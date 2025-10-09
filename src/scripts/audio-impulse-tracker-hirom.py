from subprocess import run, CalledProcessError
from pathlib import Path
import sys
import os

def get_executable_path():
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


def get_home_path() -> str:
    """Get snes-ide home directory, can raise subprocess.CalledProcessError"""

    command: list[str] = ["get-snes-ide-home.exe" if os.name == "nt" else "get-snes-ide-home"]
    cwd: str = get_executable_path()

    return run(command, cwd=cwd, capture_output=True, text=True, check=True)


def convert() -> int:
    """Convert Impulse Tracker files to HiROM SNES' soundbank using smconv."""

    snesmod: Path
    
    if os.name == "nt":
        snesmod = Path(get_home_path()) / "bin" / "pvsneslib" / "tools" / "smconv.exe"
        
    else:
        snesmod = Path(get_home_path()) / "bin" / "pvsneslib" / "tools" / "smconv"

    try:
        
        input_file = Path(sys.argv[1])

        if not input_file or not input_file.exists():

            print("Failed, input_file does not exist")
            return -1
            
        run([str(snesmod), "-s", "-i", "-o", "soundbank", input_file], cwd=Path(input_file).parent, check=True)

    except CalledProcessError as e:

        print(f"Error while executing {snesmod}: {e}")
        return -1

    print("Success")
    return 0

if __name__ == "__main__":

    exit(convert())
