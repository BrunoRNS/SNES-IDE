from tkinter import StringVar, messagebox, filedialog, SOLID
from pathlib import Path
import tkinter as tk
import subprocess
import webbrowser
import atexit
import sys
import os

class shutil:
    """Reimplementation of class shutil to avoid errors in Wine"""

    @staticmethod
    def copy(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method copy using copy command"""

        src, dst = map(lambda x: Path(x).resolve(), (src, dst))

        subprocess.run(f'copy "{src}" "{dst}"', shell=True, check=True)

    @staticmethod
    def copytree(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method copytree using xcopy"""

        src, dst = map(lambda x: Path(x).resolve(), (src, dst))

        cmd = f'xcopy "{src}" "{dst}" /E /I /Y /Q /H'
        subprocess.run(cmd, shell=True, check=True)

    @staticmethod
    def rmtree(path: str|Path) -> None:
        """Reimplementation of method rmtree using rmdir"""

        path = Path(path).resolve()

        subprocess.run(f'rmdir /S /Q "{path}"', shell=True, check=True)

    @staticmethod
    def move(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method move using move command"""

        src, dst = map(lambda x: Path(x).resolve(), (src, dst))

        subprocess.run(f'move "{src}" "{dst}"', shell=True, check=True)


class PathManager:

    def __init__(self):
        """Initialize the PathManager to determine the root path based on execution context."""

        self.root = self._get_root_path()

    def _get_root_path(self) -> Path:
        """Determine the root path based on whether the script is run as a frozen executable or a Python script."""
        if getattr(sys, 'frozen', False):

            print("Executable path mode chosen")

            return Path(sys.executable).parent.parent
        
        else:

            print("Python script path mode chosen")
            return Path(__file__).absolute().parent.parent

    def get_tool_path(self, *parts) -> Path:
        """Construct a path to a tool within the 'libs' directory."""
        return self.root.joinpath(*parts)

class M8TEExecutor:

    def __init__(self, path_manager: PathManager):
        """Initialize the M8TEExecutor with the path to the M8TE executable."""

        self.m8te_path = path_manager.get_tool_path("libs", "M8TE", "bin", "M8TE.exe")

    def run(self):
        """Run the M8TE executable and handle any errors."""

        try:

            subprocess.run([str(self.m8te_path)], check=True)

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {self.m8te_path}: {e}")
            return -1

        messagebox.showinfo("SNES-IDE", "Success!")
        return 0

class Gfx4SnesExecutor:

    def __init__(self, path_manager: PathManager):
        """Initialize the Gfx4SnesExecutor with the path to the gfx4snes executable."""

        self.gfx4snes_path = path_manager.get_tool_path("libs", "pvsneslib", "tools", "gfx4snes.exe")
        self.root = path_manager.root

    def run(self):
        """Run the gfx4snes tool with user-selected options and input file."""

        try:

            nwindow = tk.Tk()
            nwindow.title("Choose options for the gfx4snes")
            input_file = filedialog.askopenfilename(filetypes=[("your image(PNG or BMP)", ["*.png", "*.bmp"])])

            if not input_file:

                nwindow.destroy()
                messagebox.showerror("Fatal", "No Input file selected")

                return -1

            options, entries = self._create_options(nwindow)
            tk.Button(nwindow, text="Run", command=lambda: self._execute(nwindow, input_file, options, entries)).pack()
            
            nwindow.mainloop()

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {self.gfx4snes_path}: {e}")

        else:

            messagebox.showinfo("SNES-IDE", "Success!")

    def _create_options(self, nwindow):
        """Create the options and entries for the gfx4snes tool in a new window."""

        stroptions = [
            "-b,        add blank tile management (for multiple bgs)",
            "-s,        size of image blocks in pixels {[8],16,32,64} <int>",
            "-k,        output in packed pixel format",
            "-z,        add blank tile management (for multiple bgs)",
            "-W,        width of image block in pixels <int>",
            "-H,        height of image block in pixels <int>",
            "-f,        generate the whole picture with an offset for tile number {0..2047}",
            "-m,        include map for output",
            "-g,        include high priority bit in map",
            "-y,        generate map in pages of 32x32 (good for scrolling)",
            "-R,        no tile reduction (not advised)",
            "-M,        convert the whole picture for mode 1,5,6 or 7 format {[1],5,6,7} <int>",
            "-a,        rearrange palette and preserve palette numbers in tilemap",
            "-d,        palette rounding (to a maximum value of 63)",
            "-e,        palette entry to add to map tiles {0..7} <int>",
            "-o,        number of colors to output to filename.pal {0..256} <int>",
            "-p,        include palette for output",
            "-u,        number of colors to use {4,16,128,[256]} <int>",
        ]

        options = [StringVar() for _ in range(len(stroptions))]

        entries = dict()

        for i, opt in enumerate(stroptions):

            tk.Checkbutton(nwindow, text=opt, variable=options[i], onvalue="1", offvalue="0").pack(anchor="w")

            if "<int>" in opt:

                entry = tk.Entry(nwindow)
                entry.pack()
                entries[opt[:2]] = entry

        return options, entries

    def _execute(self, nwindow, input_file, options, entries):
        """Execute the gfx4snes command with the selected options and input file."""

        stroptions = [
            "-b,        add blank tile management (for multiple bgs)",
            "-s,        size of image blocks in pixels {[8],16,32,64} <int>",
            "-k,        output in packed pixel format",
            "-z,        add blank tile management (for multiple bgs)",
            "-W,        width of image block in pixels <int>",
            "-H,        height of image block in pixels <int>",
            "-f,        generate the whole picture with an offset for tile number {0..2047}",
            "-m,        include map for output",
            "-g,        include high priority bit in map",
            "-y,        generate map in pages of 32x32 (good for scrolling)",
            "-R,        no tile reduction (not advised)",
            "-M,        convert the whole picture for mode 1,5,6 or 7 format {[1],5,6,7} <int>",
            "-a,        rearrange palette and preserve palette numbers in tilemap",
            "-d,        palette rounding (to a maximum value of 63)",
            "-e,        palette entry to add to map tiles {0..7} <int>",
            "-o,        number of colors to output to filename.pal {0..256} <int>",
            "-p,        include palette for output",
            "-u,        number of colors to use {4,16,128,[256]} <int>",
        ]

        args = []

        for i, var in enumerate(options):

            if var.get() == "1":

                opt_flag = stroptions[i][:2]
                args.append(opt_flag)

                if "<int>" in stroptions[i]:

                    entry = entries.get(opt_flag)

                    if entry:

                        args.append(entry.get())

        nwindow.destroy()

        input_path = Path(input_file)
        command = [str(self.gfx4snes_path)] + args

        if input_path.suffix.lower() == '.bmp':

            command += ['-t', 'bmp', '-i', str(input_path)]

        else:

            command += ['-i', str(input_path)]

        result = subprocess.run(command, cwd=str(input_path.parent), capture_output=True)

        messagebox.showinfo("Result: ", str(result))

class SnesToolsExecutor:

    def __init__(self, path_manager: PathManager):
        """Initialize the SnesToolsExecutor with the path to the snestools executable."""

        self.snestools_path = path_manager.get_tool_path("libs", "pvsneslib", "tools", "snestools.exe")

    def run(self):
        """Run the snestools tool with user-selected input file."""

        try:

            input_file = filedialog.askopenfilename(filetypes=[("your snes ROM", ["*.smc", "*.sfc"])])

            if not input_file:

                messagebox.showerror("Error", "Input file does not exist")
                return -1
            
            input_path = Path(input_file)
            result = subprocess.run([str(self.snestools_path), str(input_path)], capture_output=True, text=True)

            messagebox.showinfo("snestools", str(result))

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {self.snestools_path}: {e}")
            return -1

        messagebox.showinfo("SNES-IDE", "Success!")
        return 0

class Tmx2SnesExecutor:

    def __init__(self, path_manager: PathManager):
        """Initialize the Tmx2SnesExecutor with the path to the tmx2snes executable."""

        self.tmx2snes_path = path_manager.get_tool_path("libs", "pvsneslib", "tools", "tmx2snes.exe")

    def run(self):
        """Run the tmx2snes tool with user-selected input files."""

        try:

            input_file = filedialog.askopenfilename(filetypes=[("tmxfilename", "*")])
            input_file2 = filedialog.askopenfilename(filetypes=[("mapfilename", "*")])

            if not (input_file and input_file2):
                messagebox.showerror("Error", "Input file does not exist")
                return -1
            
            input_path = Path(input_file)
            subprocess.run([str(self.tmx2snes_path), str(input_path), str(input_file2)], cwd=str(input_path.parent))

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {self.tmx2snes_path}: {e}")
            return -1

        messagebox.showinfo("SNES-IDE", "Success!")
        return 0

class FontCopier:

    def __init__(self, path_manager: PathManager):
        """Initialize the FontCopier with the path to the pvsneslib font image."""

        self.font_path = path_manager.get_tool_path("font", "pvsneslibfont.png")

    def run(self):
        """Copy the font image to a user-selected directory."""

        try:

            target_dir = filedialog.askdirectory(title="Select the folder you want to generate the font")

            if not target_dir:
                messagebox.showerror("Fatal", "No directory selected")
                return -1
            
            target_path = Path(target_dir)
            shutil.copy(str(self.font_path), str(target_path))

        except Exception:

            messagebox.showerror("Fatal", "Error while copying files")
            return -1
        

        messagebox.showinfo("SNES-IDE", "Success!")
        return 0
    

class HTTPServer:
    def __init__(self, path, port=8000):
        self.path = path
        self.port = port
        self.process = None

    def run(self):
        os.chdir(self.path)
        self.process = subprocess.Popen(["python", "-m", "http.server", str(self.port)])
        webbrowser.open(f"http://localhost:{self.port}")

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("Server stopped.")

    def __del__(self):
        self.stop()

class TilesetExtractorOpener:

    def __init__(self, path_manager: PathManager):
        """Initialize the TilesetExtractorOpener with the path to the tileset extractor HTML file."""

        self.tse_path = path_manager.get_tool_path("libs", "pvsneslib", "tools", "tilesetextractor", "index.html")

    def run(self):
        """Open the tileset extractor in the default web browser."""

        # Register cleanup on exit
        server = HTTPServer(self.tse_path)
        atexit.register(server.stop)

        server.run()

class GfxToolsApp:

    def __init__(self):
        """Initialize the GfxToolsApp with a PathManager and set up the main window."""

        self.path_manager = PathManager()
        self.window = tk.Tk()
        self.window.title("grafic-tools")
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface with buttons for each tool."""

        self._add_button("Mode 3 and 7 tileset and tilemap editor", "Click to run M8TE", M8TEExecutor(self.path_manager).run)
        self._add_button("gfx4snes of pvsneslib! convert your image to .pic, .pal and .map format", "Click to select your image", Gfx4SnesExecutor(self.path_manager).run)
        self._add_button("SNES file info viewer(snestools of pvsneslib)", "Click to select your smc/sfc file", SnesToolsExecutor(self.path_manager).run)
        self._add_button("TMX and map converter(tmx2snes)", "Click to select your tmx and map files", Tmx2SnesExecutor(self.path_manager).run)
        self._add_button("The pvsneslib text font in your hands, just copy as font.png", "Click to generate the text font in the desired folder", FontCopier(self.path_manager).run)
        self._add_button("Online Tileset extractor by André Michelle", "Click to run tileset extractor", TilesetExtractorOpener(self.path_manager).run)

    def _add_button(self, label_text, button_text, command):
        """Create a label and button in the main window."""

        var = StringVar()

        label = tk.Label(self.window, textvariable=var, relief=SOLID)
        button = tk.Button(self.window, text=button_text, command=command)

        var.set(label_text)

        label.pack()
        button.pack()

    def run(self):
        """Run the main loop of the application."""

        self.window.mainloop()

if __name__ == "__main__":
    """Run the GfxToolsApp if this script is executed directly."""

    GfxToolsApp().run()
