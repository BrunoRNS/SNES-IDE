from subprocess import run, CalledProcessError
from typing import NoReturn
from pathlib import Path
import platform
import sys
import os

def get_executable_path() -> Path:
        """Get the path of the executable or script based on whether the script is frozen 
        (PyInstaller) or not."""

        if getattr(sys, 'frozen', False):
            # PyInstaller executable
            print("executable path mode chosen")

            return Path(sys.executable).absolute().parent
        
        else:
            # Normal script
            print("Python script path mode chosen")

            return Path(__file__).absolute().parent

def main() -> NoReturn:
    """Main logic to open a snes emulator in snes-ide"""

    home_path: Path

    try:
        home_path = Path(
            run(
                ["get-snes-ide-home.exe"] if os.name == "nt" 
                else ["./get-snes-ide-home"], shell=True, text=True,
                cwd=get_executable_path(), check=True
            ).stdout
        )
    except CalledProcessError as e:
        print(f"Error while getting snes-ide home folder: {e}, exiting...")
        exit(-1)
    except Exception as e:
        print(f"Unknown error while getting snes-ide home folder: {e}, exiting...")
        exit(-1)

    snes_emulator: Path = home_path / "bin" / "snes-emulator"

    if os.name == "nt":
        snes_emulator = snes_emulator / "lakesnes.exe"

    elif platform.system().lower() == "darwin":
        snes_emulator = snes_emulator / "bsnes.app"

    else:
        snes_emulator = snes_emulator / "lakesnes"

    try:
        
        if platform.system().lower() == "darwin":
            run(["open", "-a", str(snes_emulator)], check=True)
        
        else:
            run([str(snes_emulator)], check=True)

    except CalledProcessError as e:

        print(f"Error while executing {snes_emulator}: {e}")
        exit(-1)

    exit(0)

if __name__ == "__main__":
    main()
