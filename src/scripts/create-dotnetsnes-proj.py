from typing import Union, List, NoReturn, Optional, Tuple
from tkinter import Tk, filedialog
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

