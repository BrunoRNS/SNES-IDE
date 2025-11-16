"""
SNES-IDE - gfx-png-bmp-snes-converter.py
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

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QGridLayout, QTabWidget, QGroupBox, QLabel, QLineEdit, 
                               QPushButton, QCheckBox, QComboBox, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt, QProcess
from subprocess import CalledProcessError
from typing import List
from pathlib import Path
import os
import sys


class TileConverterGUI(QMainWindow):
    """
    A PySide6-based GUI for converting images to tile formats with various conversion options.

    This class provides a graphical interface for configuring tile conversion parameters
    including tile size, compression, palette options, and output formats.
    """

    def __init__(self) -> None:
        """Initialize the main application window and UI components."""
        super().__init__()
        self.setWindowTitle("Tile Converter")
        self.setGeometry(100, 100, 600, 700)
        
        # Initialize variables
        self.input_file: str = ""
        self.file_type: str = "png"
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        self.setup_ui(main_layout)
        
        # Initialize process for running commands
        self.process = QProcess()
        self.process.finished.connect(self.on_process_finished)

    def setup_ui(self, main_layout: QVBoxLayout) -> None:
        """Set up all UI components and layout."""
        self.create_file_section(main_layout)

        # Create notebook (tab widget)
        self.notebook = QTabWidget()
        main_layout.addWidget(self.notebook)

        self.create_tiles_tab()
        self.create_map_tab()
        self.create_palette_tab()
        self.create_misc_tab()

        # Convert button
        convert_btn = QPushButton("Convert")
        convert_btn.clicked.connect(self.convert)
        main_layout.addWidget(convert_btn)

    def create_file_section(self, parent_layout: QVBoxLayout) -> None:
        """Create file input section."""
        file_group = QGroupBox("File Options")
        file_layout = QGridLayout(file_group)

        # Input file selection
        file_layout.addWidget(QLabel("Input File:"), 0, 0)
        self.file_entry = QLineEdit()
        self.file_entry.setPlaceholderText("Select input file...")
        file_layout.addWidget(self.file_entry, 0, 1)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn, 0, 2)

        # File type selection
        file_layout.addWidget(QLabel("File Type:"), 1, 0)
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(["bmp", "png"])
        self.file_type_combo.setCurrentText("png")
        file_layout.addWidget(self.file_type_combo, 1, 1, Qt.AlignmentFlag.AlignLeft)

        parent_layout.addWidget(file_group)

    def create_tiles_tab(self) -> None:
        """Create tiles options tab."""
        tiles_widget = QWidget()
        tiles_layout = QVBoxLayout(tiles_widget)

        self.add_blank_tile = QCheckBox("Add blank tile management (for multiple backgrounds)")
        tiles_layout.addWidget(self.add_blank_tile)

        # Block size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size of image blocks in pixels:"))
        self.block_size_combo = QComboBox()
        self.block_size_combo.addItems(["8", "16", "32", "64"])
        self.block_size_combo.setCurrentText("8")
        size_layout.addWidget(self.block_size_combo)
        size_layout.addStretch()
        tiles_layout.addLayout(size_layout)

        self.packed_format = QCheckBox("Output in packed pixel format")
        tiles_layout.addWidget(self.packed_format)

        self.lz77_compressed = QCheckBox("Output in LZ77 compressed pixel format")
        tiles_layout.addWidget(self.lz77_compressed)

        # Custom block dimensions
        tiles_layout.addWidget(QLabel("Custom block dimensions (override -s):"))
        
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width:"))
        self.block_width_edit = QLineEdit("8")
        self.block_width_edit.setMaximumWidth(80)
        width_layout.addWidget(self.block_width_edit)
        width_layout.addStretch()
        tiles_layout.addLayout(width_layout)
        
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Height:"))
        self.block_height_edit = QLineEdit("8")
        self.block_height_edit.setMaximumWidth(80)
        height_layout.addWidget(self.block_height_edit)
        height_layout.addStretch()
        tiles_layout.addLayout(height_layout)

        tiles_layout.addStretch()
        self.notebook.addTab(tiles_widget, "Tiles Options")

    def create_map_tab(self) -> None:
        """Create map options tab."""
        map_widget = QWidget()
        map_layout = QVBoxLayout(map_widget)

        # Tile offset
        offset_layout = QHBoxLayout()
        offset_layout.addWidget(QLabel("Tile number offset (0-2047):"))
        self.tile_offset_edit = QLineEdit("0")
        self.tile_offset_edit.setMaximumWidth(80)
        offset_layout.addWidget(self.tile_offset_edit)
        offset_layout.addStretch()
        map_layout.addLayout(offset_layout)

        self.include_map = QCheckBox("Include map for output")
        map_layout.addWidget(self.include_map)

        self.high_priority_bit = QCheckBox("Include high priority bit in map")
        map_layout.addWidget(self.high_priority_bit)

        self.generate_pages = QCheckBox("Generate map in pages of 32x32 blocks")
        map_layout.addWidget(self.generate_pages)

        self.no_tile_reduction = QCheckBox("No tile reduction (not advised)")
        map_layout.addWidget(self.no_tile_reduction)

        # Mode format
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Output mode format:"))
        self.mode_format_combo = QComboBox()
        self.mode_format_combo.addItems(["1", "5", "6", "7", "9"])
        self.mode_format_combo.setCurrentText("1")
        mode_layout.addWidget(self.mode_format_combo)
        mode_layout.addStretch()
        map_layout.addLayout(mode_layout)

        map_layout.addStretch()
        self.notebook.addTab(map_widget, "Map Options")

    def create_palette_tab(self) -> None:
        """Create palette options tab."""
        palette_widget = QWidget()
        palette_layout = QVBoxLayout(palette_widget)

        self.rearrange_palette = QCheckBox("Rearrange palette and preserve palette numbers in tilemap")
        palette_layout.addWidget(self.rearrange_palette)

        self.palette_rounding = QCheckBox("Palette rounding (to maximum value of 63)")
        palette_layout.addWidget(self.palette_rounding)

        # Palette entry
        entry_layout = QHBoxLayout()
        entry_layout.addWidget(QLabel("Palette entry to add to map tiles (0-15):"))
        self.palette_entry_edit = QLineEdit("0")
        self.palette_entry_edit.setMaximumWidth(80)
        entry_layout.addWidget(self.palette_entry_edit)
        entry_layout.addStretch()
        palette_layout.addLayout(entry_layout)

        # Colors output
        colors_output_layout = QHBoxLayout()
        colors_output_layout.addWidget(QLabel("Number of colors to output (0-256):"))
        self.colors_output_edit = QLineEdit("16")
        self.colors_output_edit.setMaximumWidth(80)
        colors_output_layout.addWidget(self.colors_output_edit)
        colors_output_layout.addStretch()
        palette_layout.addLayout(colors_output_layout)

        self.include_palette = QCheckBox("Include palette for output")
        palette_layout.addWidget(self.include_palette)

        # Colors used
        colors_used_layout = QHBoxLayout()
        colors_used_layout.addWidget(QLabel("Number of colors to use:"))
        self.colors_used_combo = QComboBox()
        self.colors_used_combo.addItems(["4", "16", "128", "256"])
        self.colors_used_combo.setCurrentText("16")
        colors_used_layout.addWidget(self.colors_used_combo)
        colors_used_layout.addStretch()
        palette_layout.addLayout(colors_used_layout)

        palette_layout.addStretch()
        self.notebook.addTab(palette_widget, "Palette Options")

    def create_misc_tab(self) -> None:
        """Create miscellaneous options tab."""
        misc_widget = QWidget()
        misc_layout = QVBoxLayout(misc_widget)

        self.quiet_mode = QCheckBox("Quiet mode")
        misc_layout.addWidget(self.quiet_mode)

        version_btn = QPushButton("Display Version Information")
        version_btn.clicked.connect(self.show_version)
        misc_layout.addWidget(version_btn)

        misc_layout.addStretch()
        self.notebook.addTab(misc_widget, "Misc Options")

    def browse_file(self) -> None:
        """Open file dialog to select input file."""
        file_types = "Bitmap files (*.bmp);;PNG files (*.png);;All files (*.*)"
        
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select input file",
            "",
            file_types
        )

        if filename:
            self.file_entry.setText(filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.bmp':
                self.file_type_combo.setCurrentText('bmp')
            elif ext == '.png':
                self.file_type_combo.setCurrentText('png')

    def show_version(self) -> None:
        """Display version information."""
        QMessageBox.information(
            self,
            "Version Information",
            "Tile Converter GUI v5.0\nGPL v3 License"
        )

    def validate_inputs(self) -> bool:
        """
        Validate all user inputs before conversion.

        Returns:
            bool: True if all inputs are valid, False otherwise
        """
        input_file = self.file_entry.text()
        
        if not input_file:
            QMessageBox.critical(self, "Error", "Please select an input file")
            return False

        if not os.path.exists(input_file):
            QMessageBox.critical(self, "Error", "Input file does not exist")
            return False

        try:
            tile_offset = int(self.tile_offset_edit.text())
            if not (0 <= tile_offset <= 2047):
                raise ValueError("Tile offset must be between 0 and 2047")

            palette_entry = int(self.palette_entry_edit.text())
            if not (0 <= palette_entry <= 15):
                raise ValueError("Palette entry must be between 0 and 15")

            colors_output = int(self.colors_output_edit.text())
            if not (0 <= colors_output <= 256):
                raise ValueError("Colors output must be between 0 and 256")

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Invalid numeric input: {e}")
            return False

        return True

    def build_command_line(self) -> List[str]:
        """
        Build command line arguments based on GUI selections.

        Returns:
            List[str]: The constructed command line arguments
        """
        args: List[str] = []

        if self.add_blank_tile.isChecked():
            args.append("-b")

        block_size = self.block_size_combo.currentText()
        if block_size != "8":
            args.append(f"-s {block_size}")

        if self.packed_format.isChecked():
            args.append("-k")

        if self.lz77_compressed.isChecked():
            args.append("-z")

        if block_size == "8":
            block_width = self.block_width_edit.text()
            block_height = self.block_height_edit.text()
            if block_width != "8":
                args.append(f"-W {block_width}")
            if block_height != "8":
                args.append(f"-H {block_height}")

        tile_offset = self.tile_offset_edit.text()
        if tile_offset != "0":
            args.append(f"-f {tile_offset}")

        if self.include_map.isChecked():
            args.append("-m")

        if self.high_priority_bit.isChecked():
            args.append("-g")

        if self.generate_pages.isChecked():
            args.append("-y")

        if self.no_tile_reduction.isChecked():
            args.append("-R")

        mode_format = self.mode_format_combo.currentText()
        if mode_format != "1":
            args.append(f"-M {mode_format}")

        if self.rearrange_palette.isChecked():
            args.append("-a")

        if self.palette_rounding.isChecked():
            args.append("-d")

        palette_entry = self.palette_entry_edit.text()
        if palette_entry != "0":
            args.append(f"-e {palette_entry}")

        colors_output = self.colors_output_edit.text()
        if colors_output != "16":
            args.append(f"-o {colors_output}")

        if self.include_palette.isChecked():
            args.append("-p")

        colors_used = self.colors_used_combo.currentText()
        if colors_used != "16":
            args.append(f"-u {colors_used}")

        args.append(f"-i \"{self.file_entry.text()}\"")
        args.append(f"-t {self.file_type_combo.currentText()}")

        if self.quiet_mode.isChecked():
            args.append("-q")

        return args

    def convert(self) -> None:
        """Execute the conversion with selected parameters."""
        if not self.validate_inputs():
            return

        try:
            gfx4snes = (
                Path(self.get_home_path()) / "bin" /
                "pvsneslib" / "devkitsnes" / "tools" /
                ("gfx4snes.exe" if os.name == "nt" else "gfx4snes")
            )
        except CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to get snes-ide home path due to: {e}")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unknown error occurred when getting snes-ide home path due to: {e}")
            return

        if not gfx4snes.exists():
            QMessageBox.critical(self, "Error", f"gfx4snes not found at: {gfx4snes}")
            return

        command_line = self.build_command_line()
        full_command = [str(gfx4snes)] + command_line

        QMessageBox.information(
            self,
            "Conversion started",
            f"Conversion started with parameters:\n{' '.join(full_command)}\n\n"
        )

        # Run the process asynchronously
        working_dir = Path(self.file_entry.text()).parent
        self.process.setWorkingDirectory(str(working_dir))
        self.process.start(str(gfx4snes), command_line)

    def on_process_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        """Handle process completion."""
        if exit_code == 0:
            QMessageBox.information(
                self,
                "Conversion finished",
                "Conversion finished successfully!"
            )
        else:
            error_output = self.process.readAllStandardError().data()
            QMessageBox.critical(
                self,
                "Conversion failed",
                f"Failed to convert image to SNES format.\nError: {error_output}"
            )

    @staticmethod
    def get_executable_path() -> str:
        """
        Get Script Path, by using the path of the script itself.
        """
        return str(Path(__file__).resolve().parent)

    @classmethod
    def get_home_path(cls) -> str:
        """Get snes-ide home directory"""
        return str(Path(cls.get_executable_path()).parent)


def main() -> None:
    """Main function to launch the Tile Converter GUI."""
    app = QApplication(sys.argv)
    
    app.setApplicationName("Tile Converter")
    app.setApplicationVersion("5.0")
    
    window = TileConverterGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
