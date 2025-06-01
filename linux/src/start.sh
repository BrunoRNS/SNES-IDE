#!/bin/bash

set -e

if [ "$SUDO_USER" ]; then

    USER_HOME=$(eval echo "~$SUDO_USER")

else

    USER_HOME="$HOME"
    
fi

export WINEPREFIX="$USER_HOME/.wine-snes-ide"

WINE_USER="$(whoami)"

SHORTCUT="$WINEPREFIX/drive_c/users/$WINE_USER/Desktop/snes-ide/snes-ide.exe"
SHORTCUT2="$WINEPREFIX/drive_c/users/$WINE_USER/Desktop/snes-ide/snes-ide.bat"

SHORTCUTDIR="$WINEPREFIX/drive_c/users/$WINE_USER/Desktop/snes-ide/"

cd "$SHORTCUTDIR"

if [ -f "$SHORTCUT" ]; then

    echo "Starting SNES-IDE via shortcut..."
    wine cmd /c "./snes-ide.exe"

else

    if [ -f "$SHORTCUT2" ]; then

        echo "Starting SNES-IDE via shortcut..."
        wine cmd /c "./snes-ide.bat"

    else

        echo "SNES IDE not found!"
        exit 1

    fi

fi

exit 0