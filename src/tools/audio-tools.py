# Audio tools for SNES-IDE

from tkinter import messagebox, filedialog, StringVar, SOLID
from pathlib import Path

import tkinter as tk

import subprocess
import sys

def get_executable_path() -> Path:

    if getattr(sys, 'frozen', False):
        # PyInstaller executable
        print("Executable path mode chosen")

        return Path(sys.executable).parent
    
    else:
        # Normal script
        print("Python script path mode chosen")

        return Path(__file__).absolute().parent

class AudioToolsApp:

    def __init__(self):
        """Initialize the Audio Tools application."""

        self.window = tk.Tk()

        # SNES-IDE home's path
        self.root = Path(get_executable_path()).parent

        self.window.title("Audio-tools")

        self.setup_widgets()
        self.window.mainloop()

    def setup_widgets(self):
        """Set up the widgets for the Audio Tools application."""

        self.var1 = StringVar()
        self.label1 = tk.Label(self.window, textvariable=self.var1, relief=SOLID)
        self.button1 = tk.Button(self.window, text="Click to select your wav file", command=self.first)
        self.var1.set("WAV(uncompressed) to MP3 converter")
        self.label1.pack()
        self.button1.pack()

        self.var2 = StringVar()
        self.label2 = tk.Label(self.window, textvariable=self.var2, relief=SOLID)
        self.button2 = tk.Button(self.window, text="Click to select your mp3 file", command=self.second)
        self.var2.set("MP3 to WAV(uncompressed) converter with Hz and channels control")
        self.label2.pack()
        self.button2.pack()

        self.var3 = StringVar()
        self.label3 = tk.Label(self.window, textvariable=self.var3, relief=SOLID)
        self.button3 = tk.Button(self.window, text="Click to select your wav file", command=self.third)
        self.var3.set("WAV(uncompressed) to BRR(snes format) converter")
        self.label3.pack()
        self.button3.pack()

        self.var4 = StringVar()
        self.label4 = tk.Label(self.window, textvariable=self.var4, relief=SOLID)
        self.button4 = tk.Button(self.window, text="Click to select your brr file", command=self.forth)
        self.var4.set("BRR(snes format) to WAV(uncompressed sound) converter")
        self.label4.pack()
        self.button4.pack()

        self.var5 = StringVar()
        self.label5 = tk.Label(self.window, textvariable=self.var5, relief=SOLID)
        self.button5 = tk.Button(self.window, text="Click to run SCHISMTRACKER!", command=self.fifth)
        self.var5.set("Create your impulse tracker sound for snes games!")
        self.label5.pack()
        self.button5.pack()

        self.var6 = StringVar()
        self.label6 = tk.Label(self.window, textvariable=self.var6, relief=SOLID)
        self.button6 = tk.Button(self.window, text="Click to select your it file", command=self.sixth)
        self.var6.set("Impulse Tracker to SPC(snes' SPC-700 sound file) converter")
        self.label6.pack()
        self.button6.pack()

        self.var7 = StringVar()
        self.label7 = tk.Label(self.window, textvariable=self.var7, relief=SOLID)
        self.button7 = tk.Button(self.window, text="Click to select your it file", command=self.seventh)
        self.var7.set("Impulse tracker to LoROM SNES' soundbank converter")
        self.label7.pack()
        self.button7.pack()

        self.var8 = StringVar()
        self.label8 = tk.Label(self.window, textvariable=self.var8, relief=SOLID)
        self.button8 = tk.Button(self.window, text="Click to select your it file", command=self.eighth)
        self.var8.set("Impulse tracker to HiROM SNES' soundbank converter")
        self.label8.pack()
        self.button8.pack()

    def first(self):
        """Convert WAV files to MP3 using the converter."""

        wav2mp3: Path = self.root / "tools" / "soundsnes" / "wav2mp3_converter" / "wav2mp3_converter.exe"
        
        try:

            if not wav2mp3.exists():

                messagebox.showerror("Error", f"Executable {wav2mp3} does not exist")
                return -1
    
            subprocess.run([wav2mp3])

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {wav2mp3}: {e}")
            return -1
        
        messagebox.showinfo("SNES-IDE", "Success!")

        return 0


    def second(self):
        """Convert MP3 files to WAV the converter."""

        local: Path = self.root / "tools" / "soundsnes" / "mp3wavlauncher.exe"

        if not local.exists():

            local = local.parent / "mp3wavlauncher.bat"

        try:

            if not local.exists():

                messagebox.showerror("Error", f"Executable {local} does not exist")
                return -1
            
            subprocess.run([local])

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {local}: {e}")
            return -1

        messagebox.showinfo("SNES-IDE", "Success!")

        return 0

    def third(self):
        """Convert WAV files to BRR using snesbrr converter."""
        
        snesbrr: Path = self.root / "libs" / "pvsneslib" / "tools" / "snesbrr.exe"

        try:

            if not snesbrr.exists():

                messagebox.showerror("Error", f"Executable {snesbrr} does not exist")
                return -1
            
            if not snesbrr.is_file():
                
                messagebox.showerror("Error", f"Executable {snesbrr} is not a file")
                return -1
            
            input_file = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])

            if input_file:

                input_file = Path(input_file)

            else:

                messagebox.showerror("Error", "Input file does not exist")
                return -1
            
            if not input_file.exists():

                messagebox.showerror("Error", f"Input file {input_file} does not exist")
                return -1
            
            subprocess.run([snesbrr, "-e", input_file, str(input_file).split('.')[0] + ".brr"])

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {snesbrr}: {e}")
            return -1

        messagebox.showinfo("SNES-IDE", "Success!")
        return 0

    def forth(self):
        """Convert BRR files to WAV using snesbrr converter."""

        snesbrr: Path = self.root / "libs" / "pvsneslib" / "tools" / "snesbrr.exe"

        try:

            if not snesbrr.exists():
                
                messagebox.showerror("Error", f"Executable {snesbrr} does not exist")
                return -1
            
            if not snesbrr.is_file():

                messagebox.showerror("Error", f"Executable {snesbrr} is not a file")
                return -1

            input_file = filedialog.askopenfilename(filetypes=[("BRR files", "*.brr")])

            if input_file:
                input_file = Path(input_file)

            else:
                messagebox.showerror("Error", "Input file does not exist")
                return -1
            
            subprocess.run([snesbrr, "-d", input_file, str(input_file).split('.')[0] + ".wav"])

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {snesbrr}: {e}")
            return -1

        
        messagebox.showinfo("SNES-IDE", "Success!")
        return 0

    def fifth(self):
        """Run SCHISMTRACKER to create impulse tracker sound for SNES games."""

        tracker: Path = self.root / "tools" / "soundsnes" / "tracker" / "schismtracker.exe"

        try:
            
            subprocess.run([tracker])

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {tracker}: {e}")
            return -1
        
        messagebox.showinfo("SNES-IDE", "Success!")
        return 0

    def sixth(self):
        """Convert Impulse Tracker files to SPC using smconv."""

        snesmod: Path = self.root / "libs" / "pvsneslib" / "tools" / "smconv.exe"
        try:
            
            input_file = filedialog.askopenfilename(filetypes=[("Impulse Tracker files", "*.it")])

            if input_file:
                input_file = Path(input_file)

            else:
                messagebox.showerror("Error", "Input file does not exist")
                return -1
            
            subprocess.run([snesmod, input_file], check=True)

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {snesmod}: {e}")
            return -1

        messagebox.showinfo("SNES-IDE", "Success!")
        return 0

    def seventh(self):
        """Convert Impulse Tracker files to LoROM SNES' soundbank using smconv."""
        snesmod: Path = self.root / "libs" / "pvsneslib" / "tools" / "smconv.exe"

        try:

            input_file = filedialog.askopenfilename(filetypes=[("Impulse Tracker files", "*.it")])

            if input_file:

                input_file = Path(input_file)

            else:

                messagebox.showerror("Error", "Input file does not exist")

                return -1
            
            subprocess.run([snesmod, "-s", "-o", "soundbank", input_file], cwd=Path(input_file).parent, check=True)

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {snesmod}: {e}")
            return -1

        messagebox.showinfo("SNES-IDE", "Success!")
        return 0

    def eighth(self):
        """Convert Impulse Tracker files to HiROM SNES' soundbank using smconv."""

        snesmod: Path = self.root / "libs" / "pvsneslib" / "tools" / "smconv.exe"

        try:

            input_file = filedialog.askopenfilename(filetypes=[("Impulse Tracker files", "*.it")])

            if input_file:

                input_file = Path(input_file)

            else:

                messagebox.showerror("Error", "Input file does not exist")
                return -1
            
            subprocess.run([snesmod, "-s", "-i", "-o", "soundbank", input_file], cwd=Path(input_file).parent, check=True)

        except subprocess.CalledProcessError as e:

            messagebox.showerror("Fatal", f"Error while executing {snesmod}: {e}")


        messagebox.showinfo("SNES-IDE", "Success!")
        return 0

if __name__ == "__main__":
    """Main entry point for the Audio Tools application."""

    app = AudioToolsApp()

    print("Audio tools application has been started successfully.")
