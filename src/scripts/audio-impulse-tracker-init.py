from subprocess import run, CalledProcessError
from pathlib import Path
import platform
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

    schism: "Path|str"
    
    if os.name == "nt":
        schism = Path(get_home_path()) / "bin" / "schismtracker" / "schismtracker.exe"
    
    elif platform.system().lower() == "darwin":
        schism = Path(get_home_path()) / "bin" / "schismtracker" / "Schism Tracker.app"

    elif platform.system().lower() == "linux": # then should be in path
        schism = "schismtracker"

    if not schism or not schism.exists():

        print(f"Failed, schism tracker does not exist in: {schism}")
        return -1

    try:
        
        if platform.system().lower() == "darwin":
            run(["open", "-a", str(schism)], check=True)
        
        else:
            run([str(schism)], check=True)

    except CalledProcessError as e:

        print(f"Error while executing {schism}: {e}")
        return -1

    print("Success")
    return 0

if __name__ == "__main__":

    exit(convert())
