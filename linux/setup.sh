#!/bin/bash

set -e

ICON_PATH="../icons/icon.ico"
START_SH="start.sh"

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
SRC_DIR="$SCRIPT_DIR/src"

cd $SCRIPT_DIR

if [[ "$EUID" -eq 0 ]]; then

    echo "Error: DO NOT run this script as root or with sudo."
    exit -1

fi

# Give chmod +x to all files in src dir
for file in "$SRC_DIR"/*; do

    if [[ -f "$file" ]]; then

        chmod +x "$file"

    fi
    
done

# Check if already installed (simple check: presence of a .installed file)
if [[ -f ".installed" ]]; then

    read -p "Installation detected. Do you want to create a desktop shortcut for $START_SH? (y/n): " create_shortcut

    if [[ "$create_shortcut" =~ ^[Yy]$ ]]; then

        DESKTOP_FILE="$HOME/Desktop/SNES-IDE.desktop"
        SYSTEM_DESKTOP_FILE="/usr/share/applications/SNES-IDE.desktop"

        cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=SNES-IDE
Exec=$(realpath "$SRC_DIR/$START_SH")
Icon=$(realpath "$ICON_PATH")
Terminal=true
EOF

        echo "Shortcut created at $DESKTOP_FILE"

        # Copy to system applications directory (Debian/Ubuntu)

        echo "Write your password to copy to applications: "

        if sudo cp "$DESKTOP_FILE" "$SYSTEM_DESKTOP_FILE"; then

            echo "Write your password to give your DESKTOP FILE permissions 644: "
            sudo chmod 644 "$SYSTEM_DESKTOP_FILE"
            echo "Shortcut also installed system-wide at $SYSTEM_DESKTOP_FILE"

        else

            echo "Could not move shortcut to $SYSTEM_DESKTOP_FILE. You may need to run as root."

        fi

    fi

    exit 0

fi

bash "$SRC_DIR/build"

# Ask user if they want to execute start.sh
if [[ -f "$SRC_DIR/$START_SH" ]]; then

    read -p "Do you want to start snes-ide now? (y/n): " exec_start

    if [[ "$exec_start" =~ ^[Yy]$ ]]; then

        bash "$SRC_DIR/$START_SH"

    fi

fi
