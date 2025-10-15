from typing import Union, List, NoReturn, Optional, Tuple
from subprocess import run, CalledProcessError
from typing_extensions import Literal
from tkinter import Tk, filedialog
from pathlib import Path
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
        # Create and configure the Tkinter root window
        root = Tk()
        root.withdraw()  # Hide the main window

        try:
            root.attributes('-topmost', True)  # type: ignore
        except: ...

        selected_path: Union[str, List[str], Tuple[str, ...], None] = None
        
        if directory:
            # Directory selection mode
            selected_path = filedialog.askdirectory(title=title)
        elif multiple:
            # Multiple file selection mode
            selected_path = filedialog.askopenfilenames(
                title=title, 
                filetypes=file_types
            )
            # Convert tuple to list for consistency
            if selected_path:
                selected_path = list(selected_path)
        else:
            # Single file selection mode
            selected_path = filedialog.askopenfilename(
                title=title, 
                filetypes=file_types
            )
        
        # Safely destroy the Tkinter window
        if root:
            root.destroy()
            root = None
        
        # Validate selection
        if not selected_path or (isinstance(selected_path, list) and len(selected_path) == 0):
            print("No file/directory selected. Application terminated.")
            sys.exit(1)
        
        # Validate path exists (for single file/directory)
        if isinstance(selected_path, str) and not os.path.exists(selected_path):
            print(f"Selected path does not exist: {selected_path}")
            sys.exit(1)
        
        return selected_path
        
    except Exception as e:
        # Ensure window is destroyed even if error occurs
        if root:
            try:
                root.destroy()
            except:
                pass  # Ignore destruction errors during exception handling
        
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


def get_home_path() -> str:
    """Get snes-ide home directory, can raise subprocess.CalledProcessError"""

    command: list[str] = ["get-snes-ide-home.exe" if os.name == "nt" else "get-snes-ide-home"]
    cwd: str = get_executable_path()

    return run(command, cwd=cwd, capture_output=True, text=True, check=True).stdout

def convert() -> Literal[-1, 0]:
    """Convert BRR files to WAV using snesbrr converter."""

    snesbrr: Path

    if os.name == "nt":
        snesbrr = Path(get_home_path()) / "bin" / "pvsneslib" / "tools" / "snesbrr.exe"
    
    elif os.name == "posix":
        snesbrr = Path(get_home_path()) / "bin" / "pvsneslib" / "tools" / "snesbrr"

    try:

        if not snesbrr.exists():
            print("snesbrr does not exist")
            return -1

        input_file: Path = Path(str(
            get_file_path("Select your BRR file", [("BRR files", "*.brr")])
        ))

        if not input_file or not input_file.exists() or not str(input_file).endswith(".brr"):

            print("Input file does not exist or is not a brr file")
            return -1
            
        run([snesbrr, "-d", input_file, str(input_file).split('.')[0] + ".wav"])

    except CalledProcessError as e:

        print(f"Error while executing snesbrr to convert your wav file: {e}")
        return -1
        
    print("Success!")
    return 0

if __name__ == "__main__":

    exit(convert())
