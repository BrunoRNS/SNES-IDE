from pathlib import Path
import subprocess

class shutil:
    """Reimplementation of class shutil to avoid errors in Wine"""

    @staticmethod
    def copy(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method copy using copy command"""

        subprocess.run(f'copy "{src}" "{dst}"', shell=True, check=True)

    @staticmethod
    def copytree(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method copytree using xcopy"""

        cmd = f'xcopy "{src}" "{dst}" /E /I /Y /Q /H'
        subprocess.run(cmd, shell=True, check=True)

    @staticmethod
    def rmtree(path: str|Path) -> None:
        """Reimplementation of method rmtree using rmdir"""

        subprocess.run(f'rmdir /S /Q "{path}"', shell=True, check=True)

    @staticmethod
    def move(src: str|Path, dst: str|Path) -> None:
        """Reimplementation of method move using move command"""

        subprocess.run(f'move "{src}" "{dst}"', shell=True, check=True)

def main(cs_path: Path | str, exe_path: Path | str) -> int:
    """
    Builds and publishes a C# project using the .NET CLI.

    This function expects two arguments:
        1. The path to a C# source file (.cs).
        2. The desired output executable path.

    The function performs the following steps:
        - Validates the number of arguments and prints usage information if insufficient.
        - Determines the absolute paths for the input C# file and output executable.
        - Searches for a .csproj file in the same directory as the C# file.
        - Runs 'dotnet restore' to restore NuGet packages for the project.
        - Ensures the output directory exists.
        - Builds and publishes the project using .NET 8.0 for the 'win-x64' runtime, as a self-contained, single-file executable.
        - Copies the published output files to the specified output directory.
        - Handles errors at each step and prints appropriate error messages.

    Exits the process with a non-zero status code if any step fails.
    """

    cs_file, exe_name = map(lambda x: Path(x).absolute(), (cs_path, exe_path))

    cs_dir = cs_file.parent

    # Find the .csproj file in the same directory
    csproj_files = list(cs_dir.glob("*.csproj"))

    if not csproj_files:

        print(f"Error: No .csproj file found in {cs_dir}")
        return 1

    csproj_path = csproj_files[0]

    # dotnet restore
    result = subprocess.run(["dotnet", "restore", str(csproj_path)])

    if result.returncode != 0:

        print("Error: Failed to restore NuGet packages.")
        return 1

    out_dir = Path(exe_name).parent

    # Ensure output directory exists
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build and publish using .NET 8.0 to the default publish folder
    publish_cmd = [
        "dotnet", "publish", str(csproj_path),
        "-c", "Release",
        "-f", "net8.0",
        "-r", "win-x64",
        "--self-contained", "true",
        "/p:PublishSingleFile=true",
        "/p:PublishTrimmed=false",
    ]

    result = subprocess.run(publish_cmd)

    if result.returncode != 0:

        print("Error: Publish failed. Please check the project file and configuration.")
        return 1

    publish_dir = cs_dir / "bin" / "Release" / "net8.0" / "win-x64" / "publish"

    if not publish_dir.exists():

        print(f"Error: Published directory not found: {publish_dir}")
        return 1

    # Copy the entire published directory to the output directory
    try:

        for item in publish_dir.iterdir():

            dest = out_dir / item.name

            if item.is_dir():

                if dest.exists():

                    shutil.rmtree(dest)

                shutil.copytree(item, dest)

            else:

                shutil.copy(item, dest)

    except Exception as e:

        print(f"Error: Failed to copy published directory to {out_dir}, {e}")

        return 1

    print(f"Build completed successfully. The published files are located at: {out_dir}")

    return 0

if __name__ == "__main__":

    import sys

    sys.exit(main(sys.argv[1], sys.argv[2]))
