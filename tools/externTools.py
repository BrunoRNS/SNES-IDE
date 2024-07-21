import webbrowser
import tkinter as tk

window = tk.Tk()

def open_mj():
    webbrowser.open_new_tab("https://snes.party/")

def open_sm():
    webbrowser.open_new_tab("https://musiclab.chromeexperiments.com/Song-Maker/")

mj = tk.Button(window, text="Open Multiplayer server to upload your ROM", command = open_mj)
mj.pack()

sm = tk.Button(window, text="Open Chrome Soundmaker to create wav sound", command = open_sm)
sm.pack()

window.mainloop()
