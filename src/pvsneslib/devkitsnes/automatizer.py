from tkinter import messagebox
from pathlib import Path
import tkinter as tk
import subprocess
import sys

def get_executable_path():
    """
    Returns the path of the executable or script.
    If the script is run as a PyInstaller executable, it returns the directory of the executable.
    If the script is run normally, it returns the directory of the script.
    """

    if getattr(sys, 'frozen', False):
        # PyInstaller executable
        print("Executable path mode chosen")

        return Path(sys.executable).parent
    
    else:
        # Normal script
        print("Python script path mode chosen")

        return Path(__file__).absolute().parent

class DebugModeSelector:
    
    def __init__(self):
        """Initialize the DebugModeSelector and ask for debug mode."""

        self.debug = self.ask_debug_mode()

    def ask_debug_mode(self):

        while True:

            response = input("Debug mode: yes(y) or no(n)?\n")

            match response:

                case 'y': return True
                case 'n': return False

                case _: print("Not valid response! just y or n, case sensitive!")

# Usage:
# DEBUG = DebugModeSelector().debug

class DragDropListbox(tk.Listbox):

    def __init__(self, master, **kw):
        """Initialize the DragDropListbox with single selection mode and bind events."""

        kw['selectmode'] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)

        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        """Set the current index based on the mouse click position."""

        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        """Shift the selection based on the mouse drag position."""

        i = self.nearest(event.y)

        if i < self.curIndex:

            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i

        elif i > self.curIndex:

            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i

class ReorderList:

    def __init__(self, items: list[str]):
        """Initialize the ReorderList with a list of items and create the GUI."""

        self.items: list[str] = items
        self.listbox: DragDropListbox
        self.root: tk.Tk

        self.reorder_list()


    def check_order(self):
        """Check the order of the listbox items and confirm with the user."""

        order = self.listbox.get(0, tk.END)

        if messagebox.askyesno("Confirmation", f"Linkfile order is correct?\n\n{order}"):

            self.root.quit()

            return order
        
        else:

            messagebox.showinfo("Order was not confirmed", "Please, reorder the list.")

    def add_element(self):
        """Add a new element to the listbox."""

        new_element = input("Write down the element you want to add to the list:\n")
        self.listbox.insert(tk.END, new_element)

    def remove_element(self):
        """Remove the selected element from the listbox."""

        selected_item_index = self.listbox.curselection()

        if selected_item_index:

            self.listbox.delete(selected_item_index)

    def reorder_list(self) -> list[str]:
        """Create the GUI for reordering the listbox items."""
    
        self.root = tk.Tk()
        self.root.title("Linkfile reoderer")
        self.root.geometry("300x700")

        self.label = tk.Label(self.root, text="Move the linkfile elements to change it order:")
        self.label.pack(pady=10)

        self.listbox = DragDropListbox(self.root, bg="white", fg="black", width=40, height=25)
        self.listbox.pack(pady=10)

        for item in self.items:
            self.listbox.insert(tk.END, item)

        self.insertb = tk.Button(self.root, text="Insert new element", command=self.add_element)
        self.insertb.pack(pady=10)
    
        self.removeb = tk.Button(self.root, text="Remove selected element", command=self.remove_element)
        self.removeb.pack(pady=10)
    
        self.button = tk.Button(self.root, text="Confirm Order", command=self.check_order)
        self.button.pack(pady=10)

        self.root.mainloop()

        return list(self.listbox.get(0, tk.END))


class SNESAutomatizer:

    def __init__(self, src_dir: Path, memory_map: str, speed: str, debug: bool):
        """Initialize the SNESAutomatizer with source directory, memory map, speed, and debug mode."""

        self.base_dir = Path(get_executable_path()).parent

        print(self.base_dir)

        self.src_dir = Path(src_dir)

        self.memory_map = memory_map

        self.speed = speed

        self.debug = debug

        if not self.src_dir.exists() or not self.src_dir.is_dir():

            raise Exception("Path does not exists or is not a path")

        self.lib_dir = self._get_lib_dir()
        self.tools_dir = self.base_dir / 'tools'
        self.devkit_dir = self.base_dir / 'devkitsnes'
        self.asm_files: list[Path] = []
        self.c_files: list[Path] = []

        self.cc = self.devkit_dir / 'bin' / '816-tcc.exe'
        self.assembler = self.devkit_dir / 'bin' / 'wla-65816.exe'
        self.linker = self.devkit_dir / 'bin' / 'wlalink.exe'
        self.opt = self.tools_dir / '816-opt.exe'
        self.ctf = self.tools_dir / 'constify.exe'

    def _get_lib_dir(self):
        """Return the library directory based on memory map and speed."""

        if self.memory_map == "HIROM" and self.speed == "FAST":

            return self.base_dir / 'lib' / 'HiROM_FastROM'
        
        elif self.memory_map == "LOROM" and self.speed == "FAST":

            return self.base_dir / 'lib' / 'LoROM_FastROM'
        
        elif self.memory_map == "HIROM" and self.speed == "SLOW":

            return self.base_dir / 'lib' / 'HiROM_SlowROM'
        
        elif self.memory_map == "LOROM" and self.speed == "SLOW":

            return self.base_dir / 'lib' / 'LoROM_SlowROM'
        
        else:

            raise Exception("Error mapping memory...")
        

    def collect_files(self):
        """Collect all C and ASM files from the source directory."""

        if not self.src_dir.exists() or not self.src_dir.is_dir():
            raise Exception("Source directory does not exist or is not a directory.")

        self.c_files = list(self.src_dir.rglob("*.c"))
        self.asm_files = list(self.src_dir.rglob("*.asm"))

    def compile_c_files(self):
        """Compile C files to assembly files using the devkit tools."""

        for c_file in self.c_files:

            ps_file = c_file.with_suffix('.ps')
            asp_file = c_file.with_suffix('.asp')
            asm_file = c_file.with_suffix('.asm')
            obj_file = c_file.with_suffix('.obj')

            args = [self.cc, '-I' + str(self.devkit_dir / "include"), '-Wall', '-c', c_file]

            if self.memory_map == "HIROM":
                args.append('-H')

            if self.speed == "FAST":
                args.append('-F')

            args += ['-o', ps_file]
            subprocess.run(args)

            with open(asp_file, "w") as f:

                subprocess.run([self.opt, ps_file], stdout=f)

            subprocess.run([self.ctf, c_file, asp_file, asm_file])
            subprocess.run([self.assembler, '-d', '-s', '-x', '-o', obj_file, asm_file])

    def assemble_asm_files(self):
        """Assemble ASM files to object files using the assembler."""

        for asm_file in self.asm_files:

            subprocess.run([self.assembler, '-d', '-s', '-x', '-o', asm_file.with_suffix('.obj'), asm_file])

    def create_linkfile(self):
        """Create a linkfile for the linker with all object files and libraries."""

        linkfile: list[str] = [str(obj_file.with_suffix('.obj')) for obj_file in self.asm_files + self.c_files]
        linkfile.insert(0, "[objects]")

        for file in self.lib_dir.rglob("*"):

            linkfile.append(str(file))

        linkfile = ReorderList(linkfile).reorder_list()

        linkfile_path = self.src_dir / 'linkfile'

        with open(linkfile_path, 'w') as f:

            f.write('\n'.join(linkfile))

        return linkfile_path

    def link(self, linkfile_path):
        """Link the object files and libraries to create the final output file."""

        if not linkfile_path.exists():
            raise Exception("Linkfile does not exist. Please create it first.")
        
        print("Linking files...")

        subprocess.run([
            self.linker, '-d', '-s', '-c', '-v', '-A', '-L', self.lib_dir,
            linkfile_path, self.src_dir / 'output.sfc'
        ])

        print("\nBuild finished succesfully!\n")

    def cleanup(self):
        """Remove temporary files created during the build process."""

        try:

            for c_file in self.c_files:

                for ext in ['.ps', '.asp', '.asm', '.obj']:

                    Path.unlink(c_file.with_suffix(ext), missing_ok=True)

            for asm_file in self.asm_files:

                Path.unlink(asm_file.with_suffix('.obj'), missing_ok=True)


            Path.unlink(self.src_dir / "linkfile", missing_ok=True)

            Path.unlink(self.src_dir / 'output.sym', missing_ok=True)
            
        except Exception as e:

            print(f"Cleanup error: {e}")

        print("TEMP FILES REMOVED SUCCESFULLY!")

        input("PRESS ANY KEY TO EXIT...")


    def debug_info(self):
        """Display debug information and instructions for the user."""

        print("Debug files in source directory: .ps -> tcc_dbg, .asp -> opt_dbg, .asm -> constifier debug, .sym -> linker debug")
        input("PRESS ANY KEY TO EXIT...")

    def run(self):
        """Run the automatizer to collect files, compile C files, assemble ASM files, create linkfile, and link."""
        print("Starting SNES Automatizer...")

        self.collect_files()
        self.compile_c_files()
        self.assemble_asm_files()

        linkfile_path = self.create_linkfile()

        self.link(linkfile_path)

        if not self.debug:

            self.cleanup()

        else:

            self.debug_info()

if __name__ == "__main__":

    base_dir = Path(get_executable_path()).parent

    src_dir = Path(sys.argv[1])
    memory_map: str = sys.argv[2]
    speed: str = sys.argv[3]

    if not src_dir.exists() or not src_dir.is_dir():

        raise Exception("Source directory does not exist or is not a directory.")
    
    if memory_map not in {"HIROM", "LOROM"}:
        
        raise Exception("Memory map must be either 'HIROM' or 'LOROM'.")

    automatizer = SNESAutomatizer(
        src_dir=src_dir, 
        memory_map=memory_map, 
        speed=speed, 
        debug=DebugModeSelector().ask_debug_mode()
    )

    automatizer.run()
