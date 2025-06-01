from shutil import copytree
from re import match
from os import path
import sys


class ProjectCreator:

    def __init__(self):
        """Initialize the project creator with user input for project name and path."""

        print("**Welcome to the SNES-IDE project creator!**")
        print("This tool will help you create a new SNES-IDE project.")
        print("Please follow the instructions below to create your project.\n")

        print("Write down the name of your new project:\n")
        self.project_name = input()

        print("Write down the Full path of the folder you want to create a project: \n")
        self.full_path = input()

    
    @staticmethod
    def get_executable_path():
        """Get the path of the executable or script based on whether the script is frozen (PyInstaller) or not."""

        if getattr(sys, 'frozen', False):
            # PyInstaller executable
            print("executable path mode chosen")

            return str(path.dirname(sys.executable))
        
        else:
            # Normal script
            print("Python script path mode chosen")

            return str(path.dirname(path.abspath(__file__)))


    def run(self):
        """Run the project creation process."""

        # Check if the specified path exists
        if path.isdir(self.full_path):

            if match(r"^[A-Za-z0-9_-]+$", self.project_name):

                target_path = path.join(self.full_path, self.project_name)
                template_path = path.abspath(path.join(self.get_executable_path(), "..", "template"))

                copytree(template_path, target_path)

                input("Project created successfully! Press any key to exit...")

            else:

                input("Invalid project name. Please use alphanumeric characters, underscores, or hyphens. Press any key to exit...")

        else:

            input("The specified path does not exist. Press any key to exit...")


if __name__ == "__main__":

    ProjectCreator().run()
