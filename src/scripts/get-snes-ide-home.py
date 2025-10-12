from pathlib import Path
import sys

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

if __name__ == "__main__":

    snes_ide_home: Path = get_executable_path().parent

    print(snes_ide_home)
