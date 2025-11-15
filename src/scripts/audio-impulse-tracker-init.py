"""
SNES-IDE - audio-impulse-tracker-init.py
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

from subprocess import run, CalledProcessError
from typing_extensions import Literal
from pathlib import Path
import platform

def get_executable_path() -> str:
    """
    Get Script Path, by using the path of the script itself.
    """

    return str(Path(__file__).resolve().parent)

def get_home_path() -> str:
    """Get snes-ide home directory"""

    return str(Path(get_executable_path()).parent)


def convert() -> Literal[-1, 0]:
    """Init schismtracker."""

    schism: Path
    
    if platform.system().lower() == "windows":
        schism = Path(get_home_path()) / "bin" / "schismtracker" / "schismtracker.exe"
    
    elif platform.system().lower() == "darwin":
        schism = Path(get_home_path()) / "bin" / "schismtracker" / "Schism Tracker.app"

    else:
        schism = Path(get_home_path()) / "bin" / "schismtracker" / "Schism_Tracker-x86_64.AppImage"

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
