"""
SNES-IDE - get_file_path.py
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

from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import Qt

from typing import Union, List, NoReturn, Tuple, Optional

from pathlib import Path
import sys
import os


def get_file_path(
    title: str = "Select file",
    file_types: List[Tuple[str, str]] = [("All files", "*.*")],
    multiple: bool = False,
    directory: bool = False
) -> Union[str, List[str], NoReturn]:
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
    
    app = None
    
    try:
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)

        file_types_str = ";;".join([f"{desc} ({ext})" for desc, ext in file_types])

        dialog = QFileDialog()
        dialog.setWindowTitle(title)
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        selected_path: Union[Optional[str], List[str]] = None
        
        if directory:
            dialog.setFileMode(QFileDialog.FileMode.Directory)
            dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
            
            if dialog.exec() == QFileDialog.DialogCode.Accepted:
                selected_path = dialog.selectedFiles()[0] if dialog.selectedFiles() else "None"
                selected_path = selected_path if Path(selected_path).resolve().is_dir() and Path(selected_path).resolve().exists() else None
                
        elif multiple:
            dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
            dialog.setNameFilter(file_types_str)
            
            if dialog.exec() == QFileDialog.DialogCode.Accepted:
                selected_path = dialog.selectedFiles()
                
        else:
            dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            dialog.setNameFilter(file_types_str)
            
            if dialog.exec() == QFileDialog.DialogCode.Accepted:
                selected_path = dialog.selectedFiles()[0] if dialog.selectedFiles() else None
                
        if not selected_path or (isinstance(selected_path, list) and len(selected_path) == 0):
            print("No file/directory selected. Application terminated.")
            sys.exit(1)

        if isinstance(selected_path, str) and not os.path.exists(selected_path):
            print(f"Selected path does not exist: {selected_path}")
            sys.exit(1)

        return selected_path

    except Exception as e:
        print(f"Error in file dialog: {e}")
        sys.exit(1)
    
