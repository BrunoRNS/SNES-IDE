"""
SNES-IDE - gfx-tmx-tmj-converter.py
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
from subprocess import CompletedProcess
from typing import NoReturn
from pathlib import Path
import subprocess
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self, web_app: "Path|str") -> None:

        super().__init__()
        self.setWindowTitle("App PySide6 com HTML")

        html_path: Path = (
            Path(web_app) if isinstance(web_app, str) else web_app / 'index.html'
        )

        self.webview: QWebEngineView = QWebEngineView()
        self.webview.load(f"file:///{html_path.resolve()}")

        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.webview)

        central_widget: QWidget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.showMaximized()

def get_executable_path() -> str:
    """Get the path of the executable or script based on whether the script is frozen 
    (PyInstaller) or not."""

    if getattr(sys, 'frozen', False):
        print("executable path mode chosen")
        return str(Path(sys.executable).parent)
        
    else:
        print("Python script path mode chosen")
        return str(Path(__file__).resolve().parent)

def main() -> NoReturn:
    """Init TileSetExtractor from pvsneslib to convert TMX to TMJ"""

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
    os.environ["PVSNESLIB_HOME"] = str(pvsneslib_home)

    pvsneslib_tmx_tmj_converter: Path = Path(output.stdout.strip()) / "libs" / "pvsneslib" / "tilesetextractor"

    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow(pvsneslib_tmx_tmj_converter)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
