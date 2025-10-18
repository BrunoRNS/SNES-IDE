"""
SNES-IDE - snes-ide.py
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
    scriptExecuted: Signal = Signal(str, str)
    
    def __init__(self) -> None:
        super().__init__()
        self.scripts_dir: Path = self.get_executable_path() / "scripts"

    @staticmethod 
    def get_executable_path() -> Path:
        """Get the path of the executable or script based on whether the script is frozen 
        (PyInstaller) or not."""

        if getattr(sys, 'frozen', False):

            print("executable path mode chosen")
            return Path(sys.executable).resolve().parent
        
        else:

            print("Python script path mode chosen")
            return Path(__file__).resolve().parent
    
    @Slot(str)
    def run_script(self, script_name: str) -> None:
        """Execute a Python script from the scripts directory"""
        try:
            script_path: Path = self.scripts_dir / script_name
            if script_path.exists():
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
        
        central_widget: QWidget = QWidget()
        self.setCentralWidget(central_widget)
        layout: QVBoxLayout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.web_view: QWebEngineView = QWebEngineView()
        
        self.channel: QWebChannel = QWebChannel()
        self.script_runner: ScriptRunner = ScriptRunner()
        self.channel.registerObject("scriptRunner", self.script_runner)
        self.web_view.page().setWebChannel(self.channel)
        
        html_path: Path = ScriptRunner.get_executable_path() / "assets" / "index.html"
        self.web_view.load(f"file:///{html_path.resolve()}")
        
        layout.addWidget(self.web_view)

def main() -> NoReturn:
    app: QApplication = QApplication(sys.argv)
    
    try:
        app.setStyle('Fusion') # type: ignore
    except: ...
    
    window: MainWindow = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
