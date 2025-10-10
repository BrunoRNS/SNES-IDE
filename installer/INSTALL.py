from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QUrl, QThread

from http.server import HTTPServer, SimpleHTTPRequestHandler
import websockets
import threading
import asyncio
import urllib

from zipfile import ZipInfo, ZipFile
import zipfile
import tarfile
import lzma

from typing import Optional, Tuple, Dict, List
from pathlib import Path
import subprocess
import platform
import tempfile
import shutil
import psutil
import time
import stat
import sys
import os

class LZMAZipExtractor:
    """
    Cross-platform class for extracting LZMA-compressed ZIP files.
    Supports Windows, macOS, and Linux using only native Python libraries.

    Usage example:

        if __name__ == "__main__":

            extractor = LZMAZipExtractor()
    
            try:

                extracted_path = extractor.extract_zip("file_with_lzma.zip", "~/Desktop/extracted")
                print(f"Files extracted to: {extracted_path}")
        
                extracted_path = extractor.extract_zip("file.zip", "~/Desktop/extracted")

                print(f"Extracted content: {len(os.listdir(extracted_path))} items")
        
                extractor.cleanup()
        
            except Exception as e:

                print(f"Error: {e}")
    
    """
    
    def __init__(self) -> None:

        self.supported_compression = [zipfile.ZIP_DEFLATED, zipfile.ZIP_LZMA]
        self.extracted_path = None
    
    def extract_zip(self, zip_path: "str|Path", extract_to: "str|Path", create_subdir:bool=True) -> str:
        """
        Extracts a ZIP file with LZMA compression support.
        
        Args:
            zip_path (str|Path): Path to the ZIP file
            extract_to (str|Path): Destination folder.
            create_subdir (bool): If True, creates subdirectory with ZIP name
            
        Returns:
            str: Path to the extracted folder
            
        Raises:
            ValueError:
                If ZIP file doesn't exist or is invalid, 
                or if extract_to is not defined or is not a path
            RuntimeError:
                If there's LZMA decompression error
        """

        zip_path = Path(zip_path)

        if not zip_path.exists():

            raise ValueError(f"ZIP file not found: {zip_path}")

        if not extract_to or not os.path.exists(extract_to):

            raise ValueError(f"There's no extract_to path or it doesn't exist: {extract_to}")
        
        extract_to = Path(extract_to)
        final_extract_path: Path
        zip_name: str

        if create_subdir:

            zip_name = zip_path.stem
            final_extract_path = extract_to / zip_name

        else:

            final_extract_path = extract_to
        
        final_extract_path.mkdir(parents=True, exist_ok=True)
        
        try:

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:

                zip_info: list[ZipInfo] = zip_ref.infolist()
                
                for file_info in zip_info:

                    self._extract_single_file(zip_ref, file_info, final_extract_path)
            
            self.extracted_path = str(final_extract_path)

            return self.extracted_path
            
        except zipfile.BadZipFile as e:

            raise ValueError(f"Corrupted ZIP file: {e}")

        except Exception as e:

            if final_extract_path.exists() and create_subdir:

                shutil.rmtree(final_extract_path)

            raise RuntimeError(f"Extraction error: {e}")
    
    def _extract_single_file(self, zip_ref: ZipFile, file_info: ZipInfo, extract_path: Path) -> None:
        """
        Extracts a single file from ZIP, handling LZMA compression.
        """

        target_path: Path = extract_path / file_info.filename
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_info.compress_type == zipfile.ZIP_LZMA:

            self._extract_lzma_file(zip_ref, file_info, target_path)

        else:

            zip_ref.extract(file_info, extract_path)
    
    def _extract_lzma_file(self, zip_ref: ZipFile, file_info: ZipInfo, target_path: Path) -> None:
        """
        Manually extracts LZMA compressed file.
        """

        try:

            with zip_ref.open(file_info, 'r') as compressed_file:

                compressed_data = compressed_file.read()
            
            decompressed_data = lzma.decompress(compressed_data)
            
            with open(target_path, 'wb') as output_file:

                output_file.write(decompressed_data)
            
            if hasattr(file_info, 'external_attr'):

                os.chmod(target_path, file_info.external_attr >> 16)
                
        except lzma.LZMAError as e:

            raise RuntimeError(f"LZMA error decompressing {file_info.filename}: {e}")
    
    def get_extracted_path(self) -> "str|None":
        """
        Returns the path of the last extraction.
        
        Returns:
            str or None: Extraction path or None if no extraction occurred
        """
        return self.extracted_path
    
    def cleanup(self) -> bool:
        """
        Removes extracted files (if applicable).
        Useful for cleaning up temporary files.
        """
        if self.extracted_path and os.path.exists(self.extracted_path):

            shutil.rmtree(self.extracted_path)
            self.extracted_path = None

            return True

        return False
    
    @staticmethod
    def is_lzma_zip(zip_path: "str|Path") -> bool:
        """
        Checks if a ZIP file contains LZMA compression.
        
        Args:
            zip_path (str|Path): Path to the ZIP file
            
        Returns:
            bool: True if contains LZMA files
        """

        try:

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:

                for file_info in zip_ref.infolist():

                    if file_info.compress_type == zipfile.ZIP_LZMA:

                        return True

            return False

        except:
            return False


class StaticFileServer(QThread):
    """Static file server running in separate thread"""
    
    def __init__(self, folder_path: str, port: int = 8000):
        """Init StaticFileServer data"""

        super().__init__()

        self.folder_path = folder_path
        self.port = port

        self.server: Optional[HTTPServer] = None
        
    def run(self):
        """Start static file server"""

        os.chdir(self.folder_path)

        handler = SimpleHTTPRequestHandler
        self.server = HTTPServer(('localhost', self.port), handler)

        print(f"Serving files from: {self.folder_path}")
        print(f"URL: http://localhost:{self.port}")

        self.server.serve_forever()
        
    def stop(self):
        """Stop the server"""

        if self.server:

            self.server.shutdown()
            self.server.server_close()


class WebSocketManager:
    """
    WebSocket manager that runs in background
    and allows sending messages from main thread
    """
    
    def __init__(self, port: int = 8080):
        """Init WebSocketManager with default and given values, port is set to 8080, where the
        front-end is trying to connect, don't change here without changing front-end connection."""

        self.port = port
        self.connections: "set[websockets.WebSocketServerProtocol]" = set()
        self.server_thread: Optional[threading.Thread] = None
        self.running = False
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        
    async def _handler(self, websocket, path: str):
        """Handle WebSocket connections"""

        self.connections.add(websocket)
        print(f"WebSocket connected: {websocket.remote_address}")
        
        try:
            await websocket.wait_closed()

        finally:

            self.connections.remove(websocket)
            print(f"WebSocket disconnected: {websocket.remote_address}")
    
    async def _run_server(self):
        """Run WebSocket server"""

        try:

            async with websockets.serve(self._handler, "localhost", self.port):

                print(f"WebSocket server: ws://localhost:{self.port}")
                await asyncio.Future()

        except Exception as e:
            print(f"WebSocket error: {e}")

        finally:
            self.running = False
    
    def _run_in_thread(self):
        """Run asyncio loop in separate thread"""

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        try:
            self.loop.run_until_complete(self._run_server())

        finally:

            if self.loop.is_running():
                self.loop.stop()

            self.loop.close()
    
    def start(self):
        """Start WebSocket server"""

        if self.running:
            return
            
        self.running = True
        self.server_thread = threading.Thread(target=self._run_in_thread, daemon=True)
        self.server_thread.start()

        # Wait 3 seconds to estabilish websocket connection
        time.sleep(3)

        print("WebSocket running in background...")
    
    def stop(self):
        """Stop WebSocket server"""

        if self.running and self.loop:

            self.running = False
            self.loop.call_soon_threadsafe(self.loop.stop)
    
    def send_message(self, message: str):
        """Send message to all connected clients (callable from main thread)"""

        if not self.running or not self.loop:

            print("WebSocket is not running")
            return
            
        if not self.connections:

            print("No WebSocket clients connected")
            return
            
        asyncio.run_coroutine_threadsafe(self._send_to_all(message), self.loop)
        print(f"Message sent to {len(self.connections)} client(s): {message}")
    
    async def _send_to_all(self, message: str):
        """Send message to all clients (async)"""

        if self.connections:

            await asyncio.wait([conn.send(message) for conn in self.connections])
    
    def get_connection_count(self) -> int:
        """Return number of active connections"""

        return len(self.connections)


class PyQtWebApp:
    """
    PySide6 application that loads a folder with web files
    and behaves like an embedded browser
    """
    
    def __init__(
        self, web_folder: str, window_title: str = "PySide6 WebApp", 
        window_size: tuple = (1200, 800), http_port: int = 8000
    ):
        """Init PyQtWebApp with some data"""

        self.web_folder = os.path.abspath(web_folder)
        self.window_title = window_title
        self.window_size = window_size
        self.http_port = http_port
        
        self.app: Optional[QApplication] = None
        self.window: Optional[QMainWindow] = None
        self.web_view: Optional[QWebEngineView] = None
        self.file_server: Optional[StaticFileServer] = None
        
    def start(self):
        """Start PySide6 application and file server"""

        self.file_server = StaticFileServer(self.web_folder, self.http_port)
        self.file_server.start()
        
        time.sleep(1)  # Wait for server to start
        
        # Start PySide6 application
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle(self.window_title)
        self.window.resize(*self.window_size)
        
        # Setup central widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create web view
        self.web_view = QWebEngineView()
        url = QUrl(f"http://localhost:{self.http_port}")
        self.web_view.load(url)
        
        layout.addWidget(self.web_view)
        self.window.setCentralWidget(central_widget)
        
        print(f"PySide6 application started - loading: {url.toString()}")
    
    def show(self):
        """Show the window"""

        if self.window:
            self.window.show()
    
    def close(self):
        """Close application and servers"""

        if self.file_server:
            self.file_server.stop()
            self.file_server.wait()
        
        if self.app:
            self.app.quit()
        
        print("PySide6 application closed")


class SystemRequirementsChecker:
    """
    System requirements checker for cross-platform applications.
    Verifies disk space, OS, architecture, RAM, and package managers.
    """
    
    def __init__(self):
        """Init SystemRequirementsChecker"""
        self.system_info = self._get_system_info()
        self.requirements_met = False
        self.check_results: Dict[str, Tuple[bool, str]] = {}
        self.error_messages: List[str] = []
    
    def _get_system_info(self) -> Dict[str, str]:
        """Get comprehensive system information"""
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'os_release': platform.release(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'platform': platform.platform()
        }
    
    def _get_system_drive(self) -> str:
        """Get the system drive path based on OS"""
        system = self.system_info['os']

        if system == "Windows":
            return os.path.splitdrive(os.environ.get('PROGRAMFILES', 'C:'))[0] + '\\'

        elif system == "Darwin":  # macOS
            return "/Applications/"

        else:  # Linux/Unix
            return "/usr/"
    
    def check_disk_space(self, required_gb: int = 5) -> Tuple[bool, str]:
        """
        Check if required disk space is available on system drive.
        
        Args:
            required_gb: Required free space in GB
            
        Returns:
            Tuple of (success, message)
        """
        try:
            drive = self._get_system_drive()
            disk_usage = psutil.disk_usage(drive)
            free_gb = disk_usage.free / (1024 ** 3)  # Convert to GB
            # required_bytes = required_gb * (1024 ** 3)
            
            success = free_gb >= required_gb
            message = f"Disk space: {free_gb:.1f}GB free of {required_gb}GB required on {drive}"

            return success, message
            
        except Exception as e:
            return False, f"Disk space check failed: {str(e)}"
    
    def check_operating_system(self) -> Tuple[bool, str]:
        """
        Check if operating system meets requirements.
        
        Required:
        - Windows 10+ x86_64
        - macOS BigSur+ arm64
        - Linux Debian/Ubuntu/RHEL amd64
        
        Returns:
            Tuple of (success, message)
        """
        system = self.system_info['os']
        arch = self.system_info['architecture']
        release = self.system_info['os_release']
        
        if system == "Windows":
            # Check Windows version (10+)
            try:
                major_version = int(release.split('.')[0])

                if major_version >= 10 and arch in ['x86_64', 'AMD64']:
                    return True, f"Windows {release} {arch} - compatible"

                else:
                    return False, f"Windows {release} {arch} - requires Windows 10+ x86_64"

            except (ValueError, IndexError):
                return False, f"Windows version check failed"
                
        elif system == "Darwin":  # macOS
            # Check macOS version (BigSur+ = 11.0+)
            try:
                version_str = platform.mac_ver()[0]
                major_version = int(version_str.split('.')[0]) if version_str else 0

                if major_version >= 11 and arch in ['arm64']:
                    return True, f"macOS {version_str} {arch} - compatible"

                else:
                    return False, f"macOS {version_str} {arch} - requires macOS 11.0+ (BigSur) arm64"

            except (ValueError, IndexError):
                return False, "macOS version check failed"
                
        elif system == "Linux":
            # Check Linux distribution and architecture
            distro_info = self._get_linux_distro()
            distro_name = distro_info['name'].lower() if distro_info else "unknown"
            distro_like = distro_info['id_like'].lower() if distro_info else "unknown"
            
            # Check if it's Debian/Ubuntu or RHEL based
            is_debian_based = any(name in distro_name + distro_like for name in ['debian', 'ubuntu', 'mint', 'elementary', 'kali', 'tails'])
            is_rhel_based = any(name in distro_name + distro_like for name in ['redhat', 'rhel', 'centos', 'mandriva', 'fedora', 'rocky', 'alma'])
            
            if (is_debian_based or is_rhel_based) and arch in ['x86_64', 'AMD64']:

                distro_msg = distro_info['name'] if distro_info else "Linux"
                return True, f"{distro_msg} {arch} - compatible"

            else:
                return False, f"Linux {distro_name} {arch} - requires Debian/Ubuntu or RHEL-based amd64"
                
        else:
            return False, f"Unsupported operating system: {system}"
    
    @staticmethod
    def _get_linux_distro() -> Optional[Dict[str, str]]:
        """Get Linux distribution information"""
        try:
            # Try to read /etc/os-release
            with open('/etc/os-release', 'r') as f:
                lines = f.readlines()
            
            distro_info = {}

            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    distro_info[key] = value.strip('"')
            
            return {
                'name': distro_info.get('NAME', 'Unknown'),
                'id': distro_info.get('ID', 'Unknown'),
                'version': distro_info.get('VERSION_ID', 'Unknown'),
                'id_like': distro_info.get('ID_LIKE', 'Unknown'),
            }

        except:

            return None
    
    @staticmethod
    def check_ram(required_gb: int = 1) -> Tuple[bool, str]:
        """
        Check if system has sufficient RAM.
        
        Args:
            required_gb: Required RAM in GB
            
        Returns:
            Tuple of (success, message)
        """
        try:
            memory = psutil.virtual_memory()
            total_gb = memory.total / (1024 ** 3)
            success = total_gb >= required_gb
            message = f"RAM: {total_gb:.1f}GB of {required_gb}GB required"

            return success, message

        except Exception as e:
            return False, f"RAM check failed: {str(e)}"
    
    def check_package_manager(self) -> Tuple[bool, str]:
        """
        Check for required package manager and install if missing.
        
        Returns:
            Tuple of (success, message)
        """

        system = self.system_info['os']
        
        if system == "Windows":
            return self._check_chocolatey()

        elif system == "Darwin":
            return self._check_homebrew()
            
        elif system == "Linux":
            return self._check_linux_package_manager()

        else:
            return False, f"No package manager for {system}"
    
    @staticmethod
    def _check_chocolatey() -> Tuple[bool, str]:
        """Check and install Chocolatey on Windows"""

        try:
            # Check if Chocolatey is installed
            result = subprocess.run(['choco', '--version'], 
                                  capture_output=True, text=True, shell=True)

            if result.returncode == 0:
                return True, "Chocolatey is installed"
            
            # Install Chocolatey
            print("Installing Chocolatey...")
            install_script = (
                "Set-ExecutionPolicy Bypass -Scope Process -Force; "
                "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
                "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
            )
            
            result = subprocess.run(['powershell', '-Command', install_script],
                                  capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                return True, "Chocolatey installed successfully"

            else:
                return False, f"Chocolatey installation failed: {result.stderr}"
                
        except Exception as e:
            return False, f"Chocolatey check failed: {str(e)}"
    
    @staticmethod
    def _check_homebrew() -> Tuple[bool, str]:
        """Check and install Homebrew on macOS"""

        try:
            # Check if Homebrew is installed
            result = subprocess.run(['brew', '--version'], 
                                  capture_output=True, text=True)

            if result.returncode == 0:
                return True, "Homebrew is installed"
            
            # Install Homebrew
            print("Installing Homebrew...")
            install_script = (
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/'
                'Homebrew/install/HEAD/install.sh)"'
            )
            
            result = subprocess.run(install_script, shell=True,
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "Homebrew installed successfully"

            else:
                return False, f"Homebrew installation failed: {result.stderr}"
                
        except Exception as e:
            return False, f"Homebrew check failed: {str(e)}"
    
    @staticmethod
    def _check_linux_package_manager() -> Tuple[bool, str]:
        """Check for apt or rpm on Linux"""
        try:
            # Check for apt (Debian/Ubuntu)
            if shutil.which('apt'):
                result = subprocess.run(['apt', '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return True, "APT package manager is available"
            
            # Check for rpm/dnf/yum (RHEL-based)
            if shutil.which('dnf'):
                return True, "DNF package manager is available"
            elif shutil.which('yum'):
                return True, "YUM package manager is available"
            elif shutil.which('rpm'):
                return True, "RPM package manager is available"
            
            return False, "No supported package manager found (apt/dnf/yum/rpm)"
            
        except Exception as e:
            return False, f"Linux package manager check failed: {str(e)}"
    
    def check_all_requirements(self) -> bool:
        """
        Perform all system requirement checks.
        
        Returns:
            bool: True if all requirements are met
        """
        print("Checking system requirements...")
        print(f"System: {self.system_info['os']} {self.system_info['architecture']}")
        print(f"Platform: {self.system_info['platform']}")
        print()
        
        # Perform all checks
        checks = [
            ("Disk Space", self.check_disk_space(5)),
            ("Operating System", self.check_operating_system()),
            ("RAM", self.check_ram(1)),
            ("Package Manager", self.check_package_manager())
        ]
        
        # Store results
        all_passed = True

        for check_name, (passed, message) in checks:

            status = "PASS" if passed else "FAIL"
            self.check_results[check_name] = (passed, message)

            print(f"{status} {check_name}: {message}")
            
            if not passed:
                all_passed = False
        
        print()

        if all_passed:
            print("All system requirements are met!")
            self.requirements_met = True

        else:
            print("Some requirements are not met. Please address the issues above.")
            self.requirements_met = False
        
        return all_passed
    
    def get_detailed_report(self) -> str:
        """Generate a detailed requirements report"""

        report = []
        report.append("System Requirements Check Report")
        report.append("=" * 40)
        report.append(f"Operating System: {self.system_info['os']}")
        report.append(f"Architecture: {self.system_info['architecture']}")
        report.append(f"Platform: {self.system_info['platform']}")
        report.append("")
        
        for check_name, (passed, message) in self.check_results.items():

            status = "PASS" if passed else "FAIL"
            report.append(f"{check_name}: {status}")
            report.append(f"  {message}")
            report.append("")
        
        report.append(f"Overall: {'PASS' if self.requirements_met else 'FAIL'}")
        return "\n".join(report)
    
    def is_compatible(self) -> bool:
        """Check if system is compatible (OS and architecture only)"""

        os_check, _ = self.check_operating_system()
        return os_check

    def show_error_dialog(self):
        """
        Display a PySide6 error message dialog with system requirement issues.
        
        This method shows a detailed error dialog listing all failed requirements
        and provides guidance on how to resolve them.
        """

        self.error_messages = []

        for check_name, (status, log) in self.check_results.items():
            if not status:
                self.error_messages.append(f"{check_name} FAILED: {log}")

        if not self.error_messages:
            return
            
        try:
            
            # Get or create QApplication instance
            app = QApplication.instance()
            if not app:
                raise Exception("Failed to recognize application")
            
            # Create error message
            error_text = "System requirements check failed:\n\n"
            error_text += "\n".join(self.error_messages)
            
            # Add resolution guidance
            error_text += "\n\nPlease resolve these issues and restart the application."
            
            # Create and show message box
            msg_box = QMessageBox()
            msg_box.setWindowTitle("System Requirements Not Met")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Your system does not meet the minimum requirements")
            msg_box.setDetailedText(error_text)
            msg_box.setStandardButtons(QMessageBox.Ok)
            
            # Set window properties
            msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
            msg_box.resize(600, 400)
            
            print("Displaying system requirements error dialog...")
            msg_box.exec()
            
        except Exception as e:

            print(f"Failed to show error dialog: {e}")
            print("Error details:")
            for error in self.error_messages:
                print(f"\t{error}")

"""
==================================================================================
TO CHECK:
==================================================================================
"""

class ApplicationInstaller:
    """
    Multi-platform application installer that handles dependency installation
    and application setup across Windows, macOS, and Linux.
    """
    
    def __init__(self, app_name: str = "MyApp", app_version: str = "1.0.0"):
        self.app_name = app_name
        self.app_version = app_version
        self.system_info = self._get_system_info()
        self.app_dir = self._get_app_directory()
        self.temp_dir = self._get_temp_directory()
        self.desktop_dir = self._get_desktop_directory()
        
        # Create necessary directories
        os.makedirs(self.app_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def _get_system_info(self) -> dict:
        """Get detailed system information"""
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'os_release': platform.release(),
            'architecture': platform.machine(),
            'platform': platform.platform()
        }
    
    def _get_app_directory(self) -> Path:
        """Get application installation directory based on OS"""
        system = self.system_info['os']
        if system == "Windows":
            return Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')) / self.app_name
        elif system == "Darwin":
            return Path("/Applications") / f"{self.app_name}.app"
        else:  # Linux
            return Path("/opt") / self.app_name
    
    def _get_temp_directory(self) -> Path:
        """Get temporary directory for downloads"""
        temp_base = Path(os.environ.get('TEMP', '/tmp'))
        return temp_base / f"{self.app_name}_install"
    
    def _get_desktop_directory(self) -> Path:
        """Get desktop directory for shortcuts"""
        system = self.system_info['os']
        if system == "Windows":
            return Path(os.path.expanduser("~")) / "Desktop"
        elif system == "Darwin":
            return Path.home() / "Desktop"
        else:  # Linux
            return Path.home() / "Desktop"
    
    def _run_command(self, command: List[str], shell: bool = False) -> Tuple[bool, str]:
        """
        Run a system command and return success status and output.
        
        Args:
            command: Command to execute
            shell: Whether to run in shell mode
            
        Returns:
            Tuple of (success, output)
        """
        try:
            if shell and isinstance(command, list):
                command = " ".join(command)
            
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            
            return success, output
            
        except subprocess.TimeoutExpired:
            return False, "Command timed out after 5 minutes"
        except Exception as e:
            return False, f"Command execution failed: {str(e)}"
    
    def _download_file(self, url: str, destination: Path) -> bool:
        """
        Download a file from URL to destination.
        
        Args:
            url: URL to download from
            destination: Local path to save file
            
        Returns:
            bool: True if download successful
        """
        try:
            print(f"📥 Downloading: {url}")
            urllib.request.urlretrieve(url, destination)
            print(f"✅ Downloaded: {destination.name}")
            return True
        except Exception as e:
            print(f"❌ Download failed: {str(e)}")
            return False
    
    def _extract_archive(self, archive_path: Path, extract_to: Path) -> bool:
        """
        Extract archive file (zip, tar.gz, etc.)
        
        Args:
            archive_path: Path to archive file
            extract_to: Directory to extract to
            
        Returns:
            bool: True if extraction successful
        """
        try:
            print(f"📦 Extracting: {archive_path.name}")
            
            if archive_path.suffix == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            elif archive_path.suffix in ['.tar', '.gz', '.bz2', '.xz']:
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_to)
            else:
                print(f"❌ Unsupported archive format: {archive_path.suffix}")
                return False
            
            print(f"✅ Extracted to: {extract_to}")
            return True
            
        except Exception as e:
            print(f"❌ Extraction failed: {str(e)}")
            return False
    
    def _make_executable(self, file_path: Path) -> bool:
        """
        Make a file executable (Unix-like systems)
        
        Args:
            file_path: Path to file
            
        Returns:
            bool: True if successful
        """
        try:
            if self.system_info['os'] != "Windows":
                file_path.chmod(file_path.stat().st_mode | stat.S_IEXEC)
            return True
        except Exception as e:
            print(f"❌ Failed to make executable: {str(e)}")
            return False
    
    def install_make(self) -> bool:
        """
        Install make (gmake for macOS)
        
        Returns:
            bool: True if installation successful
        """
        system = self.system_info['os']
        print("🔧 Installing make...")
        
        if system == "Windows":
            # Install make using Chocolatey
            success, output = self._run_command(['choco', 'install', 'make', '-y'])
            if success:
                print("✅ make installed via Chocolatey")
            return success
            
        elif system == "Darwin":
            # Install gmake using Homebrew
            success, output = self._run_command(['brew', 'install', 'make'])
            if success:
                print("✅ gmake installed via Homebrew")
            return success
            
        else:  # Linux
            # Install make using package manager
            if shutil.which('apt'):
                success, output = self._run_command(['sudo', 'apt', 'update'])
                success, output = self._run_command(['sudo', 'apt', 'install', '-y', 'make'])
            elif shutil.which('dnf'):
                success, output = self._run_command(['sudo', 'dnf', 'install', '-y', 'make'])
            elif shutil.which('yum'):
                success, output = self._run_command(['sudo', 'yum', 'install', '-y', 'make'])
            else:
                print("❌ No supported package manager found for make installation")
                return False
            
            if success:
                print("✅ make installed via package manager")
            return success
    
    def install_dotnet_sdk_8(self) -> bool:
        """
        Install .NET SDK 8
        
        Returns:
            bool: True if installation successful
        """
        system = self.system_info['os']
        print("🔧 Installing .NET SDK 8...")
        
        if system == "Windows":
            # Install using Chocolatey
            success, output = self._run_command(['choco', 'install', 'dotnet-8.0-sdk', '-y'])
            if success:
                print("✅ .NET SDK 8 installed via Chocolatey")
            return success
            
        elif system == "Darwin":
            # Install using Homebrew
            success, output = self._run_command(['brew', 'install', '--cask', 'dotnet-sdk'])
            if success:
                print("✅ .NET SDK 8 installed via Homebrew")
            return success
            
        else:  # Linux
            # Install using package manager or Microsoft's script
            if shutil.which('apt'):
                # Ubuntu/Debian
                commands = [
                    ['wget', 'https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb', '-O', '/tmp/packages-microsoft-prod.deb'],
                    ['sudo', 'dpkg', '-i', '/tmp/packages-microsoft-prod.deb'],
                    ['sudo', 'apt', 'update'],
                    ['sudo', 'apt', 'install', '-y', 'dotnet-sdk-8.0']
                ]
            elif shutil.which('dnf'):
                # RHEL/Fedora
                commands = [
                    ['sudo', 'rpm', '-Uvh', 'https://packages.microsoft.com/config/rhel/8/packages-microsoft-prod.rpm'],
                    ['sudo', 'dnf', 'install', '-y', 'dotnet-sdk-8.0']
                ]
            else:
                print("❌ Unsupported Linux distribution for .NET SDK installation")
                return False
            
            for cmd in commands:
                success, output = self._run_command(cmd)
                if not success:
                    print(f"❌ .NET SDK installation failed: {output}")
                    return False
            
            print("✅ .NET SDK 8 installed")
            return True
    
    def move_executables_to_app_dir(self) -> bool:
        """
        Move executables to application directory
        
        Returns:
            bool: True if successful
        """
        print("📁 Moving executables to app directory...")
        
        # This would depend on your specific application structure
        # Example: move from temp directory to app directory
        source_dir = self.temp_dir / "bin"
        dest_dir = self.app_dir / "bin"
        
        try:
            if source_dir.exists():
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(source_dir, dest_dir)
                print(f"✅ Executables moved to: {dest_dir}")
                return True
            else:
                print("⚠️ No executables found to move")
                return True
                
        except Exception as e:
            print(f"❌ Failed to move executables: {str(e)}")
            return False
    
    def install_jdk_8_with_fx(self) -> bool:
        """
        Install JDK 8 with JavaFX
        
        Returns:
            bool: True if installation successful
        """
        print("☕ Installing JDK 8 with JavaFX...")
        
        # URLs for JDK 8 with JavaFX (these are examples - replace with actual URLs)
        jdk_urls = {
            "Windows": "https://example.com/jdk8-windows-fx.zip",
            "Darwin": "https://example.com/jdk8-macos-fx.tar.gz", 
            "Linux": "https://example.com/jdk8-linux-fx.tar.gz"
        }
        
        system = self.system_info['os']
        url = jdk_urls.get(system)
        
        if not url:
            print(f"❌ No JDK URL available for {system}")
            return False
        
        # Download JDK
        archive_path = self.temp_dir / f"jdk8-fx.{'zip' if system == 'Windows' else 'tar.gz'}"
        if not self._download_file(url, archive_path):
            return False
        
        # Extract to app directory
        jdk_dir = self.app_dir / "jdk"
        if not self._extract_archive(archive_path, jdk_dir):
            return False
        
        # Set JAVA_HOME environment variable (optional)
        if system != "Windows":
            # For Unix-like systems, we can create a symlink or set environment
            java_home = jdk_dir / "Contents/Home" if system == "Darwin" else jdk_dir
            print(f"✅ JDK installed. JAVA_HOME would be: {java_home}")
        else:
            print("✅ JDK installed for Windows")
        
        return True
    
    def run_install_scripts(self) -> bool:
        """
        Run required installation scripts
        
        Returns:
            bool: True if all scripts successful
        """
        print("📜 Running installation scripts...")
        
        scripts_dir = self.temp_dir / "scripts"
        if not scripts_dir.exists():
            print("⚠️ No scripts directory found")
            return True
        
        system = self.system_info['os']
        
        for script_file in scripts_dir.iterdir():
            if system == "Windows" and script_file.suffix == '.bat':
                success, output = self._run_command([str(script_file)], shell=True)
            elif system != "Windows" and script_file.suffix == '.sh':
                self._make_executable(script_file)
                success, output = self._run_command([str(script_file)])
            else:
                continue
            
            if not success:
                print(f"❌ Script failed: {script_file.name} - {output}")
                return False
            else:
                print(f"✅ Script executed: {script_file.name}")
        
        print("✅ All installation scripts completed")
        return True
    
    def create_shortcut(self) -> bool:
        """
        Create desktop shortcut (Windows) or .desktop file (Linux) or symlink (macOS)
        
        Returns:
            bool: True if shortcut creation successful
        """
        print("🔗 Creating shortcut...")
        
        system = self.system_info['os']
        main_executable = self.app_dir / "bin" / f"{self.app_name.lower()}.exe" if system == "Windows" else self.app_dir / "bin" / self.app_name.lower()
        
        if not main_executable.exists():
            print(f"⚠️ Main executable not found: {main_executable}")
            return False
        
        if system == "Windows":
            # Create .lnk shortcut on Windows
            shortcut_path = self.desktop_dir / f"{self.app_name}.lnk"
            
            # Using PowerShell to create shortcut
            ps_script = f"""
            $WshShell = New-Object -comObject WScript.Shell
            $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
            $Shortcut.TargetPath = "{main_executable}"
            $Shortcut.WorkingDirectory = "{self.app_dir}"
            $Shortcut.Save()
            """
            
            success, output = self._run_command(['powershell', '-Command', ps_script])
            if success:
                print(f"✅ Windows shortcut created: {shortcut_path}")
            return success
            
        elif system == "Darwin":
            # Create .app bundle or symlink
            # For simplicity, creating a symlink in Applications
            apps_dir = Path("/Applications")
            app_link = apps_dir / f"{self.app_name}.app"
            
            try:
                if app_link.exists():
                    app_link.unlink()
                
                # Create actual .app bundle structure would be more complex
                # For now, creating a simple symlink
                app_link.symlink_to(self.app_dir)
                print(f"✅ macOS application link created: {app_link}")
                return True
            except Exception as e:
                print(f"❌ Failed to create macOS shortcut: {str(e)}")
                return False
                
        else:  # Linux
            # Create .desktop file
            desktop_file = self.desktop_dir / f"{self.app_name}.desktop"
            desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={self.app_name}
Comment={self.app_name} Application
Exec={main_executable}
Icon={self.app_dir / "icon.png"}
Terminal=false
StartupWMClass={self.app_name}
Categories=Utility;
"""
            
            try:
                with open(desktop_file, 'w') as f:
                    f.write(desktop_content)
                
                # Make executable
                desktop_file.chmod(desktop_file.stat().st_mode | stat.S_IEXEC)
                
                # Also create symlink in /usr/local/bin for command line access
                bin_link = Path("/usr/local/bin") / self.app_name.lower()
                if bin_link.exists():
                    bin_link.unlink()
                bin_link.symlink_to(main_executable)
                
                print(f"✅ Linux .desktop file created: {desktop_file}")
                return True
                
            except Exception as e:
                print(f"❌ Failed to create Linux shortcut: {str(e)}")
                return False
    
    def verify_installation(self) -> bool:
        """
        Verify that installation was successful
        
        Returns:
            bool: True if verification passed
        """
        print("🔍 Verifying installation...")
        
        checks = []
        
        # Check if app directory exists and has content
        checks.append(("App directory", self.app_dir.exists() and any(self.app_dir.iterdir())))
        
        # Check if main executable exists
        system = self.system_info['os']
        main_executable = self.app_dir / "bin" / f"{self.app_name.lower()}.exe" if system == "Windows" else self.app_dir / "bin" / self.app_name.lower()
        checks.append(("Main executable", main_executable.exists()))
        
        # Check if .NET is available
        success, output = self._run_command(['dotnet', '--version'])
        checks.append((".NET SDK", success and '8.' in output))
        
        # Check if make is available
        make_cmd = 'gmake' if system == "Darwin" else 'make'
        success, output = self._run_command([make_cmd, '--version'])
        checks.append(("Make tool", success))
        
        # Check if Java is available (if JDK was installed)
        jdk_dir = self.app_dir / "jdk"
        if jdk_dir.exists():
            java_exec = jdk_dir / "bin" / "java"
            if system == "Darwin":
                java_exec = jdk_dir / "Contents/Home/bin/java"
            
            success, output = self._run_command([str(java_exec), '-version'])
            checks.append(("Java Runtime", success))
        
        # Print results
        all_passed = True
        for check_name, passed in checks:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("🎉 Installation verification successful!")
        else:
            print("⚠️ Some installation checks failed")
        
        return all_passed
    
    def cleanup_temp_files(self) -> bool:
        """
        Clean up temporary installation files
        
        Returns:
            bool: True if cleanup successful
        """
        print("🧹 Cleaning up temporary files...")
        
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            print("✅ Temporary files cleaned up")
            return True
        except Exception as e:
            print(f"⚠️ Failed to clean up temp files: {str(e)}")
            return False
    
    def install_all(self) -> bool:
        """
        Execute all installation steps
        
        Returns:
            bool: True if all steps successful
        """
        print(f"🚀 Starting {self.app_name} installation...")
        print(f"📁 Install directory: {self.app_dir}")
        print(f"💻 Platform: {self.system_info['os']} {self.system_info['architecture']}")
        print()
        
        installation_steps = [
            ("Installing make", self.install_make),
            ("Installing .NET SDK 8", self.install_dotnet_sdk_8),
            ("Moving executables", self.move_executables_to_app_dir),
            ("Installing JDK 8 with JavaFX", self.install_jdk_8_with_fx),
            ("Running install scripts", self.run_install_scripts),
            ("Creating shortcut", self.create_shortcut),
            ("Verifying installation", self.verify_installation),
            ("Cleaning up", self.cleanup_temp_files),
        ]
        
        for step_name, step_function in installation_steps:
            print(f"\n{'='*50}")
            print(f"Step: {step_name}")
            print(f"{'='*50}")
            
            if not step_function():
                print(f"❌ Installation failed at: {step_name}")
                return False
        
        print(f"\n{'='*50}")
        print(f"🎉 {self.app_name} installation completed successfully!")
        print(f"📁 Location: {self.app_dir}")
        print(f"{'='*50}")
        
        return True

"""
==================================================================================

==================================================================================
"""

def get_executable_path():
    """Get the path of the executable or script based on whether the script is frozen 
    (PyInstaller) or not."""

    if getattr(sys, 'frozen', False):
        # PyInstaller executable
        print("executable path mode chosen")

        return Path(sys.executable).absolute().parent
        
    else:
        # Normal script
        print("Python script path mode chosen")

        return Path(__file__).absolute().parent


def install(ws: WebSocketManager, zip_extractor: LZMAZipExtractor, local_dir: Path):
    """Make all nine install steps"""
    
    steps = [
        # Install make(gmake for macOS)
        ...,
        # Install .net-sdk-8
        ...,
        # Move Executables to App dir
        ...,
        # Uncompress JDK-8 + FX to App dir
        ...,
        # Run required install scripts
        ...,
        # Move shortcut executable to Desktop(or /usr/local/bin and create .desktop file)
        ...,
        # Verify instalation
        ...,
    ]

def main():
    """Main Logic of the INSTALL application"""

    checker = SystemRequirementsChecker()
    print("System Requirements Checker")
    print("=" * 30)

    requirements_met = checker.check_all_requirements()

    zip_extractor = LZMAZipExtractor()
    ws = WebSocketManager()
    
    try:
        ws.start()

        with tempfile.TemporaryDirectory() as temp_dir:

            web_path = zip_extractor.extract_zip(
                get_executable_path() / "gui" / "installer-gui.zip", temp_dir, create_subdir=True
            )

            app = PyQtWebApp(
                web_path, window_title="SNES-IDE Installer"
            )

            app.start()

            if not requirements_met:

                checker.show_error_dialog()
                time.sleep(5)
                exit(-1)

            app.show()

            while True:

                if ws.get_connection_count() > 0:
                    break
            
            install(ws, zip_extractor, get_executable_path())

    except Exception as e:

        print(f"Error while executing installer: {e}")
    
    finally:
        app.close()
        ws.stop()

if __name__ == "__main__":
    main()
