from webbrowser import open_new_tab
import tkinter as tk

class ExternTools:

    def __init__(self):
        """Initialize the ExternTools class."""

        # URLs for external tools
        self.mj_url = "https://snes.party/"
        self.sm_url = "https://musiclab.chromeexperiments.com/Song-Maker/"


    def open_mj(self):
        """Open the Multiplayer server URL in a new browser tab."""

        open_new_tab(self.mj_url)


    def open_sm(self):
        """Open the Chrome Soundmaker URL in a new browser tab."""

        open_new_tab(self.sm_url)


    def startWindow(self):
        """Create and start the GUI window for external tools."""

        self.window = tk.Tk()
        self.window.title("External Tools")
        self.window.geometry("300x100")

        mj_button = tk.Button(self.window, text="Open Multiplayer server to upload your ROM", command=self.open_mj)
        mj_button.pack(pady=10)

        sm_button = tk.Button(self.window, text="Open Chrome Soundmaker to create wav sound", command=self.open_sm)
        sm_button.pack(pady=10)

        self.window.mainloop()


if __name__ == "__main__":

    externtools = ExternTools()

    externtools.startWindow()
