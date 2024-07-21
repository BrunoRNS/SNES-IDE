# Default libraries
import sys
import os
import shutil
import tkinter as tk
import subprocess
import webbrowser
from tkinter import StringVar, messagebox, filedialog, SOLID

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

window.title("grafic-tools")

def first():
    try:
        m8te = root / "libs" / "M8TE" / "bin" / "M8TE.exe"
        subprocess.run([m8te])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {m8te}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")

var1 = StringVar()
label1 = tk.Label(window, textvariable=var1, relief=SOLID)
button1 = tk.Button(window, text="Click to run M8TE", command=first)
var1.set("Mode 3 and 7 tileset and tilemap editor")
label1.pack()
button1.pack()


def second():
    try:
        nwindow = tk.Tk()
        nwindow.title("Chose options for the gfx4snes")
        local = root / "libs" / "pvsneslib" / "tools" / "gfx4snes.exe"
        input_file = filedialog.askopenfilename(filetypes=[("your image(PNG or BMP)", ["*.png", "*.bmp"])])
        if input_file:
            pass
        else:
            nwindow.destroy()
            messagebox.showerror("Fatal", "No Input file selected")
            return None
        options = [
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
                StringVar(),
        ]
        stroptions = [
                str("-b,        add blank tile management (for multiple bgs)"),
                str("-s,        size of image blocks in pixels {[8],16,32,64} <int>"),
                str("-k,        output in packed pixel format"),
                str("-z,        add blank tile management (for multiple bgs)"),
                str("-W,        width of image block in pixels <int>"),
                str("-H,        height of image block in pixels <int>"),
                str("-f,        generate the whole picture with an offset for tile number {0..2047}"),
                str("-m,        include map for output"),
                str("-g,        include high priority bit in map"),
                str("-y,        generate map in pages of 32x32 (good for scrolling)"),
                str("-R,        no tile reduction (not advised)"),
                str("-M,        convert the whole picture for mode 1,5,6 or 7 format {[1],5,6,7} <int>"),
                str("-a,        rearrange palette and preserve palette numbers in tilemap"),
                str("-d,        palette rounding (to a maximum value of 63)"),
                str("-e,        palette entry to add to map tiles {0..7} <int>"),
                str("-o,        number of colors to output to filename.pal {0..256} <int>"),
                str("-p,        include palette for output"),
                str("-u,        number of colors to use {4,16,128,[256]} <int>"),
        ]
        def opt():
            global list_
            list_ = list()
            for i, op in enumerate(options):
                if op.get() == "1":
                    var: str = stroptions[i]
                    list_.append(var[:2])
                    if var.endswith("<int>") and "-s" in var:
                        list_.append(int_entry_s.get())
                    if var.endswith("<int>") and "-W" in var:
                        list_.append(int_entry_w.get())
                    if var.endswith("<int>") and "-H" in var:
                        list_.append(int_entry_h.get())
                    if var.endswith("<int>") and "-e" in var:
                        list_.append(int_entry_e.get())
                    if var.endswith("<int>") and "-o" in var:
                        list_.append(int_entry_o.get())
                    if var.endswith("<int>") and "-M" in var:
                        list_.append(int_entry_m.get())
                    if var.endswith("<int>") and "-u" in var:
                        list_.append(int_entry_u.get())
                else:
                    print(op.get())
                    pass
            nwindow.destroy()
            if input_file.lower().endswith('.bmp'):
                command = [local] + list_ + ['-t', 'bmp', '-i', input_file]
            else:
                command = [local] + list_ + ['-i', input_file]
            messagebox.showinfo("Result: ", subprocess.run(command, cwd=str(Path(input_file).parent), capture_output=True))
            return None
            
        int_entry_s = tk.Entry(nwindow)
        int_entry_w = tk.Entry(nwindow)
        int_entry_h = tk.Entry(nwindow)
        int_entry_e = tk.Entry(nwindow)
        int_entry_o = tk.Entry(nwindow)
        int_entry_m = tk.Entry(nwindow)
        int_entry_u = tk.Entry(nwindow)
        for i, var in enumerate(options):
            tk.Checkbutton(nwindow, text=stroptions[i], variable=var, onvalue="1", offvalue="0").pack(anchor="w")
            if stroptions[i].endswith("<int>") and "-s" in stroptions[i]:
                int_entry_s.pack()
            if stroptions[i].endswith("<int>") and "-W" in stroptions[i]:
                int_entry_w.pack()
            if stroptions[i].endswith("<int>") and "-H" in stroptions[i]:
                int_entry_h.pack()
            if stroptions[i].endswith("<int>") and "-e" in stroptions[i]:
                int_entry_e.pack()
            if stroptions[i].endswith("<int>") and "-o" in stroptions[i]:
                int_entry_o.pack()
            if stroptions[i].endswith("<int>") and "-M" in stroptions[i]:
                int_entry_m.pack()
            if stroptions[i].endswith("<int>") and "-u" in stroptions[i]:
                int_entry_u.pack()
        
        tk.Button(nwindow, text="Run", command=opt).pack()
        nwindow.mainloop()
        
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {local}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")

var2 = StringVar()
label2 = tk.Label(window, textvariable=var2, relief=SOLID)
button2 = tk.Button(window, text="Click to select your image", command=second)
var2.set("gfx4snes of pvsneslib! convert your image to .pic, .pal and .map format")
label2.pack()
button2.pack()


def third():
    try:
        snestools = root / "libs" / "pvsneslib" / "tools" / "snestools.exe"
        input_file = filedialog.askopenfilename(filetypes=[("your snes ROM", ["*.smc", "*.sfc"])])
        if input_file:
            input_file: Path = Path(input_file)
        else:
            messagebox.showerror("Error", "Input file does not exist")
            return -1
        messagebox.showinfo("snestools", subprocess.run([snestools, input_file], capture_output=True, text=True))
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {snestools}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")

var3 = StringVar()
label3 = tk.Label(window, textvariable=var3, relief=SOLID)
button3 = tk.Button(window, text="Click to select your smc/sfc file", command=third)
var3.set("SNES file info viewer(snestools of pvsneslib)")
label3.pack()
button3.pack()

def forth():
    try:
        tmx2snes = root / "libs" / "pvsneslib" / "tools" / "tmx2snes.exe"
        input_file = filedialog.askopenfilename(filetypes=[("tmxfilename", "*")])
        input_file2 = filedialog.askopenfilename(filetypes=[("mapfilename", "*")])
        if input_file and input_file2:
            input_file: Path = Path(input_file)
        else:
            messagebox.showerror("Error", "Input file does not exist")
            return -1
        subprocess.run([tmx2snes, input_file, input_file2], cwd=str(Path(input_file).parent))
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fatal", f"Error while executing {tmx2snes}: {e}")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")
        
var4 = StringVar()
label4 = tk.Label(window, textvariable=var4, relief=SOLID)
button4 = tk.Button(window, text="Click to select your tmx and map files", command=forth)
var4.set("TMX and map converter(tmx2snes)")
label4.pack()
button4.pack()

def fifth():
    try:
        font = root / "font" / "pvsneslibfont.png"
        shutil.copyfile(str(font), str(Path(filedialog.askdirectory(title="Select the folder you want to generate the font")) / "font.png"))
    except:
        messagebox.showerror("Fatal", f"Error while copying files")
    else:
        messagebox.showinfo("SNES-IDE", "Success!")

var5 = StringVar()
label5 = tk.Label(window, textvariable=var5, relief=SOLID)
button5 = tk.Button(window, text="Click to generate the text font in the desired folder", command=fifth)
var5.set("The pvsneslib text font in your hands, just copy as font.png")
label5.pack()
button5.pack()

def sixth():
    tse = root / "libs" / "pvsneslib" / "tools" / "tilesetextractor" / "index.html"
    webbrowser.open("file:///" + str(tse))

var6 = StringVar()
label6 = tk.Label(window, textvariable=var6, relief=SOLID)
button6 = tk.Button(window, text="Click to run tileset extractor", command=sixth)
var6.set("Online Tileset extractor by André Michelle")
label6.pack()
button6.pack()


window.mainloop()
