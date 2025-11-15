#include <windows.h>
#include <string>
#include <cstdlib>
#include <shellapi.h>

/**
 * Checks if a file exists at the given path.
 *
 * @param path The path to check for file existence.
 * @return true if the file exists, false otherwise.
 */
bool FileExists(const std::string &path)
{

    DWORD attrib = GetFileAttributesA(path.c_str());

    return (attrib != INVALID_FILE_ATTRIBUTES && !(attrib & FILE_ATTRIBUTE_DIRECTORY));
}

/**
 * Retrieves the directory of the current executable.
 *
 * @return The directory of the current executable as a string, or an empty string if the executable path cannot be determined.
 */
std::string GetExecutableDirectory()
{

    char exePath[MAX_PATH];

    if (GetModuleFileNameA(NULL, exePath, MAX_PATH) == 0)
    {

        return "";
    }

    std::string exeDir(exePath);
    size_t lastSlash = exeDir.find_last_of("\\");

    if (lastSlash != std::string::npos)
    {

        return exeDir.substr(0, lastSlash);
    }

    return "";
}

/**
 * Displays an error message box with the given message and returns -1.
 *
 * @param message The error message to display.
 * @return -1 to indicate an error.
 */
int ShowError(const std::string &message)
{

    MessageBoxA(NULL, message.c_str(), "SNES IDE - Error", MB_ICONERROR | MB_OK);

    return -1;
}

/**
 * The main entry point of the program.
 *
 * This function determines the executable directory and attempts to launch the
 * SNES IDE Python script using the virtual environment Python executable.
 *
 * If any errors occur during the startup process, an error message box will be
 * displayed with a descriptive error message.
 *
 * @return The exit code of the launched process, or -1 if an error occurred.
 */
int main()
{

    std::string exeDir = GetExecutableDirectory();

    if (exeDir.empty())
    {

        return ShowError("Cannot determine executable directory");
    }

    std::string venvPython = exeDir + "\\venv\\Scripts\\python.exe";
    std::string scriptPath = exeDir + "\\src\\snes-ide.py";

    if (!FileExists(venvPython))
    {

        return ShowError("Python virtual environment not found: " + venvPython);
    }

    if (!FileExists(scriptPath))
    {

        return ShowError("Main script not found: " + scriptPath);
    }

    std::string command = "\"" + venvPython + "\" \"" + scriptPath + "\"";

    SetEnvironmentVariableA("QT_QUICK_BACKEND", "software");
    SetEnvironmentVariableA("QMLSCENE_DEVICE", "softwarecontext");
    SetEnvironmentVariableA("QT_QPA_PLATFORM", "windows");
    SetEnvironmentVariableA("LIBGL_ALWAYS_SOFTWARE", "1");

    STARTUPINFOA si = {sizeof(si)};
    PROCESS_INFORMATION pi;

    if (CreateProcessA(NULL, (LPSTR)command.c_str(), NULL, NULL, FALSE,
                       CREATE_NO_WINDOW, NULL, NULL, &si, &pi))
    {
        WaitForSingleObject(pi.hProcess, INFINITE);

        DWORD exitCode;
        GetExitCodeProcess(pi.hProcess, &exitCode);

        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);

        return exitCode;
    }
    else
    {

        return ShowError(
            "Failed to start SNES IDE. Error code: " + std::to_string(GetLastError()));
    }
    
}
