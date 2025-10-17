from typing import Union, List, NoReturn, Optional, Tuple
from tkinter import Tk, filedialog
from pathlib import Path
from re import match
import subprocess
import shutil
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


class ProjectCreator:

    def __init__(self) -> None:

        self.full_path: Path = Path(str(
            get_file_path(
                "Select the directory of your project", [("Directories", "*")],
                directory=True
            )
        ))
        self.project_name: str = self.full_path.name

    @staticmethod
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

    def get_home_path(self) -> str:
        """Get snes-ide home directory, can raise subprocess.CalledProcessError"""

        command: list[str] = ["get-snes-ide-home.exe" if os.name == "nt" else "./get-snes-ide-home"]
        cwd: str = self.get_executable_path()

        return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


    def validate(self) -> None:
        """Check class attributes given as terminal parameters"""

        if not (
            Path(self.full_path).is_dir() and 
            Path(self.full_path).exists() and 
            match(r"^[A-Za-z0-9_-]+$", self.project_name)
        ):

            print("Illegal parameter was given to create-javasnes-proj")
            exit(-1)

    def run(self) -> NoReturn:
        """Run the project creation process."""

        target_path: Path = self.full_path / self.project_name

        try:
            template_path: Path = Path(self.get_home_path()) / "libs" / "javasnes" / "template"

        except subprocess.CalledProcessError:

            print("Error while getting path to templates")
            exit(-1)

        try:
            shutil.copytree(template_path, target_path)

        except Exception as e:
            print(f"Error while copying the template: {e}")
            exit(-1)

        print("Successfully copied template to target path, exiting...")
        exit(0)


if __name__ == "__main__":

    ProjectCreator().run()
