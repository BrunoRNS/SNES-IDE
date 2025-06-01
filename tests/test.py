""" This is just an example test script for the SNES-IDE-out project. """
from pathlib import Path
import subprocess

ROOT = Path(__file__).parent.parent.resolve()
SNESIDEOUT = ROOT / "SNES-IDE-out"

def test() -> None:
    """
    Test the project.
    """
    install_bat = SNESIDEOUT / "INSTALL.bat"

    if install_bat.exists():

        try:
            subprocess.run([str(install_bat)], check=True, shell=True, cwd=SNESIDEOUT)

        except subprocess.CalledProcessError as e:

            print(f"INSTALL.bat failed with exit code {e.returncode}")

    else:
        
        print("INSTALL.bat not found in SNES-IDE-out directory.")

if __name__ == "__main__":
    test()
    print("Test completed.")
    exit(0)