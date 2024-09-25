# SNES-IDE: Your Creative Journey into Game Development
## What Is SNES-IDE?

SNES-IDE is an open-source and freeware Integrated Development Environment (IDE) designed specifically for creating SNES games on Windows systems using pvsneslib. Here’s what you need to know:

- Languages: It uses [C](https://en.wikipedia.org/wiki/C_(programming_language)) and a touch of assembly(65816 and spc700) code for development.
- Compilers: The [816-tcc](https://github.com/alekmaul/tcc) and [wla-dx](https://github.com/vhelin/wla-dx) compilers from [pvsneslib](https://github.com/alekmaul/pvsneslib) are your tools.
- Main Library: SNES-IDE relies on [pvsneslib](https://github.com/alekmaul/pvsneslib) v4.3 (with some tweaks for better Windows compatibility).
- Learn with Examples: Dive into the complete tutorial and explore numerous game samples.
- Emulator Choice: For testing, I recommend the freeware and open-source [snes9x](https://github.com/snes9xgit/snes9x) emulator.
- Ready to embark on your game development adventure?

## Why Choose SNES?
Developing games for the SNES is a blast! Here’s why:

- Cross-Platform Magic: SNES games can run on various platforms, from classic consoles to modern devices.
- Pure Fun: The SNES is iconic, and creating games for it is a joyous experience.
- Learn and Create: Knowing the basic of C programming, SNES-IDE and the tutorials empower you to create anything you imagine.

## Installation Requirements

To get started with SNES-IDE:

Operating System: Windows (tested on Windows 10 and higher). [How can I see my Windows version](https://support.microsoft.com/en-us/windows/which-version-of-windows-operating-system-am-i-running-628bec99-476a-2c13-5296-9dd081cdd808)

Architecture: x64, x86_64, or amd64 (not compatible with ARM systems).[How can I see if I my PC have this CPU?](https://www.tenforums.com/tutorials/176966-how-check-if-processor-32-bit-64-bit-arm-windows-10-a.html)

Minimum Resources: At least 2 GB RAM and 200 MB free disk space. - Probably your pc will have

Curiosity and Time: Set aside time to read the documentation and explore!


## Getting started

1. Download the ZIP file from our GitHub repository.
2. Unzip the contents to a folder of your choice.
3. Double-click the "INSTALL" file to set up SNES-IDE.

This will generate this shortcuts:

- "text-editor" - [Notepad++](https://github.com/notepad-plus-plus/notepad-plus-plus) for editing your code
- "audio-tools" - Create your sound
- "graphic-tools" - Create your graphic
- "export-rom" - Export your game(after compiling it in ROM format) to various platforms
- "other-tools" - Other good online tools
- "create-new-project" - For creating a new project by hello world template
- "compiler" - Compile your project into a SNES ROM 

## How can I use it?

Having your SNES-IDE already installed, you can create your games. First of all read the tutorial for you understand how you create your first game 

## Tutorials and Documentation

Before getting started:
First, you need to know that SNES-IDE uses the C language (assembly is possible and highly recommended for some speed aspects). It's highly recommended to be familiar with C programming before trying to develop with SNES-IDE. Learning C language at same time as learning Super Nintendo programming is definitely too difficult and you will end up getting nowhere.

C language tutorials:
- [Complete Giraffe academy's tutorial with code:blocks](https://youtu.be/KJgsSFOSQv0)
- [C tutorial in 10 minutes](https://youtu.be/dTp0c41XnrQ)

Remember that we will use '#include "snes.h"' in this tutorial, because it is in the same directory, and not '#include \<snes.h\>' like when we use '#include \<stdio.h\>' and other global libraries.

Snes Hardware basic:
- [retrovgames](https://retrovgames.com/snes-hardware-explained/)

Getting started
- [SNES basics](docs/snes-basic/README.md)

Pvsneslib/SNES-IDE tutorial
- [Intermediary](docs/pvsneslib/README.md)

Examples
- [Hello World template](https://github.com/BrunoRNS/SNES-IDE/tree/main/template)
- [Source examples](https://github.com/BrunoRNS/SNES-IDE/tree/main/docs/examples)
- - Atention! Source examples' data files(images, sounds, musics and etc..) must be converted using audio-tools, gfx-tools, etc.. See the tutorial of how to compile or see in pvsneslib docs the makefile showing the paramters of converting.
- [Example's ROMs](https://github.com/BrunoRNS/SNES-IDE/tree/main/snes9x-1.62.3/Roms)

## Need help?

Contact me by github begining a discussion or sharing an issue.

## How SNES-IDE works?

We have 6 batch files that works like .lnk files redirecting you to the original executable. Some executables call other ones, and another ones. Bigger part made with python, a smaller part made with c#, c, javascript, assembly, and a smaller one made with julia language.

The ideia is to simplify the installation and the use of pvsneslib in windows systems, we don't need more linux terminals and software(like make) in windows! We are independent now!

We use a lot of freeware softwares for a complete IDE, you won't need a lot of another softwares for creating a simple game for SNES anymore.

Any question of how does SNES-IDE works, see the source code, or begin a github discussion.

## How can I countribute?

First of all read CODE_OF_CONDUCT.txt

- Sending a pull request(see PULL_REQUEST_RULES.txt).
- Sharing an issue.
- begining a good discussion.

This repostitory is public and freeware, and I am open to anyone who want to upgrade this IDE

## Licence

SNES-IDE is released under the GNU GPL v3 license. This means that if you fork or use this repository, you must adhere to the terms outlined in the LICENSE.txt file. However, any game you create using this engine is entirely yours, and you're free to use it for any purpose.

Relating to extern libraries and tools you have to check their respective licences to make stuffs with them. If you have questions about licences, begin a discussion about it for I can help you.

This IDE is not affliated with, nor authorized, endorsed or licensed in any way by Nintendo Corporation, its affliates or subsidiaries. No Nintendo licenced and original or modified SNES ROMs are included in this repository!

## Special Thanks

Thanks a lot for this projects that help me creating this repostitory!

- [@Alekmaul and all pvsneslib team for pvsneslib](https://github.com/alekmaul/pvsneslib)
- [All Notepad++ team for notepad++](https://github.com/notepad-plus-plus/notepad-plus-plus)
- [snes9x team for snes9x](https://github.com/snes9xgit/snes9x)
- [@angelo-wf for the javascript snes emulator](https://github.com/angelo-wf/SnesJs)
- [schismtracker team for schismtracker](https://github.com/schismtracker/schismtracker)
- [@nesdoug for M8TE](https://github.com/nesdoug/M8TE)
- [@AlekIII for web-wav-converter](https://github.com/AlexIII/web-wav-converter)
- [@luizomf that teached me programming](https://github.com/luizomf)
- **Aka Hiryu** for snes9x port for ps2
- [@nesbox team for nesbox](https://nesbox.com)
- Family and friends!

And everbody that help me anyway in this SNES-IDE!
