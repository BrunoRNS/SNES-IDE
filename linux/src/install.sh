#!/bin/bash
set -e

# Detect correct home directory even if running with sudo
if [ "$SUDO_USER" ]; then

    USER_HOME=$(eval echo "~$SUDO_USER")

else

    USER_HOME="$HOME"

fi

export WINEPREFIX="$USER_HOME/.wine-snes-ide"
WINE_TARGET_DIR="$USER_HOME/.wine-snes-ide/drive_c/SNES-IDE"

# Define important directories
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PROJECT_ROOT="$(realpath "$SCRIPT_DIR/../..")"

cd $SCRIPT_DIR

# 1. Copy project files to Wine directory (avoid nested SNES-IDE/SNES-IDE)
echo "Preparing Wine directory at $WINE_TARGET_DIR..."
echo ""
echo "Write down the password to clean previous build: "

sudo rm -rf "$WINE_TARGET_DIR"

echo "Previous build cleaned successfully!"

mkdir -p "$WINE_TARGET_DIR"

cp -r "$PROJECT_ROOT"/* "$WINE_TARGET_DIR"

# 2. Build all C# projects (.csproj) recursively using .NET 8
echo "Building all C# projects in $WINE_TARGET_DIR/src..."

find "$WINE_TARGET_DIR/src" -name "*.csproj" | while read -r csproj; do

    proj_dir="$(dirname "$csproj")"
    echo "Building $(basename "$csproj") in $proj_dir with .NET 8..."

    (cd "$proj_dir" && dotnet publish "$(basename "$csproj")" --output . -c Release -f net8.0 -r win-x64 --self-contained true /p:PublishSingleFile=true /p:PublishTrimmed=false)

done


# 3. Run Windows batch build and install scripts via Wine
cd "$WINE_TARGET_DIR"

if [ -f "./build/build.bat" ]; then

    echo "Running build.bat with Wine..."
    wine cmd /c "./build/build.bat linux"

else

    echo "Error: build.bat not found in ./build/"
    exit 1

fi

if [ -f "./SNES-IDE-out/INSTALL.bat" ]; then

    echo "Running INSTALL.bat with Wine..."
    wine cmd /c "./SNES-IDE-out/INSTALL.bat linux"

else

    echo "Error: INSTALL.bat not found in SNES-IDE-out/"
    exit 1

fi

echo "Build and installation completed successfully."


# Mark as installed
cd "$SCRIPT_DIR"
touch ../.installed
