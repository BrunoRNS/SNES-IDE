"""
SNES-IDE Main Application
Modern Super Nintendo Development Environment using PySide6 WebView
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, 
                              QMessageBox, QVBoxLayout, QWidget)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl, QObject, Slot, QDir
from PySide6.QtGui import QIcon

from typing_extensions import NoReturn


class Backend(QObject):
    """
    Backend class for communication between JavaScript and Python
    Handles all file operations and script execution
    """
    
    def __init__(self) -> None:
        """Initialize the backend"""
        super().__init__()
        self.scripts_dir: Path = Path("scripts")
    
    @Slot(str, result=str)
    def get_current_directory(self):
        """Returns the current working directory"""
        return str(Path.cwd())
    
    @Slot(str, result=str)
    def select_directory(self, title):
        """
        Opens directory selection dialog
        Args:
            title: Dialog title
        Returns:
            str: Selected directory path or empty string if cancelled
        """
        directory = QFileDialog.getExistingDirectory(None, title)
        return directory if directory else ""
    
    @Slot(str, str, result=str)
    def select_file(self, title, file_types):
        """
        Opens file selection dialog
        Args:
            title: Dialog title
            file_types: File type filter (e.g., "Images (*.png *.bmp)")
        Returns:
            str: Selected file path or empty string if cancelled
        """
        file_path, _ = QFileDialog.getOpenFileName(None, title, "", file_types)
        return file_path if file_path else ""
    
    @Slot(str, str, result=bool)
    def run_script_with_directory(self, script_name, directory):
        """
        Executes a script with the selected directory
        Args:
            script_name: Name of the script to execute
            directory: Directory path to pass as argument
        Returns:
            bool: True if successful, False otherwise
        """
        if not directory:
            return False
        
        try:
            script_path = self._get_script_path(script_name)
            if not script_path:
                return False
            
            result = subprocess.run([str(script_path), directory], 
                                  capture_output=True, text=True, check=True)
            
            if result.returncode == 0:
                self._show_message("Success", f"Operation completed successfully!\n{result.stdout}")
                return True
            
            else:
                self._show_message("Error", f"Script execution failed:\n{result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            
            self._show_message("Error", f"Script execution failed: {e}")
            return False
        
        except Exception as e:
            self._show_message("Error", f"Unexpected error: {e}")
            return False
    
    @Slot(str, str, result=bool)
    def run_script_with_file(self, script_name, file_path):
        """
        Executes a script with the selected file
        Args:
            script_name: Name of the script to execute
            file_path: File path to pass as argument
        Returns:
            bool: True if successful, False otherwise
        """
        if not file_path:
            return False
        
        try:
            script_path = self._get_script_path(script_name)
            if not script_path:
                return False
            
            result = subprocess.run([str(script_path), file_path], 
                                  capture_output=True, text=True, check=True)
            
            if result.returncode == 0:
                self._show_message("Success", f"Operation completed successfully!\n{result.stdout}")
                return True
            else:
                self._show_message("Error", f"Script execution failed:\n{result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            self._show_message("Error", f"Script execution failed: {e}")
            return False
        
        except Exception as e:
            self._show_message("Error", f"Unexpected error: {e}")
            return False
    
    @Slot(str, str, str, result=bool)
    def run_script_with_options(self, script_name, file_path, options_json):
        """
        Executes a script with file and options
        Args:
            script_name: Name of the script to execute
            file_path: File path to pass as argument
            options_json: JSON string with options
        Returns:
            bool: True if successful, False otherwise
        """
        if not file_path:
            return False
        
        try:
            script_path = self._get_script_path(script_name)
            if not script_path:
                return False
            
            # Build command arguments
            args = [str(script_path), file_path]
            
            # Parse and add options
            if options_json:
                options = json.loads(options_json)
                for option, value in options.items():
                    if value is True:
                        args.append(option)
                    elif value is not None and value is not False:
                        args.append(option)
                        args.append(str(value))
            
            result = subprocess.run(args, capture_output=True, text=True, check=True)
            
            if result.returncode == 0:
                self._show_message("Success", f"Operation completed successfully!\n{result.stdout}")
                return True
            
            else:
                self._show_message("Error", f"Script execution failed:\n{result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            self._show_message("Error", f"Script execution failed: {e}")
            return False
        
        except Exception as e:
            self._show_message("Error", f"Unexpected error: {e}")
            return False
    
    @Slot(str, result=bool)
    def run_script(self, script_name):
        """
        Executes a script without arguments
        Args:
            script_name: Name of the script to execute
        Returns:
            bool: True if successful, False otherwise
        """
        
        try:
            script_path = self._get_script_path(script_name)
            
            if not script_path:
                return False
            
            result = subprocess.run([str(script_path)], 
                                  capture_output=True, text=True, check=True)
            
            if result.returncode == 0:
                self._show_message("Success", f"Operation completed successfully!\n{result.stdout}")
                return True
            
            else:
                self._show_message("Error", f"Script execution failed:\n{result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            self._show_message("Error", f"Script execution failed: {e}")
            return False
        
        except Exception as e:
            self._show_message("Error", f"Unexpected error: {e}")
            return False
    
    def _get_script_path(self, script_name):
        """
        Gets the full path to a script, considering OS-specific extensions
        Args:
            script_name: Base name of the script
        Returns:
            Path: Full path to the script or None if not found
        """
        if os.name == 'nt':  # Windows
            script_file = script_name + '.exe'
            
        else:  # Unix/Linux/Mac
            script_file = script_name
        
        script_path = self.scripts_dir / script_file
        
        if not script_path.exists():
            
            self._show_message("Error", f"Script not found: {script_path}")
            return None
        
        return script_path
    
    def _show_message(self, title, message) -> None:
        """
        Shows a message dialog
        Args:
            title: Dialog title
            message: Message content
        """
        
        QMessageBox.information(None, title, message)


class MainWindow(QMainWindow):
    """
    Main application window with WebView
    """
    
    def __init__(self):
        """Initialize the main window"""
        
        super().__init__()
        self.backend = Backend()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        
        self.setWindowTitle("SNES-IDE - Super Nintendo Development Environment")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create web view
        self.web_view = QWebEngineView()
        
        # Set up web channel for JavaScript-Python communication
        self.channel = QWebChannel()
        self.channel.registerObject("backend", self.backend)
        self.web_view.page().setWebChannel(self.channel)
        
        # Load the HTML interface
        html_path = Path(__file__).parent / "index.html"
        if html_path.exists():
            self.web_view.load(QUrl.fromLocalFile(str(html_path)))
        else:
            # Fallback: create basic HTML
            self.web_view.setHtml(self._get_fallback_html())
        
        layout.addWidget(self.web_view)
    
    def _get_fallback_html(self) -> str:
        """Returns fallback HTML if index.html is not found"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SNES-IDE</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    background: linear-gradient(to bottom, #2d3748, #4a5568);
                    color: white;
                    margin: 0;
                    padding: 20px;
                }
                .error { 
                    text-align: center; 
                    margin-top: 100px;
                }
            </style>
        </head>
        <body>
            <div class="error">
                <h1>SNES-IDE</h1>
                <p>Error: index.html not found. Please make sure it's in the same directory as main.py</p>
            </div>
        </body>
        </html>
        """


def main() -> NoReturn:
    """
    Main application entry point
    """
    # Create application instance
    app: QApplication = QApplication(sys.argv)
    app.setApplicationName("SNES-IDE")
    app.setApplicationVersion("5.0.0")
    
    # Create and show main window
    window: MainWindow = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
