# SNES-IDE Linux Installation Guide

## **1. Requirements**

- **Wine** must be installed and configured.
- You need permission to run scripts and (optionally) to install a desktop shortcut system-wide.

- **.NET SDK for Linux**  
  Required for building and running any .NET-based components. Install it using your package manager (for example, `sudo apt install dotnet-sdk-8.0` on Debian).  
  For more details, visit the [.NET download page](https://dotnet.microsoft.com/download).

- **Configure installers**
  Go to [installers setup guide](./installers/README.md) to see more detailed information.

---

## **2. Installation Steps**

### **A. Prepare the Environment**

1. **Open a terminal** in the root of your SNES-IDE project.

2. **Make sure all scripts are executable:**

   ```bash
   chmod +x ./linux/setup.sh ./linux/src/*.sh
   ```

---

### **B. Run the Setup Script**

#### **Start the installation process:**

```bash
bash ./linux/setup.sh
```

**The script will**:

- Make all scripts in src executable.
- Check for a previous installation (`.installed` file).
- If already installed, it offers to create a desktop shortcut.
- If not installed, it runs all scripts in src except start.sh.

---

### **C. Build and Install**

- The build script:
  - Checks for Wine and initializes a dedicated Wine prefix (`~/.wine-snes-ide`).
  - Optionally runs Windows installers for dependencies (Python, Visual Studio) if present.
  - Calls install.sh.

- _Note: if you want to change to the original Wine prefix, run:_ ```export WINEPREFIX="yourOldWinePrefix"```_._

- The install.sh script:
  - Moves the SNES-IDE files into the Wine prefix.
  - Runs the Windows build script (`build.bat`) via Wine.
  - Runs the Windows installer script (INSTALL.bat) via Wine.
  - Marks the installation as complete by creating a `.installed` file.

---

### **D. Create a Desktop Shortcut (Optional)**

- If installation is detected, the setup script will ask if you want to create a desktop shortcut.
- If you agree, it creates `SNES-IDE.desktop` on your desktop and attempts to move it to applications for system-wide access.

---

### **E. Starting SNES-IDE**

- After installation, you can start SNES-IDE by running:

  ```bash
  ./linux/src/start.sh
  ```

- Or use the desktop shortcut if you created one.

---

## **3. Notes**

- The Wine prefix used is `~/.wine-snes-ide`, keeping SNES-IDE isolated from your main Wine environment.
- The main executable is expected at:  
  `~/.wine-snes-ide/drive_c/users/<your_user>/Desktop/snes-ide/snes-ide.exe`
- If you need to re-run the installation, delete the `.installed` file and run setup.sh again.

---

**If you encounter issues, check the terminal output for errors and ensure all dependencies (like Wine) are installed.**
