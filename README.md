# <img src="./assets/icons/icon.png" alt="SNES-IDE" width="46" style="vertical-align:middle;margin-right:5px;"> SNES-IDE: Your Journey into Snes Game Development

## What Is SNES-IDE?

SNES-IDE is an open-source, cross-platform Integrated Development Environment (IDE) designed for creating SNES games using [pvsneslib](https://github.com/alekmaul/pvsneslib).  
It works natively on Windows and is fully supported on Linux via Wine, with scripts and automation for both platforms.

- **Languages:** C (main) and some assembly (65816 and spc700).
- **Compilers:** [816-tcc](https://github.com/alekmaul/tcc) and [wla-dx](https://github.com/vhelin/wla-dx) from pvsneslib.
- **Main Library:** [pvsneslib](https://github.com/alekmaul/pvsneslib) version 4.3.
- **Emulator:** [bsnes](https://github.com/bsnes-emu/bsnes) for testing.
- **Cross-platform:** Native on Windows, works on Linux (via Wine) with dedicated scripts.
- **Build from Source:** Full support for building all tools and the IDE itself from source.

## Why Choose SNES-IDE?

- **Cross-Platform:** Develop on Windows or Linux (via Wine).
- **All-in-One:** Integrated toolchain, asset converters, and project templates.
- **Easy Start:** One-click project creation and build scripts.
- **Open Source:** Free, extensible, and community-driven.
- **Learn & Create:** Ideal for learning C and SNES hardware, with lots of examples and documentation.

## Installation Requirements

- **Operating System:** Windows 10+ or Linux Debian/Ubuntu (with Wine 9.0+).
- **Architecture:** x64, x86_64, or amd64 (not compatible with ARM).
- **Minimum Resources:** 2 GB RAM, 200 MB disk space.

### Dependencies

- **Dependencies:**
  - **Windows:** OpenGL 3.2+ video driver or Direct3D 9.0.
  - **Linux:** For linux, only Wine 9.0+ installed and configured is previously required.

- **Building from Source Dependencies:**
  - **Windows:** OpenGL 3.2+ video driver or Direct3D 9.0, Python 3.8 or newer, pip and PyInstaller;
  - **Linux:** Bash, Wine 9.0+ and Python 3.8 or newer;

## Getting Started

### 1. Download & Install

- **Windows:**
  1. Download the latest release from [GitHub Releases](https://github.com/BrunoRNS/SNES-IDE/releases/latest).
  2. Decompress the .zip to a folder of your choice.
  3. Double-click `INSTALL.bat` to set up SNES-IDE and create shortcuts on your Desktop.

- **Linux:**
  1. Download the .deb package from the latest release: [GitHub Releases](https://github.com/BrunoRNS/SNES-IDE/releases/latest).

  2. Install Wine:  

     `sudo apt install wine`

  3. Install SNES-IDE:

     ```sh
     sudo apt install snes-ide_xyz.deb
     ```

  4. Execute `snes-ide` in the terminal.

### 2. Building from Source

- Clone the repo:  
  `git clone https://github.com/BrunoRNS/SNES-IDE.git`
- Follow the [build instructions](./build/BUILDING_FROM_SOURCE.md) to build all tools and the IDE from source.
- After building, run the installer as above.

### 3. Shortcuts Generated

After installation, these shortcuts are created:

- **text-editor** – [Notepad++](https://github.com/notepad-plus-plus/notepad-plus-plus) .
- **audio-tools** – Convert and manage SNES-compatible audio assets.
- **graphic-tools** – Convert and manage SNES-compatible graphics.
- **other-tools** – Access additional utilities.
- **create-new-project** – Scaffold a new project from a template.
- **compiler** – Compile your project into a SNES ROM.
- **emulator** – Launch your ROM in bsnes.

- **snes-ide** – All in one shorcut, the main entry of snes-ide, here you can basically choose which tool you want to start.

> **Note:** Shortcuts are created in `Desktop/snes-ide/` on Windows, or as a desktop entry on Linux if its choosed to while building from source.

## How can I use it?

Once installed, you can create and build SNES games easily:

1. Use **create-new-project** to start a new project.
2. Edit your code with **text-editor** or any editor you like.
3. Add assets using **audio-tools** and **graphic-tools** and **other-tools**.
4. Compile with **compiler**.
5. Test your ROM with **emulator**.
6. Or run all in one with **snes-ide**.

## Tutorials and Documentation

- **C Language Tutorials:**
  - [Giraffe Academy C Tutorial](https://youtu.be/KJgsSFOSQv0)
  - [C in 10 Minutes](https://youtu.be/dTp0c41XnrQ)

- **SNES Hardware Basics:**  
  [retrovgames](https://retrovgames.com/snes-hardware-explained/)

- **Getting Started:**  
  [SNES basics](./docs/snes-basic/README.md)

- **Pvsneslib/SNES-IDE Tutorial:**  
  [Intermediary](./docs/pvsneslib/README.md)

- **Examples:**
  - [Hello World template](./tests/template/)
  - [Source examples](./docs/examples/)
  - [Example ROMs](./libs/bsnes/Roms/examples/)

> **Note:** Data files (images, sounds, etc.) must be converted using the provided tools before compiling. Remember that we will use '#include "snes.h"' in this tutorial, because it is in the same directory, and not '#include <snes.h>' like when we use '#include <stdio.h>' and other global libraries.

## How SNES-IDE Works

- Uses batch files (Windows) and shell scripts (Linux) as shortcuts to launch editors, tools, and build scripts.
- Most automation is done in Python; some tools are in C#, C, JavaScript, assembly, and Julia.
- The goal is to make pvsneslib easy to use on Windows and Linux, with minimal setup.
- All-in-one: No need for extra software to create a complete SNES game.

## Contributing

- Read [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) and [PULL_REQUEST_RULES.md](./PULL_REQUEST_RULES.md).
- Fork the repo and create a feature branch.
- Write clear, modular code with comments.
- Add or update tests as needed.
- Submit a pull request with a descriptive title and summary.
- Open issues or discussions for bugs, ideas, or questions.

## Docs

See the [complete documentation](./docs/SNES-IDE.docs.md) for more details about SNES-IDE, including advanced usage, architecture, and troubleshooting.

## License

SNES-IDE is released under the GNU GPL v3 license.  
Any game you create with this engine is entirely yours.  
Check the licenses of external libraries/tools for their terms.  
This IDE is not affiliated with, nor authorized, endorsed or licensed by Nintendo Corporation or its subsidiaries. No Nintendo-licensed or original/modified SNES ROMs are included in this repository.

## Special Thanks

Thanks to all people who made SNES-IDE possible!

- [@Alekmaul and the pvsneslib team](https://github.com/alekmaul/pvsneslib)
- [All bsnes team](https://github.com/bsnes-emu/bsnes)
- [Notepad++ team](https://github.com/notepad-plus-plus/notepad-plus-plus)
- [@angelo-wf for SnesJs](https://github.com/angelo-wf/SnesJs)
- [schismtracker team](https://github.com/schismtracker/schismtracker)
- [@nesdoug for M8TE](https://github.com/nesdoug/M8TE)
- [@AlekIII for web-wav-converter](https://github.com/AlexIII/web-wav-converter)
- [@luizomf for programming mentorship](https://github.com/luizomf)
- Family, friends, and everyone who contributed in anyway with this project!

---

If you have any questions or want to help, open an issue or discussion on GitHub!

---
