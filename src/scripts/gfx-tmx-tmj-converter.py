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
from PySide6.QtCore import QUrl
from typing import NoReturn
from pathlib import Path
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self, web_app: "Path|str") -> None:

        super().__init__()
        self.setWindowTitle("Tileset Extractor")

        html_path: Path = (
            Path(web_app) if isinstance(
                web_app, str) else web_app / 'index.html'
        )

        self.webview: QWebEngineView = QWebEngineView()
        self.url: QUrl = QUrl.fromLocalFile(str(html_path.resolve()))
        self.webview.load(self.url)

        layout: QVBoxLayout = QVBoxLayout()
        layout.addWidget(self.webview)

        central_widget: QWidget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.showMaximized()


def get_executable_path() -> str:
    """
    Get Script Path, by using the path of the script itself.
    """

    return str(Path(__file__).resolve().parent)


def get_home_path() -> str:
    """Get snes-ide home directory"""

    return str(Path(get_executable_path()).parent)


def main() -> NoReturn:
    """Init TileSetExtractor from pvsneslib to convert TMX to TMJ"""

    home_path: str = get_home_path()

    pvsneslib_home: Path = Path(home_path) / "bin" / "pvsneslib"
    os.environ["PVSNESLIB_HOME"] = str(pvsneslib_home)

    pvsneslib_tmx_tmj_converter: Path = Path(
        home_path) / "libs" / "pvsneslib" / "tilesetextractor"

    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow(pvsneslib_tmx_tmj_converter)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
