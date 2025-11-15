from typing import Dict, Set, Optional
from pathlib import Path
import subprocess
import platform
import tempfile
import shutil
import venv
import os


class BundleCreator:

    def __init__(
        self, source_dir: str, output_dir: str = "dist",
        requirements_file: "str|None" = None,
        plist_template: "str|None" = None,
        desktop_template: "str|None" = None,
        apprun_template: "str|None" = None,
        windows_launcher_template: "str|None" = None,
    ) -> None:
        """
        Initializes the BundleCreator object with the given parameters.

        Parameters:
            source_dir (str): The path to the source directory containing the SNES-IDE 
            source code.
            output_dir (str): The path to the output directory where the bundle will be 
            created. Defaults to "dist".
            requirements_file (str|None): The path to the requirements.txt file containing 
            the list of Python packages required by the SNES-IDE bundle. Defaults to None.
            plist_template (str|None): The path to the Info.plist template file used to 
            create the SNES-IDE bundle on macOS. Defaults to None.
            desktop_template (str|None): The path to the desktop template file used to 
            create the SNES-IDE bundle on Linux. Defaults to None.
            apprun_template (str|None): The path to the AppRun template file used to 
            create the SNES-IDE bundle on Linux. Defaults to None.
            windows_launcher_template (str|None): The path to the Windows launcher 
            template file used to create the SNES-IDE bundle on Windows. Defaults to None.

        The BundleCreator object uses the given parameters to create the SNES-IDE bundle 
        for the current platform. The bundle will be created in the output directory and 
        will contain the required Python packages and platform-specific files.

        """

        self.source_dir: Path = Path(source_dir)
        self.output_dir: Path = Path(output_dir)
        self.current_platform: str = platform.system().lower()

        self.requirements_file: "Path|None" = Path(
            requirements_file) if requirements_file else None
        self.plist_template: "Path|None" = Path(
            plist_template) if plist_template else None
        self.desktop_template: "Path|None" = Path(
            desktop_template) if desktop_template else None
        self.apprun_template: "Path|None" = Path(
            apprun_template) if apprun_template else None
        self.windows_launcher_template: "Path|None" = Path(
            windows_launcher_template) if windows_launcher_template else None

        self.platform_config: Dict[str, Dict[str, str]] = {
            'windows': {
                'venv_name': 'venv',
                'launcher_name': 'SNES-IDE.exe',
                'cpp_source': 'SNES-IDE.cpp',
                'src_dir': 'src'
            },
            'darwin': {
                'app_name': 'SNES-IDE.app',
                'venv_dir': 'Contents/Resources/venv',
                'src_dir': 'Contents/Resources/src',
                'macos_dir': 'Contents/MacOS',
                'launcher_name': 'SNES-IDE'
            },
            'linux': {
                'appimage_name': 'SNES-IDE.AppImage',
                'venv_dir': 'usr/venv',
                'src_dir': 'usr/src',
                'launcher_name': 'AppRun'
            }
        }

    def create_bundle(self) -> bool:
        """
        Creates a bundle for the SNES-IDE application based on the current platform.

        The bundle is created in the output directory specified during initialization and
        will contain the required Python packages and platform-specific files.

        Returns:
            bool: True if the bundle is created successfully, False otherwise.
        """

        print(f"Creating bundle for {self.current_platform}...")

        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

        self.output_dir.mkdir(parents=True)

        try:
            if self.current_platform == "windows":
                success = self._create_windows_bundle()

            elif self.current_platform == "darwin":
                success = self._create_macos_bundle()

            elif self.current_platform == "linux":
                success = self._create_linux_bundle()

            else:
                raise NotImplementedError(
                    f"Platform not supported: {self.current_platform}")

            if success:
                print(f"Bundle created successfully: {self.output_dir}")

            return success

        except Exception as error:

            print(f"Error creating bundle: {error}")
            return False

    def _copy_project_files(self, target_dir: str) -> None:
        """
        Copies the project files from the source directory to the target directory.

        Args:
            target_dir (str): The path to the target directory where the project 
            files will be copied.
        """

        print("Copying project files...")

        target_dir_path: Path = Path(target_dir)

        target_dir_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copytree(self.source_dir, target_dir)

    def _create_venv(self, venv_path: Path) -> None:
        """
        Creates a virtual environment at the given path and installs the dependencies 
        from the requirements.txt file.

        If the requirements file is not provided, PySide6 is installed as a fallback.

        Args:
            venv_path (Path): The path to the directory where the virtual environment 
            will be created.
        """

        print("Creating virtual environment...")

        venv.create(venv_path, with_pip=True)

        if self.current_platform == "windows":
            pip_executable = venv_path / "Scripts" / "pip.exe"
        else:
            pip_executable = venv_path / "bin" / "pip"

        if self.requirements_file and self.requirements_file.exists():
            print("Installing dependencies from requirements.txt...")
            subprocess.run([str(pip_executable), "install", "-r", str(self.requirements_file)],
                           check=True, capture_output=True)
        else:
            print("Installing PySide6...")
            subprocess.run([str(pip_executable), "install", "pyside6"],
                           check=True, capture_output=True)

    def _create_windows_bundle(self) -> bool:
        """
        Creates the Windows bundle by creating the directory structure, virtual environment, 
        copying project files, creating and compiling the C++ launcher, and cleaning up the 
        C++ source file.

        Returns:
            bool: True if the bundle is created successfully, False otherwise.
        """

        config = self.platform_config['windows']

        venv_path = self.output_dir / config['venv_name']
        src_path = self.output_dir / config['src_dir']

        self._create_venv(venv_path)

        self._copy_project_files(str(src_path))

        cpp_path = self._create_windows_launcher()
        exe_path = self._compile_windows_launcher(cpp_path)

        if exe_path.exists() and cpp_path.exists():
            cpp_path.unlink()
            print("Cleaned up C++ source file")

        return exe_path.exists()

    def _create_windows_launcher(self) -> Path:
        """
        Creates the Windows launcher by copying the template C++ source file to the
        output directory.

        Returns:
            Path: The path to the C++ source file.
        Raises:
            FileNotFoundError: If the Windows launcher template is not found.
        """

        if not self.windows_launcher_template or not self.windows_launcher_template.exists():

            raise FileNotFoundError("Windows launcher template not found")

        cpp_path = self.output_dir / \
            self.platform_config['windows']['cpp_source']
        shutil.copy2(self.windows_launcher_template, cpp_path)

        return cpp_path

    def _compile_windows_launcher(self, cpp_path: Path) -> Path:
        """
        Compile the Windows launcher by using either g++ or cl compiler.

        Parameters:
            cpp_path (Path): The path to the C++ source file

        Returns:
            Path: The path to the compiled executable if successful, otherwise the 
            path to the source file
        """

        config = self.platform_config['windows']
        exe_path = self.output_dir / config['launcher_name']

        print("Compiling Windows launcher...")

        compilers = [
            [
                'g++', '-std=c++17', '-O2', '-s', '-static', '-mwindows', '-o',
                str(exe_path), str(cpp_path)
            ],
            [
                'g++', '-std=c++17', '-O2', '-s', '-mwindows', '-o',
                str(exe_path), str(cpp_path)
            ],
            ['cl', '/O2', '/Fe:' + str(exe_path), str(cpp_path)]
        ]

        for compiler_args in compilers:

            try:
                result = subprocess.run(
                    compiler_args, check=True, capture_output=True, text=True, timeout=60
                )

                if result.returncode == 0 and exe_path.exists():
                    print("Launcher compiled successfully")
                    return exe_path

            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Failed to compile launcher with: ",
                      " ".join(compiler_args))
                continue

        print("Warning: Could not compile C++ launcher")
        print("Install MinGW or MSVC for automatic compilation")

        return exe_path

    def _create_macos_bundle(self) -> bool:
        """
        Creates the macOS bundle by creating the directory structure, virtual environment, 
        copying project files, copying the macOS launcher, copying the Info.plist file, 
        and setting executable permissions for the bundle.

        Returns:
            bool: True if the bundle is created successfully, False otherwise.
        """

        config = self.platform_config['darwin']

        app_path = self.output_dir / config['app_name']
        contents_path = app_path / "Contents"
        macos_path = contents_path / "MacOS"
        resources_path = contents_path / "Resources"
        venv_path = contents_path / "Resources" / "venv"
        src_path = contents_path / "Resources" / "src"

        macos_path.mkdir(parents=True)
        resources_path.mkdir(parents=True)

        self._create_venv(venv_path)

        self._copy_project_files(str(src_path))

        self._copy_macos_launcher(macos_path / config['launcher_name'])
        self._copy_macos_info_plist(contents_path / "Info.plist")

        self._set_executable_permissions(app_path)

        return app_path.exists()

    def _copy_macos_launcher(self, launcher_path: Path) -> None:
        """
        Copies the macOS AppRun template to the given path.

        Parameters:
            launcher_path (Path): The path to copy the AppRun template to.

        Raises:
            FileNotFoundError: If the AppRun template is not found.
        """

        if not self.apprun_template or not self.apprun_template.exists():

            raise FileNotFoundError("AppRun template not found")

        shutil.copy2(self.apprun_template, launcher_path)
        launcher_path.chmod(0o755)

    def _copy_macos_info_plist(self, plist_path: Path) -> None:
        """
        Copies the macOS Info.plist template to the given path.

        Parameters:
            plist_path (Path): The path to copy the Info.plist template to.

        Raises:
            FileNotFoundError: If the Info.plist template is not found.
        """

        if not self.plist_template or not self.plist_template.exists():

            raise FileNotFoundError("Info.plist template not found")

        shutil.copy2(self.plist_template, plist_path)

    def _set_executable_permissions(self, app_path: Path) -> None:
        """
        Sets the executable permissions for the given application path.

        Parameters:
            app_path (Path): The path to the application directory.
        """

        for root, _, files in os.walk(app_path):

            for file in files:

                file_path = Path(root) / file

                options: Set[str] = {
                    '.sh', '.command', '.py', '.so', '.dylib', '.AppImage', '.lib', '.html',
                    '.css', '.js'
                }

                if "MacOS" in str(file_path):
                    file_path.chmod(0o755)

                elif any(suffix in file_path.suffixes for suffix in options):

                    file_path.chmod(0o755)

    def _create_linux_bundle(self) -> bool:
        """
        Creates the Linux bundle by creating the directory structure, virtual environment, 
        copying project files, copying the AppRun and desktop files, setting executable 
        permissions for the bundle, and creating the AppImage.

        Returns:
            bool: True if the AppImage is created successfully, False otherwise.
        """

        config = self.platform_config['linux']

        with tempfile.TemporaryDirectory(prefix="snes_ide_build_") as temp_dir:
            temp_path = Path(temp_dir)
            appdir_path = temp_path / "AppDir"

            usr_bin_path = appdir_path / "usr" / "bin"
            venv_path = appdir_path / config['venv_dir']
            src_path = appdir_path / config['src_dir']

            usr_bin_path.mkdir(parents=True)

            self._create_venv(venv_path)

            self._copy_project_files(str(src_path))

            self._copy_linux_apprun(appdir_path / "AppRun")
            self._copy_linux_desktop(appdir_path / "snes-ide.desktop")

            self._set_linux_permissions(appdir_path)

            appimage_path = self._create_appimage(appdir_path)

            if appimage_path and appimage_path.exists():
                final_path = self.output_dir / config['appimage_name']
                shutil.move(str(appimage_path), str(final_path))
                final_path.chmod(0o755)
                return final_path.exists()

            return False

    def _copy_linux_apprun(self, apprun_path: Path) -> None:
        """
        Copies the AppRun template to the given path.

        Parameters:
            apprun_path (Path): The path to copy the AppRun template to.

        Raises:
            FileNotFoundError: If the AppRun template is not found.
        """

        if not self.apprun_template or not self.apprun_template.exists():

            raise FileNotFoundError("AppRun template not found")

        shutil.copy2(self.apprun_template, apprun_path)
        apprun_path.chmod(0o755)

    def _copy_linux_desktop(self, desktop_path: Path) -> None:
        """
        Copies the desktop file template to the given path.

        Parameters:
            desktop_path (Path): The path to copy the desktop file template to.

        Raises:
            FileNotFoundError: If the desktop file template is not found.
        """

        if not self.desktop_template or not self.desktop_template.exists():

            raise FileNotFoundError("Desktop template not found")

        shutil.copy2(self.desktop_template, desktop_path)

    def _set_linux_permissions(self, appdir_path: Path) -> None:
        """
        Sets the executable permissions for the given application directory.

        Parameters:
            appdir_path (Path): The path to the application directory.
        """

        apprun_path = appdir_path / "AppRun"
        if apprun_path.exists():
            apprun_path.chmod(0o755)

        venv_bin_path = appdir_path / "usr" / "venv" / "bin"

        if venv_bin_path.exists():
            for file_path in venv_bin_path.iterdir():
                if file_path.is_file():
                    file_path.chmod(0o755)

    def _create_appimage(self, appdir_path: Path) -> Optional[Path]:
        """
        Creates an AppImage from the given application directory.

        Parameters:
            appdir_path (Path): The path to the application directory.

        Returns:
            Path: The path to the created AppImage, if successful; otherwise, None.
        """

        print("Creating AppImage...")

        linuxdeploy_path = self.output_dir / "linuxdeploy-x86_64.AppImage"

        try:
            if not linuxdeploy_path.exists():
                print("Downloading linuxdeploy...")
                subprocess.run([
                    'wget', '-q', '--show-progress',
                    'https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage',
                    '-O', str(linuxdeploy_path)
                ], check=True)

            linuxdeploy_path.chmod(0o755)

            print("Generating AppImage...")
            subprocess.run([
                str(linuxdeploy_path),
                '--appdir', str(appdir_path),
                '--output', 'appimage'
            ], cwd=self.output_dir, check=True, capture_output=True)

            for file in self.output_dir.glob("*.AppImage"):

                if file != linuxdeploy_path:
                    return file

        except subprocess.CalledProcessError as error:
            print(f"Error creating AppImage: {error}")

        except FileNotFoundError:
            print("wget not found, cannot download linuxdeploy")

        return None
