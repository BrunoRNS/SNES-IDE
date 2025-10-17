from typing import Union, List, NoReturn, Optional, Tuple
from subprocess import CompletedProcess
from tkinter import Tk, filedialog
from pathlib import Path
import subprocess
import platform
import sys
import os

def get_file_path(
    title: str = "Select file",
    file_types: List[Tuple[str, str]] = [("All files", "*.*")],
    multiple: bool = False,
    directory: bool = False
) -> Union[str, List[str], Tuple[str, ...], NoReturn]:
    """
    Replaces sys.argv with a graphical file/directory selection interface.
    
    Args:
        title: Dialog window title
        file_types: List of tuples with description and extension [(desc, *.ext)]
        multiple: Whether to allow multiple file selection
        directory: Whether to select directories instead of files
    
    Returns:
        str or List[str]: Selected path(s)
        NoReturn: Exits program if user cancels or error occurs
    
    Raises:
        SystemExit: Always exits program on cancellation or error
    """
    root: Optional[Tk] = None
    
    try:
        root = Tk()
        root.withdraw()

        try:
            root.attributes('-topmost', True)  # type: ignore
        except: ...

        selected_path: Union[str, List[str], Tuple[str, ...], None] = None
        
        if directory:
            selected_path = filedialog.askdirectory(title=title)

        elif multiple:
            selected_path = filedialog.askopenfilenames(
                title=title, 
                filetypes=file_types
            )
            if selected_path:
                selected_path = list(selected_path)
        else:
            selected_path = filedialog.askopenfilename(
                title=title, 
                filetypes=file_types
            )
        
        if root:
            root.destroy()
            root = None
        
        if not selected_path or (isinstance(selected_path, list) and len(selected_path) == 0):
            print("No file/directory selected. Application terminated.")
            sys.exit(1)
        
        if isinstance(selected_path, str) and not os.path.exists(selected_path):
            print(f"Selected path does not exist: {selected_path}")
            sys.exit(1)
        
        return selected_path
        
    except Exception as e:
        if root:
            try:
                root.destroy()
            except: ...
        
        print(f"Error in file dialog: {e}")
        sys.exit(1)

def get_executable_path() -> str:
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

def main() -> NoReturn:
    """Main logic of the compilation of the javasnes project"""

    output: CompletedProcess[str] = subprocess.run(
        [".\\get-snes-ide-home.exe" if os.name == "nt" else "./get-snes-ide-home"],
        cwd=get_executable_path(), shell=True, capture_output=True, text=True
    )

    if output.returncode != 0:
        print(
            f"get-snes-ide-home failed to execute duel to {output.stderr}, exiting..."
        )
        exit(-1)

    pvsneslib_home: Path = Path(output.stdout.strip()) / "bin" / "pvsneslib"
    javasnes_jar: Path = Path(output.stdout.strip()) / "libs" / "javasnes" / "lib" / "javasnes.jar"
    java_home: Path

    if platform.system().lower() == "darwin":
        java_home = (
            Path(output.stdout.strip()) / "bin" / "jdk8" / "jdk8" / "zulu-8.jdk" / "Contents" / "Home" / "bin"
        )
    else:
        java_home = Path(output.stdout.strip()) / "bin" / "jdk8" / "jdk8" / "bin"

    os.environ["PVSNESLIB_HOME"] = str(pvsneslib_home)
    os.environ["JAVA_HOME"] = str(java_home)

    javasnes_proj: Path = Path(str(get_file_path(
        "Select JavaSnes project directory", file_types=[("Directories", "*")],
        multiple=False, directory=True
    )))

    if not (javasnes_proj / "Main.java").exists():
        print("No Main.java to build project found, exiting...")
        exit(-1)

    try:
        os.makedirs(javasnes_proj / "out", exist_ok=False)
    except Exception as e:
        print(f"Failed to create out directory: {e}, exiting...")
        exit(-1)

    try:
        javac_output: CompletedProcess[bytes]
        java_output: CompletedProcess[bytes]

        if platform.system().lower() == "windows":

            javac_output = subprocess.run(
                [str(java_home / "javac.exe"), "-cp", ".;" + str(javasnes_jar),
                "-d", "out", "*.java"
                ],
                cwd=javasnes_proj, shell=True, capture_output=True,
                env=os.environ, check=True
            )

            java_output = subprocess.run(
                [str(java_home / "java.exe"), "-cp", "out;" + str(javasnes_jar),
                "Main"
                ],
                cwd=javasnes_proj, shell=True, capture_output=True,
                env=os.environ, check=True
            )
    
        else:
        
            javac_output = subprocess.run(
                [str(java_home / "javac"), "-cp", ".:" + str(javasnes_jar),
                "-d", "out", "*.java"
                ],
                cwd=javasnes_proj, shell=True, capture_output=True,
                env=os.environ, check=True
            )

            java_output = subprocess.run(
                [str(java_home / "java"), "-cp", "out:" + str(javasnes_jar),
                "Main"
                ],
                cwd=javasnes_proj, shell=True, capture_output=True,
                env=os.environ, check=True
            )
        
        if java_output.returncode != 0 or javac_output.returncode != 0:
            print(f"Failed to generate Makefile, exiting...")
            exit(-1)

    except subprocess.CalledProcessError as e:
        print(f"Failed to generate Makefile: {e}, exiting...")
        exit(-1)

    except Exception as e:
        print(f"Unknown error in java compiling: {e}, exiting...")
        exit(-1)

    if not (javasnes_proj / "Makefile").exists():
        print("No Makefile to build project found, exiting...")
        exit(-1)

    make_output: CompletedProcess[bytes] = subprocess.run(
        ["make"], cwd=javasnes_proj, shell=True, capture_output=True,
        env=os.environ
    )

    if make_output.returncode != 0:
        print(f"Error while compiling the software {make_output.stderr}, exiting...")
        exit(-1)

    exit(0)

if __name__ == "__main__":
    main()
