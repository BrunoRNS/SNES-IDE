# Default libraries
import sys
import os
import tkinter as tk
import subprocess
from tkinter import StringVar, SOLID
from tkinter import messagebox, filedialog

# Installed libraries
from pathlib import Path

def get_executable_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller executable
        print("Executable path mode chosen")
        return os.path.dirname(sys.executable)
    else:
        # Normal script
        print("Python script path mode chosen")
        return os.path.dirname(os.path.abspath(__file__))

window = tk.Tk()

# SNES-IDE home's path
root = Path(get_executable_path()).parent

window.title("Audio-tools")

def first():
    try:
        wav2mp3 = root / "tools" / "soundsnes" / "wav2mp3_converter" / "bin" / "Debug" / "wav2mp3_converter.exe"
        subprocess.run([wav2mp3])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {wav2mp3}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")

var1 = StringVar()
label1 = tk.Label(window, textvariable=var1, relief=SOLID)
button1 = tk.Button(window, text="Click to select your wav file", command=first)
var1.set("WAV(uncompressed) to MP3 converter")
label1.pack()
button1.pack()


def second():
    try:
        local = root / "tools" / "soundsnes" / "mp3wavlauncher.exe"
        subprocess.run([local])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {local}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")

var2 = StringVar()
label2 = tk.Label(window, textvariable=var2, relief=SOLID)
button2 = tk.Button(window, text="Click to select your mp3 file", command=second)
var2.set("MP3 to WAV(uncompressed) converter with Hz and channels control")
label2.pack()
button2.pack()


def third():
    try:
        snesbrr = root / "libs" / "pvsneslib" / "tools" / "snesbrr.exe"
        input_file = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if input_file:
            input_file: Path = Path(input_file)
        else:
            messagebox.showerror("Error", "Input file does not exist")
            return -1
        subprocess.run([snesbrr, "-e", input_file, str(input_file).split('.')[0] + ".brr"])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {snesbrr}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")

var3 = StringVar()
label3 = tk.Label(window, textvariable=var3, relief=SOLID)
button3 = tk.Button(window, text="Click to select your wav file", command=third)
var3.set("WAV(uncompressed) to BRR(snes format) converter")
label3.pack()
button3.pack()

def forth():
    try:
        snesbrr = root / "libs" / "pvsneslib" / "tools" / "snesbrr.exe"
        input_file = filedialog.askopenfilename(filetypes=[("BRR files", "*.brr")])
        if input_file:
            input_file: Path = Path(input_file)
        else:
            messagebox.showerror("Error", "Input file does not exist")
            return -1
        subprocess.run([snesbrr, "-d", input_file, str(input_file).split('.')[0] + ".wav"])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {snesbrr}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")
        
var4 = StringVar()
label4 = tk.Label(window, textvariable=var4, relief=SOLID)
button4 = tk.Button(window, text="Click to select your brr file", command=forth)
var4.set("BRR(snes format) to WAV(uncompressed sound) converter")
label4.pack()
button4.pack()

def fifth():
    try:
        tracker = root / "tools" / "soundsnes" / "tracker" / "schismtracker.exe"
        subprocess.run([tracker])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {tracker}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")

var5 = StringVar()
label5 = tk.Label(window, textvariable=var5, relief=SOLID)
button5 = tk.Button(window, text="Click to run SCHISMTRACKER!", command=fifth)
var5.set("Create your impulse tracker sound for snes games!")
label5.pack()
button5.pack()

def sixth():
    try:
        snesmod = root / "libs" / "pvsneslib" / "tools" / "smconv.exe"
        input_file = filedialog.askopenfilename(filetypes=[("Impulse Tracker files", "*.it")])
        if input_file:
            input_file: Path = Path(input_file)
        else:
            messagebox.showerror("Error", "Input file does not exist")
            return -1
        subprocess.run([snesmod, input_file], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {snesmod}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")

var6 = StringVar()
label6 = tk.Label(window, textvariable=var6, relief=SOLID)
button6 = tk.Button(window, text="Click to select your it file", command=sixth)
var6.set("Impulse Tracker to SPC(snes' SPC-700 sound file) converter")
label6.pack()
button6.pack()

def seventh():
    try:
        snesmod = root / "libs" / "pvsneslib" / "tools" / "smconv.exe"
        input_file = filedialog.askopenfilename(filetypes=[("Impulse Tracker files", "*.it")])
        if input_file:
            input_file: Path = Path(input_file)
        else:
            messagebox.showerror("Error", "Input file does not exist")
            return -1
        subprocess.run([snesmod,"-s","-o","soundbank", input_file],cwd=os.path.dirname(input_file), check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {snesmod}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")
        
var7 = StringVar()
label7 = tk.Label(window, textvariable=var7, relief=SOLID)
button7 = tk.Button(window, text="Click to select your it file", command=seventh)
var7.set("Impulse tracker to LoROM SNES' soundbank converter")
label7.pack()
button7.pack()

def eighth():
    try:
        snesmod = root / "libs" / "pvsneslib" / "tools" / "smconv.exe"
        input_file = filedialog.askopenfilename(filetypes=[("Impulse Tracker files", "*.it")])
        if input_file:
            input_file: Path = Path(input_file)
        else:
            messagebox.showerror("Error", "Input file does not exist")
            return -1
        subprocess.run([snesmod,"-s","-i","-o","soundbank", input_file],cwd=os.path.dirname(input_file), check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {snesmod}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")

var8 = StringVar()
label8 = tk.Label(window, textvariable=var8, relief=SOLID)
button8 = tk.Button(window, text="Click to select your it file", command=eighth)
var8.set("Impulse tracker to HiROM SNES' soundbank converter")
label8.pack()
button8.pack()


window.mainloop()
