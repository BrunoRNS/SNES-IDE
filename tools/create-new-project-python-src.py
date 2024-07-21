import os
import re
import shutil

# Initial text
print("Write down the name of your new project:\n")

# Project name
project_name = input()

def get_executable_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller executable
        print("executable path mode chosen")
        return os.path.dirname(sys.executable)
    else:
        # Normal script
        print("Python script path mode chosen")
        return os.path.dirname(os.path.abspath(__file__))

# Second text
print("Write down the Full path of the folder you want to create a project: \n(C:\\\\ in windows, begin with / in Linux or MacOS)\n")

path = input()

# Check if the specified path exists
if os.path.isdir(path):
    # Validate the project name (alphanumeric, underscores, and hyphens)
    if re.match(r"^[A-Za-z0-9_-]+$", project_name):
        # Construct the target directory path
        target_path = os.path.join(path, project_name)

        # Copy the template folder to the specified path
        template_path = os.path.join(get_executable_path(), "..", "template")
        shutil.copytree(template_path, target_path)

        print("Project created successfully! Press any key to exit...")
        input()  # Wait for user interaction to exit
    else:
        print("Invalid project name. Please use alphanumeric characters, underscores, or hyphens. Press any key to exit...")
        input()
else:
    print("The specified path does not exist. Press any key to exit...")
    input()
