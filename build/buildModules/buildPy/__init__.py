from pathlib import Path
import subprocess
import sys

class shutil:
    """Reimplementation of class shutil to avoid errors in Wine"""

    @staticmethod
    def copy(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method copy using copy command"""

        subprocess.run(f'copy "{src}" "{dst}"', shell=True, check=True)

    @staticmethod
    def copytree(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method copytree using xcopy"""

        cmd = f'xcopy "{src}" "{dst}" /E /I /Y /Q /H'
        subprocess.run(cmd, shell=True, check=True)

    @staticmethod
    def rmtree(path: str|Path) -> None:
        """Reimplementation of method rmtree using rmdir"""

        subprocess.run(f'rmdir /S /Q "{path}"', shell=True, check=True)

    @staticmethod
    def move(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method move using move command"""

        subprocess.run(f'move "{src}" "{dst}"', shell=True, check=True)

def ensure_pip() -> bool:
    """
    Checks if the 'pip' module is installed and available for import.
    Returns:
        bool: True if 'pip' is installed, False otherwise. If 'pip' is not installed,
        an error message is written to stderr.
    """


    try:

        import pip
        return True
    
    except ImportError:

        sys.stderr.write("**pip is not installed.**\n")
        return False

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
    icon_path = (Path(__file__).parent.parent.parent / "assets" / "icons" / "icon.ico").absolute()

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

if __name__ == "__main__":

    sys.exit(main(sys.argv[1], sys.argv[2]))
