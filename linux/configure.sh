#!/bin/bash
set -e

if [[ "$EUID" -eq 0 ]]; then

    echo "Error: DO NOT run this script as root or with sudo."
    exit -1

fi

# Detect correct home directory even if running with sudo
if [ "$SUDO_USER" ]; then

    USER_HOME=$(eval echo "~$SUDO_USER")

else

    USER_HOME="$HOME"
    
fi

export WINEPREFIX="$USER_HOME/.wine-snes-ide"
WINE_TARGET_DIR="$USER_HOME/.wine-snes-ide/drive_c/SNES-IDE"

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PROJECT_ROOT="$(realpath "$SCRIPT_DIR/../..")"
OUT_DIR="$PROJECT_ROOT/SNES-IDE-out"

cd "$SCRIPT_DIR"

echo "Copying pre-built files from $OUT_DIR to $WINE_TARGET_DIR..."

echo "Write down the password to allow cleaning the previous configuration: "

sudo rm -rf "$WINE_TARGET_DIR"

mkdir -p "$WINE_TARGET_DIR"

shopt -s dotglob
cp -r "$OUT_DIR"/* "$WINE_TARGET_DIR"
shopt -u dotglob

cd "$WINE_TARGET_DIR"

if [ -f "./SNES-IDE-out/INSTALL.bat" ]; then

    echo "Running ./SNES-IDE-out/INSTALL.bat with Wine..."
    wine cmd /c "./SNES-IDE-out/INSTALL.bat"

else

    echo "Error: INSTALL.bat not found in $WINE_TARGET_DIR"
    exit 1

fi

cd "$SCRIPT_DIR"

read -p "Do you want to create a desktop shortcut for start.sh? (y/n): " create_shortcut
if [[ "$create_shortcut" =~ ^[Yy]$ ]]; then

    ICON_PATH="../icons/icon.ico"
    START_SH="start.sh"
    DESKTOP_FILE="$USER_HOME/Desktop/SNES-IDE.desktop"
    SYSTEM_DESKTOP_FILE="/usr/share/applications/SNES-IDE.desktop"

    cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=SNES-IDE
Exec=$(realpath "$SCRIPT_DIR/src/$START_SH")
Icon=$(realpath "$ICON_PATH")
Terminal=true
EOF

    echo "Shortcut created at $DESKTOP_FILE"

    echo "Write your password to copy to applications: "
    if sudo cp "$DESKTOP_FILE" "$SYSTEM_DESKTOP_FILE"; then

        sudo chmod 644 "$SYSTEM_DESKTOP_FILE"
        echo "Shortcut also installed system-wide at $SYSTEM_DESKTOP_FILE"

    else

        echo "Could not move shortcut to $SYSTEM_DESKTOP_FILE. You may need to run as root."

    fi

fi

read -p "Do you want to start SNES-IDE now? (y/n): " exec_start
if [[ "$exec_start" =~ ^[Yy]$ ]]; then

    bash "$SCRIPT_DIR/src/start.sh"

fi