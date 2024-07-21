# Initial text
println("Write down the name of your new prject:\n")

# Project name
project_name = readline()

# Second text
println("Write down the Full path of the folder you want to create a project: \n(C:\\\\ in windows, begin with / in Linux or MacOs)\n")

path = readline()
# Check if the specified path exists
if isdir(path)
    # Validate the project name (alphanumeric, underscores, and hyphens)
    if match(r"^[A-Za-z0-9_-]+$", project_name) !== nothing
        # Construct the target directory path
        target_path = joinpath(path, project_name)

        # Copy the template folder to the specified path
        cp(joinpath(Base.source_dir(), "..", "template"), target_path)

        println("Project created successfully! Press any key to exit...")
        readline()  # Wait for user interaction to exit
    else
        println("Invalid project name. Please use alphanumeric characters, underscores, or hyphens. Press any key to exit...")
        readline()
    end
else
    println("The specified path does not exist. Press any key to exit...")
    readline()
end

