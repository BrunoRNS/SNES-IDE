from pathlib import Path
from array import array
import subprocess
import sys

class SnesIde(object):

    def __init__(self, *args: object, **kwargs: object) -> None:
        """
        Initializes the class instance.

        - Sets the executable path.
        - Initializes the options array with values 0 through 6.
        - Prompts the user to select an option.
        - Executes a batch file based on the selected option and exits the program.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        self.path: Path = Path.home() / "Desktop" / "snes-ide"

        self.options: array = array("B", (0, 1, 2, 3, 4, 5, 6))

        option = self.give_options()

        sys.exit(self.execute_bat(option))


    @staticmethod
    def run(file: Path):
        """
        Executes the specified file using the Windows command prompt.

        Args:
            file (Path): The path to the file to be executed.

        Raises:
            subprocess.CalledProcessError: If the command returns a non-zero exit status.
        """

        subprocess.run(["cmd", "/c", str(file)], check=True)


    def execute_bat(self, option: int) -> int:
        """
        Executes a batch file corresponding to the given option.

        Parameters:
            option (int): An integer representing the batch file to execute.
                0 - create-new-project.bat
                1 - text-editor.bat
                2 - audio-tools.bat
                3 - graphic-tools.bat
                4 - other-tools.bat
                5 - compiler.bat
                6 - emulator.bat

        Returns:
            int: 0 if the batch file executed successfully, -1 if an error occurred.

        Raises:
            subprocess.CalledProcessError: If the batch file execution fails.
        """

        match option:

            case 0:   self.run(self.path / "create-new-project.bat"); return 0

            case 1:   self.run(self.path / "text-editor.bat"); return 0

            case 2:   self.run(self.path / "audio-tools.bat"); return 0

            case 3:   self.run(self.path / "graphic-tools.bat"); return 0

            case 4:   self.run(self.path / "other-tools.bat"); return 0

            case 5:   self.run(self.path / "compiler.bat"); return 0

            case 6:   self.run(self.path / "emulator.bat"); return 0

            case _:   return -1
    

    def give_options(self) -> int:
        """
        Presents a menu of SNES project-related options to the user and prompts for a selection.
        The available options include:

            0 - Create a new SNES project
            1 - Start Notepad++ text editor
            2 - Start an audio framework for SNES
            3 - Start a graphic framework for SNES
            4 - Run an external framework for SNES
            5 - Compile a SNES project
            6 - Emulate a SNES project with bsnes

        The method prints the options, reads user input, validates it against self.options,
        and recursively prompts again if the input is invalid.

        Returns:
            int: The selected option as an integer.

        """

        txt: str = "\
Create a new Snes project -> 0\n \
Start notepad++ text editor -> 1\n \
Start an audio framework for snes -> 2\n \
Start a graphic framework for snes -> 3\n \
Run an external framework for snes -> 4\n \
Compile a Snes project -> 5\n \
Emulate a Snes project with bsnes -> 6\n "

        print("Choose an option from the ones below: ", txt, sep="\n\n")

        option = int(input())

        if option not in self.options:

            print("\nINVALID ENTRY: try again\n")

            return self.give_options()

        return option



    @staticmethod
    def get_executable_path() -> Path:
        """
        Returns the directory path where the current executable or script is located.
        If the application is running as a PyInstaller bundle (frozen), it returns the directory containing the executable.
        Otherwise, it returns the directory containing the current Python script file.
        Returns:
            Path: The directory path of the executable or script.
        """

        if getattr(sys, 'frozen', False):
            # PyInstaller executable
            print("Executable path mode chosen")

            return Path(sys.executable).parent
    
        else:
            # Normal script
            print("Python script path mode chosen")

            return Path(__file__).absolute().parent


if __name__ == "__main__":

    SnesIde()
