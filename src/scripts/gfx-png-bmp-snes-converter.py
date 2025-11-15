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

from tkinter import Tk, filedialog, ttk, StringVar, BooleanVar
from subprocess import CompletedProcess, CalledProcessError
from tkinter.messagebox import showinfo, showerror # type: ignore
from typing import List, Tuple, Callable, NoReturn
from pathlib import Path
import tkinter as tk
import subprocess
import os

showinfo: Callable[..., str]
showerror: Callable[..., str]

class TileConverterGUI:
    """
    A Tkinter-based GUI for converting images to tile formats with various conversion options.
    
    This class provides a graphical interface for configuring tile conversion parameters
    including tile size, compression, palette options, and output formats.
    """
    
    def __init__(self) -> None:
        """Initialize the main application window and UI components."""

        self.root: Tk = tk.Tk()
        self.root.title("Tile Converter")
        self.root.geometry("600x700")
        
        self.input_file: StringVar = tk.StringVar()
        self.file_type: StringVar = tk.StringVar(value="png")
        
        self.add_blank_tile: BooleanVar = tk.BooleanVar()
        self.block_size: StringVar = tk.StringVar(value="8")
        self.packed_format: BooleanVar = tk.BooleanVar()
        self.lz77_compressed: BooleanVar = tk.BooleanVar()
        self.block_width: StringVar = tk.StringVar(value="8")
        self.block_height: StringVar = tk.StringVar(value="8")
        
        self.tile_offset: StringVar = tk.StringVar(value="0")
        self.include_map: BooleanVar = tk.BooleanVar()
        self.high_priority_bit: BooleanVar = tk.BooleanVar()
        self.generate_pages: BooleanVar = tk.BooleanVar()
        self.no_tile_reduction: BooleanVar = tk.BooleanVar()
        self.mode_format: StringVar = tk.StringVar(value="1")
        
        self.rearrange_palette: BooleanVar = tk.BooleanVar()
        self.palette_rounding: BooleanVar = tk.BooleanVar()
        self.palette_entry: StringVar = tk.StringVar(value="0")
        self.colors_output: StringVar = tk.StringVar(value="16")
        self.include_palette: BooleanVar = tk.BooleanVar()
        self.colors_used: StringVar = tk.StringVar(value="16")
        
        self.quiet_mode: BooleanVar = tk.BooleanVar()
        
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Set up all UI components and layout."""

        main_frame: ttk.Frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_file_section(main_frame)
        
        notebook: ttk.Notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.create_tiles_tab(notebook)
        self.create_map_tab(notebook)
        self.create_palette_tab(notebook)
        self.create_misc_tab(notebook)
        
        convert_btn: ttk.Button = ttk.Button(main_frame, text="Convert", command=self.convert)
        convert_btn.pack(pady=10)
    
    def create_file_section(self, parent: ttk.Frame) -> None:
        """Create file input section."""

        file_frame: ttk.Labelframe = ttk.LabelFrame(parent, text="File Options", padding="5")
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="Input File:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_frame, textvariable=self.input_file, width=50).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, pady=2)
        
        ttk.Label(file_frame, text="File Type:").grid(row=1, column=0, sticky=tk.W, pady=2)
        file_type_combo: ttk.Combobox = ttk.Combobox(file_frame, textvariable=self.file_type, 
                                      values=["bmp", "png"], state="readonly", width=10)
        file_type_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
    
    def create_tiles_tab(self, notebook: ttk.Notebook) -> None:
        """Create tiles options tab."""

        tiles_frame: ttk.Frame = ttk.Frame(notebook, padding="10")
        notebook.add(tiles_frame, text="Tiles Options")
        
        ttk.Checkbutton(tiles_frame, text="Add blank tile management (for multiple backgrounds)",
                       variable=self.add_blank_tile).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(tiles_frame, text="Size of image blocks in pixels:").grid(row=1, column=0, sticky=tk.W, pady=2)
        size_combo: ttk.Combobox = ttk.Combobox(tiles_frame, textvariable=self.block_size,
                                 values=["8", "16", "32", "64"], state="readonly", width=10)
        size_combo.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Checkbutton(tiles_frame, text="Output in packed pixel format",
                       variable=self.packed_format).grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(tiles_frame, text="Output in LZ77 compressed pixel format",
                       variable=self.lz77_compressed).grid(row=3, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(tiles_frame, text="Custom block dimensions (override -s):").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(tiles_frame, text="Width:").grid(row=5, column=0, sticky=tk.W, pady=2)
        ttk.Entry(tiles_frame, textvariable=self.block_width, width=10).grid(row=5, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(tiles_frame, text="Height:").grid(row=6, column=0, sticky=tk.W, pady=2)
        ttk.Entry(tiles_frame, textvariable=self.block_height, width=10).grid(row=6, column=1, sticky=tk.W, pady=2)
    
    def create_map_tab(self, notebook: ttk.Notebook) -> None:
        """Create map options tab."""

        map_frame: ttk.Frame = ttk.Frame(notebook, padding="10")
        notebook.add(map_frame, text="Map Options")
        
        ttk.Label(map_frame, text="Tile number offset (0-2047):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(map_frame, textvariable=self.tile_offset, width=10).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Checkbutton(map_frame, text="Include map for output",
                       variable=self.include_map).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(map_frame, text="Include high priority bit in map",
                       variable=self.high_priority_bit).grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(map_frame, text="Generate map in pages of 32x32 blocks",
                       variable=self.generate_pages).grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(map_frame, text="No tile reduction (not advised)",
                       variable=self.no_tile_reduction).grid(row=4, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(map_frame, text="Output mode format:").grid(row=5, column=0, sticky=tk.W, pady=2)
        mode_combo: ttk.Combobox = ttk.Combobox(map_frame, textvariable=self.mode_format,
                                 values=["1", "5", "6", "7", "9"], state="readonly", width=10)
        mode_combo.grid(row=5, column=1, sticky=tk.W, pady=2)
    
    def create_palette_tab(self, notebook: ttk.Notebook) -> None:
        """Create palette options tab."""

        palette_frame: ttk.Frame = ttk.Frame(notebook, padding="10")
        notebook.add(palette_frame, text="Palette Options")
        
        ttk.Checkbutton(palette_frame, text="Rearrange palette and preserve palette numbers in tilemap",
                       variable=self.rearrange_palette).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(palette_frame, text="Palette rounding (to maximum value of 63)",
                       variable=self.palette_rounding).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(palette_frame, text="Palette entry to add to map tiles (0-15):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(palette_frame, textvariable=self.palette_entry, width=10).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(palette_frame, text="Number of colors to output (0-256):").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(palette_frame, textvariable=self.colors_output, width=10).grid(row=3, column=1, sticky=tk.W, pady=2)
        
        ttk.Checkbutton(palette_frame, text="Include palette for output",
                       variable=self.include_palette).grid(row=4, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(palette_frame, text="Number of colors to use:").grid(row=5, column=0, sticky=tk.W, pady=2)
        colors_combo: ttk.Combobox = ttk.Combobox(palette_frame, textvariable=self.colors_used,
                                   values=["4", "16", "128", "256"], state="readonly", width=10)
        colors_combo.grid(row=5, column=1, sticky=tk.W, pady=2)
    
    def create_misc_tab(self, notebook: ttk.Notebook) -> None:
        """Create miscellaneous options tab."""

        misc_frame: ttk.Frame = ttk.Frame(notebook, padding="10")
        notebook.add(misc_frame, text="Misc Options")
        
        ttk.Checkbutton(misc_frame, text="Quiet mode",
                       variable=self.quiet_mode).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        ttk.Button(misc_frame, text="Display Version Information",
                  command=self.show_version).grid(row=1, column=0, sticky=tk.W, pady=10)
    
    def browse_file(self) -> None:
        """Open file dialog to select input file."""

        file_types: List[Tuple[str, str]] = [
            ("Bitmap files", "*.bmp"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        filename: str = filedialog.askopenfilename(
            title="Select input file",
            filetypes=file_types
        )
        
        if filename:
            self.input_file.set(filename)
            ext: str = os.path.splitext(filename)[1].lower()
            if ext == '.bmp':
                self.file_type.set('bmp')
            elif ext == '.png':
                self.file_type.set('png')
    
    def show_version(self) -> None:
        """Display version information."""

        showinfo("Version Information", 
                    "Tile Converter GUI v5.0\n"
                    "GPL v3 License")
    
    def validate_inputs(self) -> bool:
        """
        Validate all user inputs before conversion.
        
        Returns:
            bool: True if all inputs are valid, False otherwise
        """

        if not self.input_file.get():
            showerror("Error", "Please select an input file")
            return False
        
        if not os.path.exists(self.input_file.get()):
            showerror("Error", "Input file does not exist")
            return False
        
        try:
            tile_offset: int = int(self.tile_offset.get())
            if not (0 <= tile_offset <= 2047):
                raise ValueError("Tile offset out of range")
            
            palette_entry: int = int(self.palette_entry.get())
            if not (0 <= palette_entry <= 15):
                raise ValueError("Palette entry out of range")
            
            colors_output: int = int(self.colors_output.get())
            if not (0 <= colors_output <= 256):
                raise ValueError("Colors output out of range")
                
        except ValueError as e:
            showerror("Error", f"Invalid numeric input: {e}")
            return False
        
        return True
    
    def build_command_line(self) -> List[str]:
        """
        Build command line arguments based on GUI selections.
        
        Returns:
            str: The constructed command line string
        """

        args: List[str] = []
        
        if self.add_blank_tile.get():
            args.append("-b")
        
        if self.block_size.get() != "8":
            args.append(f"-s {self.block_size.get()}")
        
        if self.packed_format.get():
            args.append("-k")
        
        if self.lz77_compressed.get():
            args.append("-z")
        
        if self.block_size.get() == "8":
            if self.block_width.get() != "8":
                args.append(f"-W {self.block_width.get()}")
            if self.block_height.get() != "8":
                args.append(f"-H {self.block_height.get()}")
        
        if self.tile_offset.get() != "0":
            args.append(f"-f {self.tile_offset.get()}")
        
        if self.include_map.get():
            args.append("-m")
        
        if self.high_priority_bit.get():
            args.append("-g")
        
        if self.generate_pages.get():
            args.append("-y")
        
        if self.no_tile_reduction.get():
            args.append("-R")
        
        if self.mode_format.get() != "1":
            args.append(f"-M {self.mode_format.get()}")
        
        if self.rearrange_palette.get():
            args.append("-a")
        
        if self.palette_rounding.get():
            args.append("-d")
        
        if self.palette_entry.get() != "0":
            args.append(f"-e {self.palette_entry.get()}")
        
        if self.colors_output.get() != "16":
            args.append(f"-o {self.colors_output.get()}")
        
        if self.include_palette.get():
            args.append("-p")
        
        if self.colors_used.get() != "16":
            args.append(f"-u {self.colors_used.get()}")
        
        args.append(f"-i \"{self.input_file.get()}\"")
        args.append(f"-t {self.file_type.get()}")
        
        if self.quiet_mode.get():
            args.append("-q")
        
        return args
    
    def convert(self) -> "None|NoReturn":
        """Execute the conversion with selected parameters."""

        if not self.validate_inputs():
            return

        gfx4snes: Path

        try:
            gfx4snes = (
                Path(self.get_home_path()) / "bin" / "pvsneslib" / "devkitsnes" / "tools"
                / ("gfx4snes.exe" if os.name == "nt" else "gfx4snes")
            )
        except CalledProcessError as e:
            showerror(f"Failed to get snes-ide home path duel to: {e}")
            exit(-1)
        except Exception as e:
            showerror(f"Unknown error ocurred when getting snes-ide home path duel to: {e}")
            exit(-1)
        
        command_line: List[str] = self.build_command_line()
        
        showinfo("Conversion started", 
                f"Conversion started with parameters:\n{command_line}\n\n")
        
        try:
            process: CompletedProcess[bytes] = subprocess.run([gfx4snes] + command_line, shell=True,
                cwd=Path(self.input_file.get()).parent
            )
        except Exception as e:
            showerror(f"Failed to execute gfx4snes process: {e}")
            exit(-1)

        if process.returncode != 0:
            try:
                process.check_returncode()

            except CalledProcessError as e:
                showerror(f"Failed to convert image to SNES format duel to: {e}")

            finally:
                exit(-1)
        
        showinfo("Conversion finished",
                "Conversion finished successfully!")

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
        
    def run(self) -> None:
        """Start the GUI application."""

        self.root.mainloop()


def main() -> None:
    """Main function to launch the Tile Converter GUI."""

    app: TileConverterGUI = TileConverterGUI()
    app.run()

if __name__ == "__main__":
    main()
