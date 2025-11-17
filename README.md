# SNES-IDE: Your Journey into Snes Game Development

---

<img src="icon.png" alt="SNES-IDE Icon" style="width: 128px; height: 128px; display: block; margin: 0 auto; align-self: center; border-radius: 50%; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); cursor: pointer; transition: transform 0.3s ease;">

---

## What Is SNES-IDE?

SNES-IDE is an open-source, cross-platform Integrated Development Environment (IDE) designed for creating SNES games using [pvsneslib](https://github.com/alekmaul/pvsneslib).  
It works natively on Windows, Linux Ubuntu and macOS, and provides tools, templates, and automation for building, compiling, and testing SNES ROMs.

- **Languages:** C, C#, Assembly and Java.
- **Compilers:** [816-tcc](https://github.com/alekmaul/tcc) and [wla-dx](https://github.com/vhelin/wla-dx) from pvsneslib. [Dntc](https://github.com/KallDrexx/dntc) from DotnetSnes. [JavaSnes](https://github.com/BrunoRNS/javasnes) from javasnes.
- **Main Library:** [pvsneslib](https://github.com/alekmaul/pvsneslib) version 4.4. [DotnetSnes](https://github.com/KallDrexx/DotnetSnes) version 0.2. [Javasnes](https://github.com/BrunoRNS/javasnes) rolling release.
- **Emulator:** [bsnes](https://github.com/bsnes-emu/bsnes) and [lakesnes](https://github.com/angelo-wf/lakesnes) for testing.
- **Cross-platform:** Works natively on Windows, Linux Ubuntu and macOS.
- **Build from Source:** Full support for building all tools and the IDE itself from source.

## Why Choose SNES-IDE?

- **Cross-Platform:** Develop on Windows, macOS or Linux.
- **All-in-One:** Integrated toolchain, asset converters, and project templates.
- **Easy Start:** One-click project creation and build scripts.
- **Open Source:** Free, extensible, and community-driven.
- **Learn & Create:** Ideal for learning C and SNES hardware, with lots of examples and documentation.

## Getting Started

First, check the system requirements:

- **Operational System**
  - Windows 10+ x64.
  - MacOS BigSur+ arm64.
  - Linux Ubuntu Noble 24.04+ (or based) x64.
- **Free Disk Space**
  - Minimum: 960 MiB
  - Recommended: 5 GiB
- **Memory**
  - Minimum: 1 GiB
  - Recommended: 4 GiB

Download the latest release from [SNES-IDE releases](https://github.com/BrunoRNS/SNES-IDE/releases/latest) for your specific OS.

### Windows

- Download the Windows version from [SNES-IDE releases](https://github.com/BrunoRNS/SNES-IDE/releases/latest).
- The Windows version is distributed as a zip file, which you can extract and run the `SNES-IDE.exe` file to start.

### Linux

- Download the Linux version from [SNES-IDE releases](https://github.com/BrunoRNS/SNES-IDE/releases/latest).
- The Linux version is distributed as an AppImage, which you can run directly from the downloaded file.

### macOS

- Download the macOS version from [SNES-IDE releases](https://github.com/BrunoRNS/SNES-IDE/releases/latest).
- The macOS version is distributed as a zip file, which you can extract and run the `SNES-IDE.app` executable to start.

## Tutorials and Documentation

- **C Language Tutorials:**
  - [Giraffe Academy C Tutorial](https://youtu.be/KJgsSFOSQv0)
  - [C in 10 Minutes](https://youtu.be/dTp0c41XnrQ)

- **SNES Hardware Basics:**  
  - [retrovgames](https://retrovgames.com/snes-hardware-explained/)

- **Examples:**
  - [Source examples](./docs/examples/)

## Contributing

- Read [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) and [CONTRIBUTING.md](./CONTRIBUTING.md).
- Fork the repo and create a feature branch.
- Write clear, modular code with comments.
- Add or update tests as needed.
- Submit a pull request with a descriptive title and summary.
- Open issues or discussions for bugs, ideas, or questions.

## License

SNES-IDE is released under the GNU GPL v3 license.
Any game you create with this engine is entirely yours.
Check the licenses of external libraries/tools for their terms.  
This IDE is not affiliated with, nor authorized, endorsed or licensed by Nintendo Corporation or its subsidiaries. No Nintendo-licensed or original/modified SNES ROMs are included in this repository.

## Special Thanks

Thanks to all people who made SNES-IDE possible!

- [@LucianoCSiqueira for the help in javasnes and keeping me motivated to continue updating SNES-IDE](https://github.com/LucianoCSiqueira)
- [@Atomic-germ for the build refactor, automatized tests and build workflows](https://github.com/Atomic-Germ)
- [@alekmaul for pvsneslib](https://github.com/alekmaul/pvsneslib)
- [@KallDrexx for DotnetSnes](https://github.com/KallDrexx/DotnetSnes)
- [@angelo-wf for lakesnes](https://github.com/angelo-wf/lakesnes)
- [Bsnes team for bsnes emulator](https://github.com/bsnes-emu/bsnes)
- [Schismtracker team for the schism tracker](https://github.com/schismtracker/schismtracker)
- [Libresprite team for the sprite editor](https://libresprite.github.io/#!/)
- [Tiled for the map engine and tmx editor](http://www.mapeditor.org/)
- [Zulu-8 for the support for OpenJDK8, JFX and JRE-8 (javasnes dependencies)](https://www.azul.com/downloads/?version=java-8-lts&package=jdk-fx&show-old-builds=true#zul)
- And everyone who contributed in anyway with this project!

---

> If you have any questions or want to help, open an issue or discussion on GitHub!

---
