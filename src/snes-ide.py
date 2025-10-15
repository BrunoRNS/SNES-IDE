from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWebChannel import QWebChannel

from subprocess import CompletedProcess
from typing_extensions import NoReturn
from pathlib import Path
import subprocess
import sys

class ScriptRunner(QObject):
    scriptExecuted: Signal = Signal(str, str)  # script_name, result
    
    def __init__(self) -> None:
        super().__init__()
        self.scripts_dir: Path = self.get_executable_path() / "scripts"

    @staticmethod 
    def get_executable_path() -> Path:
        """Get the path of the executable or script based on whether the script is frozen 
        (PyInstaller) or not."""

        if getattr(sys, 'frozen', False):
            # PyInstaller executable
            print("executable path mode chosen")

            return Path(sys.executable).absolute().parent
        
        else:
            # Normal script
            print("Python script path mode chosen")

            return Path(__file__).absolute().parent
    
    @Slot(str)
    def run_script(self, script_name: str) -> None:
        """Execute a Python script from the scripts directory"""
        try:
            script_path: Path = self.scripts_dir / script_name
            if script_path.exists():
                # Run the script without arguments
                result: CompletedProcess[str] = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True,
                    cwd=self.scripts_dir
                )
                
                if result.returncode == 0:
                    self.scriptExecuted.emit(script_name, "Script executed successfully!")
                else:
                    self.scriptExecuted.emit(script_name, f"Error: {result.stderr}")
            else:
                self.scriptExecuted.emit(script_name, f"Script not found: {script_path}")

        except Exception as e:
            self.scriptExecuted.emit(script_name, f"Exception: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SNES IDE - Super Nintendo Development Environment")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout
        central_widget: QWidget = QWidget()
        self.setCentralWidget(central_widget)
        layout: QVBoxLayout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create web view
        self.web_view: QWebEngineView = QWebEngineView()
        
        # Set up web channel for Python-JavaScript communication
        self.channel: QWebChannel = QWebChannel()
        self.script_runner: ScriptRunner = ScriptRunner()
        self.channel.registerObject("scriptRunner", self.script_runner)
        self.web_view.page().setWebChannel(self.channel)
        
        # Load the HTML interface
        html_path: Path = ScriptRunner.get_executable_path() / "index.html"
        self.web_view.load(f"file://{html_path.absolute()}")
        
        layout.addWidget(self.web_view)

def main() -> NoReturn:
    app: QApplication = QApplication(sys.argv)
    
    # Set application style for better look
    app.setStyle('Fusion')
    
    window: MainWindow = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
