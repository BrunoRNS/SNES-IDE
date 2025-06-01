# Build Instructions

This document explains the build process and provides a way to verify if the build executed successfully.

---

## Required Dependencies for building from source

- **.NET Framework 8.0 or newer (newer versions not guaranteed):**  
  Required for compiling C# projects with .NET libraries.  
  If you are using Windows, install it from the [official website](<!-- TO IMPLEMENT -->).

- **Python 3.8 or newer:**  
  Required for running Python scripts and tooling.  
  Download and install from the [official Python website](https://www.python.org/downloads/).

- **Linux:**  
  For Linux support, install the following dependencies:
  - .NET SDK 8.0:  
    Run `sudo apt install dotnet-sdk-8.0` to install the complete .NET SDK. You do not need the Windows installer for this.
  - Wine 9.0 or newer:  
    Install and configure Wine. Older versions may work, but are not guaranteed.
  - Windows Python:  
    Download and install the **Windows** version of Python using Wine from the [official Python website](https://www.python.org/downloads/).

  > After installing these dependencies, follow the specific instructions in the [Linux build guide](../linux/README.md).

## Build Process Overview in _Windows_

To build this project in **windows** from source, you follow these steps:

1. **Install Dependencies:**  
  Ensure all required tools and libraries are installed on your system.

2. **Build the Project:**  
  Run the [build.bat](./build.bat) to compile the source code:
  
  ```bat
  cd C:\\path\\to\\SNES-IDE\\
  cmd /c build\\build.bat
  ```

---
