# This script is used to build the project.

from pathlib import Path
import subprocess
import traceback
import sys

class shutil:
    """Reimplementation of class shutil to avoid errors in Wine"""

    @staticmethod
    def copy(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method copy using copy command"""

        src, dst = map(lambda x: Path(x).resolve(), (src, dst))

        subprocess.run(f'copy "{src}" "{dst}"', shell=True, check=True)

    @staticmethod
    def copytree(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method copytree using xcopy"""

        src, dst = map(lambda x: Path(x).resolve(), (src, dst))

        cmd = f'xcopy "{src}" "{dst}" /E /I /Y /Q /H'
        subprocess.run(cmd, shell=True, check=True)

    @staticmethod
    def rmtree(path: str|Path) -> None:
        """Reimplementation of method rmtree using rmdir"""

        path = Path(path).resolve()

        subprocess.run(f'rmdir /S /Q "{path}"', shell=True, check=True)

    @staticmethod
    def move(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method move using move command"""

        src, dst = map(lambda x: Path(x).resolve(), (src, dst))

        subprocess.run(f'move "{src}" "{dst}"', shell=True, check=True)

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


def main() -> int:
    """
    Main function to run the build process.
    """

    try:

        sys.stdout.write("Cleaning SNES-IDE-out...\n")
        clean_all()

        sys.stdout.write("Copying root files...\n")
        copy_root()

        sys.stdout.write("Copying libs...\n")
        copy_lib()

        sys.stdout.write("Copying docs...\n")
        copy_docs()

        sys.stdout.write("Copying bat files...\n")
        copy_bat()

        sys.stdout.write("Copying dlls...\n")
        copy_dlls()
        
        sys.stdout.write("Copying tracker...\n")
        copyTracker()

        sys.stdout.write("Compiling python files...\n")
        compile()


    except subprocess.CalledProcessError as e:

        print("Error while executing command: ", e.__str__(), e.__repr__(), sep="\n\n")

        if e.stdout:

            print("STDOUT:", e.stdout.decode())

        if e.stderr:

            print("STDERR:", e.stderr.decode())

        traceback.print_exception(e)
        return -1
    

    except Exception as e:

        traceback.print_exception(e)
        return -1
    
    return 0

if __name__ == "__main__":
    """
    Run the main function.
    """

    sys.exit(main())