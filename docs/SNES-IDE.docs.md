# SNES-IDE Documentation

Welcome to the official documentation for **SNES-IDE** – an open-source, cross-platform Integrated Development Environment for SNES game development using [pvsneslib](https://github.com/alekmaul/pvsneslib).

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Installation](#installation)
    - [Windows](#windows-installation)
    - [Linux (via Wine)](#linux-installation)
    - [Building from Source](#building-from-source)
5. [Getting Started](#getting-started)
6. [Project Structure](#project-structure)
7. [How SNES-IDE Works](#how-snes-ide-works)
8. [Batch Files & Shortcuts](#batch-files--shortcuts)
9. [Linux Scripts](#linux-scripts)
10. [Contributing](#contributing)
11. [FAQ](#faq)
12. [Troubleshooting](#troubleshooting)
13. [License](#license)
14. [Contact](#contact)

---

## Introduction

**SNES-IDE** is a user-friendly IDE for developing Super Nintendo (SNES) games in C and assembly, powered by pvsneslib. It aims to simplify the setup and workflow for hobbyists and professionals alike, providing tools, templates, and automation for building, compiling, and testing SNES ROMs.

---

## Features

- **Integrated Toolchain:** Uses 816-tcc and wla-dx for C and assembly.
- **Project Templates:** Quickly start new SNES projects.
- **Batch Shortcuts:** One-click access to editors, tools, and build scripts.
- **Cross-Platform:** Native on Windows; works on Linux via Wine.
- **Emulator Integration:** Test ROMs instantly with bsnes or snes9x.
- **Audio & Graphics Tools:** Convert and manage SNES assets.
- **Extensible:** Open-source, modular, and easy to contribute.

---

## System Requirements

- **Operating System:**  
  - Windows 10 or newer  
  - Linux (with Wine 9.0+)
- **Architecture:** x64, x86_64, or amd64 (not ARM)
- **RAM:** 2 GB minimum
- **Disk Space:** 200 MB minimum
- **Dependencies:**  
  - [Wine](https://www.winehq.org/) (Linux only)
  - Bash (Linux)
  - Python 3.x (for some scripts)
  - Optional: Notepad++, snes9x, bsnes

---

## Installation

### Windows Installation

1. **Download** the latest SNES-IDE release (zip) from the [releases page](https://github.com/BrunoRNS/SNES-IDE/releases/latest).
2. **Extract** the contents to a folder of your choice.
3. **Run** `INSTALL.bat` by double-clicking it. This will:
    - Create a `snes-ide` folder on your Desktop with shortcuts to all tools and scripts.
    - Copy the main executable and all required files.
    - Set up batch files for launching editors, tools, and the emulator.
4. **Check** your Desktop for the new `snes-ide` folder. All shortcuts are inside.

> **Note:** If you want to move the installation, delete the `snes-ide` folder and repeat the process.

---

### Linux Installation

SNES-IDE is designed for Windows, but works well on Linux using Wine. The project provides scripts to automate setup.

1. Download the latest release from [GitHub Releases](https://github.com/BrunoRNS/SNES-IDE/releases/latest).

2. Decompress the .zip to a folder of your choice.

3. Install Wine:  

     `sudo apt install wine`

4. Run configure shell file:

     ```sh
     cd /path/to/snes-ide/
     chmod +x ./linux/configure.sh
     bash ./linux/configure.sh
     ```

5. Follow the installer steps to generate a desktop icon or just run with `./linux/src/start.sh`.

---

### Building from Source

If you want to build SNES-IDE from source (for development or customization):

1. **Clone the repository:**

    ```bash
    git clone https://github.com/BrunoRNS/SNES-IDE.git
    cd SNES-IDE
    ```

2. **Follow the build instructions:**

    See [build/BUILDING_FROM_SOURCE.md](../build/BUILDING_FROM_SOURCE.md) for detailed steps.

3. **Run the installer:**

    - On Windows: Run `INSTALL.bat` from the output directory.
    - On Linux: The `setup.sh` already runs the installer for you.

> **Note:** If you encounter build errors, check the console log and open an issue or fix it with a pull request with details.

---

## Getting Started

1. **Create a New Project:**  
   Use the `create-new-project` shortcut or batch file to scaffold a new SNES project.

2. **Edit Your Code:**  
   Open your project in Notepad++ (or your preferred editor).

3. **Add Assets:**  
   Use `audio-tools` and `graphic-tools` to convert and add SNES-compatible assets.

4. **Compile:**  
   Use the `compiler` shortcut to build your project into a SNES ROM.

5. **Test:**  
   Use the `emulator` shortcut to run your ROM in bsnes or snes9x.

---

## Project Structure

A typical SNES-IDE project directory looks like:

```sh
snes-ide/
├── libs/
│   └── notepad++/
├── tools/
│   ├── audio-tools.exe
│   ├── gfx-tools.exe
│   ├── externTools.exe
│   ├── create-new-project.exe
│   ├── automatizer-batch.bat
│   └── ...
├── snes-ide.exe
├── INSTALL.bat
├── ...
```

- **Shortcuts** are created in `Desktop/snes-ide/`.
- **Source code** and assets are managed in your project folder.

---

## How SNES-IDE Works

- **Batch Files:**  
  SNES-IDE uses batch files as shortcuts to launch tools, editors, and scripts.  
  Example: `text-editor.bat` launches Notepad++.

- **Python Automation:**  
  Scripts like `snes-ide.py` and `automatizer.py` automate project setup, compilation, and asset management.

- **Linux Support:**  
  On Linux, Bash scripts and Wine are used to mimic the Windows environment and run the same tools.

- **Emulator Integration:**  
  The IDE can launch your compiled ROM in an emulator for instant testing.

---

## Batch Files & Shortcuts

**INSTALL.bat** creates the following shortcuts in your Desktop `snes-ide` folder:

- `text-editor.bat` → Notepad++
- `audio-tools.bat` → Audio asset converter
- `graphic-tools.bat` → Graphics asset converter
- `other-tools.bat` → External tools
- `create-new-project.bat` → Project template generator
- `compiler.bat` → Build your SNES ROM
- `emulator.bat` → Launch bsnes

- `snes-ide.exe` → All in one shortcut, main entry of snes-ide.

Each shortcut is a `.bat` or `.exe` file that launches the corresponding tool or script.

---

## Linux Scripts

- **setup.sh:** Main installer for Linux. Makes scripts executable, runs setup, and creates desktop shortcuts.
- **start.sh:** Launches SNES-IDE from the terminal.
- **Other scripts:** Handle Wine prefix setup, dependency installation, and running Windows batch files via Wine.

---

## Contributing

- Read [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) and [PULL_REQUEST_RULES.md](../PULL_REQUEST_RULES.md).
- Fork the repo and create a feature branch.
- Write clear, modular code with comments.
- Add or update tests as needed.
- Submit a pull request with a descriptive title and summary.

---

## FAQ

**Q: Can I use my own editor?**  
A: Yes! Notepad++ is provided, but you can use any editor.

**Q: Does it work on Mac?**  
A: Not officially, but you may try using Wine or a VM.

**Q: Where are my ROMs?**  
A: Compiled ROMs are usually in your project folder or a `Roms/` subdirectory.

**Q: How do I add new tools?**  
A: Place them in the `tools/` directory, they **must** be a python or dotnet tool.

---

## Troubleshooting

- **Wine errors:** Ensure Wine is installed and configured. Use `winecfg` to set up your prefix.
- **Missing dependencies:** Check the terminal output for missing tools or libraries.
- **Batch file issues:** On Linux, ensure all scripts are executable (`chmod +x`).
- **Installation problems:** Delete `.installed` and re-run `setup.sh` or `INSTALL.bat`.

---

## License

SNES-IDE is licensed under the [GNU GPL v3](../LICENSE.txt).

---

## Contact

- **GitHub:** [BrunoRNS/SNES-IDE](https://github.com/BrunoRNS/SNES-IDE)
- **Issues & Discussions:** Use the GitHub repository to report bugs or ask questions.

---

Happy coding and enjoy making SNES games!
