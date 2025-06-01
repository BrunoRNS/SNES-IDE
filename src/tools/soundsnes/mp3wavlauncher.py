from pathlib import Path
import webbrowser
import sys

def get_executable_path():

    if getattr(sys, 'frozen', False):
        # PyInstaller executable
        print("executable path mode chosen")

        return Path(sys.executable).parent
    
    else:
        # Normal script
        print("Python script path mode chosen")

        return Path(__file__).absolute().parent


if __name__ == "__main__":

    print("Starting MP3 to WAV converter...")

    base_dir = Path(get_executable_path())

    # Path to local HTML file
    caminho_pagina = str(base_dir / 'web-wav-converter/index.html')

    # Open the web page in browser
    webbrowser.open_new_tab(f'file://{caminho_pagina}')
