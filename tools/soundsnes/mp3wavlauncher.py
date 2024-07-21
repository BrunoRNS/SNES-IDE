import webbrowser
import sys
from pathlib import Path
import os

def get_executable_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller executable
        print("executable path mode chosen")
        return os.path.dirname(sys.executable)
    else:
        # Normal script
        print("Python script path mode chosen")
        return os.path.dirname(os.path.abspath(__file__))


base_dir = Path(get_executable_path())

# Path to local HTML file
caminho_pagina = str(base_dir / 'web-wav-converter/index.html')

# Open the web page in browser
webbrowser.open_new_tab(f'file://{caminho_pagina}')
