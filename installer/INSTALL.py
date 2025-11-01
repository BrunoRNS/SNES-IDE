"""
SNES-IDE - INSTALL.py
Copyright (C) 2025 BrunoRNS

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import Qt, QUrl, QThread, QCoreApplication
from PySide6.QtWebEngineWidgets import QWebEngineView

from http.server import HTTPServer, SimpleHTTPRequestHandler
from websockets.server import serve
from websockets import exceptions
from asyncio import Task
import threading
import asyncio

from zipfile import ZipInfo, ZipFile
import zipfile
import lzma

from typing import Optional, Callable, Tuple, Dict, List, Type, Any
from subprocess import CompletedProcess
from typing_extensions import Literal

from pathlib import Path
import subprocess
import platform
import tempfile
import shutil
import psutil
import ctypes
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

        self.supported_compression: list[int] = [zipfile.ZIP_DEFLATED, zipfile.ZIP_LZMA]
        self.extracted_path: "None|str|Path" = None
    
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

        zip_path_path: Path = Path(zip_path)

        if not zip_path_path.exists():

            raise ValueError(f"ZIP file not found: {zip_path_path}")

        if not extract_to or not os.path.exists(extract_to):

            raise ValueError(f"There's no extract_to path or it doesn't exist: {extract_to}")
        
        extract_to_path: Path = Path(extract_to)
        final_extract_path: Path
        zip_name: str

        if create_subdir:

            zip_name = zip_path_path.stem
            final_extract_path = extract_to_path / zip_name

        else:

            final_extract_path = extract_to_path
        
        final_extract_path.mkdir(parents=True, exist_ok=True)
        
        try:

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:

                zip_info: List[ZipInfo] = zip_ref.infolist()
                
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
        """Extracts a single file from ZIP, handling LZMA compression."""
    
        file_path = Path(file_info.filename)
        if file_path.is_absolute() or ".." in file_path.parts:
            print(f"Security warning: Skipping suspicious path {file_info.filename}")
            return
        
        target_path: Path = extract_path / file_info.filename
    
        try:
            target_path.resolve().relative_to(extract_path.resolve())
        except ValueError:
            print(f"Security warning: Path traversal attempt blocked: {file_info.filename}")
            return
        
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

                compressed_data: bytes = compressed_file.read()
            
            decompressed_data: bytes = lzma.decompress(compressed_data)
            
            with open(target_path, 'wb') as output_file:

                output_file.write(decompressed_data)
            
            if hasattr(file_info, 'external_attr'):

                os.chmod(target_path, file_info.external_attr >> 16)
                
        except lzma.LZMAError as e:

            raise RuntimeError(f"LZMA error decompressing {file_info.filename}: {e}")
    
    def get_extracted_path(self) -> "str|Path|None":
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
    
    def __init__(self, folder_path: str, port: int = 8000) -> None:
        """Init StaticFileServer data"""

        super().__init__()

        self.folder_path: str = folder_path
        self.port: int = port

        self.server: Optional[HTTPServer] = None
        
    def run(self) -> None:
        """Start static file server"""

        os.chdir(self.folder_path)

        handler: Type[SimpleHTTPRequestHandler] = SimpleHTTPRequestHandler
        self.server = HTTPServer(('localhost', self.port), handler)

        print(f"Serving files from: {self.folder_path}")
        print(f"URL: http://localhost:{self.port}")

        self.server.serve_forever()
        
    def stop(self) -> None:
        """Stop the server"""

        if self.server:

            self.server.shutdown()
            self.server.server_close()

class WebSocketManager:
    """
    WebSocket manager that runs in background
    and allows sending messages from main thread
    """
    
    def __init__(self, port: int = 8080) -> None:
        """Init WebSocketManager with default and given values, port is set to 8080, where the
        front-end is trying to connect, don't change here without changing front-end connection."""

        self.port: int = port
        self.connections: set[Any] = set()
        self.server_thread: Optional[threading.Thread] = None
        self.running: bool = False
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.server: Optional[Any] = None
        
    async def _handler(self, websocket: Any) -> None:
        """Handle WebSocket connections"""

        self.connections.add(websocket)
        print(f"WebSocket connected: {websocket.remote_address}")
        
        try:
            await websocket.wait_closed()

        finally:
            self.connections.remove(websocket)
            print(f"WebSocket disconnected: {websocket.remote_address}")
    
    async def _run_server(self) -> None:
        """Run WebSocket server"""

        try:
            self.server = await serve(self._handler, "localhost", self.port)
            print(f"WebSocket server: ws://localhost:{self.port}")

            await asyncio.Future()

        except exceptions.ConnectionClosed:
            pass

        except Exception as e:
            print(f"WebSocket error: {e}")

        finally:
            self.running = False
    
    def _run_in_thread(self) -> None:
        """Run asyncio loop in separate thread"""

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        try:
            self.loop.run_until_complete(self._run_server())

        finally:
            if self.loop.is_running():
                self.loop.stop()
            self.loop.close()
    
    def start(self) -> None:
        """Start WebSocket server"""
        if self.running:
            return
        
        self.running = True
        self.server_thread = threading.Thread(target=self._run_in_thread, daemon=True)
        self.server_thread.start()
        
        max_wait: int = 150
        for _ in range(max_wait):
            if self.loop and self.loop.is_running():
                time.sleep(0.1)
            else:
                break
    
    def stop(self) -> None:
        """Stop WebSocket server"""

        if self.running and self.loop:
            self.running = False
            self.loop.call_soon_threadsafe(self.loop.stop)
    
    def stop_with_error(self, reason: str = "Unknown installation error") -> None:
        """Stop WebSocket server with code 1101, error"""
        
        future: Any = None

        if self.running and self.loop:
            self.running = False
        
            future = asyncio.run_coroutine_threadsafe(
                self._close_all_with_error(reason), 
                self.loop
            )
        
        try:
            future.result(timeout=5.0)
            print(f"WebSocket server stopped with error: {reason}")
            
        except Exception as e:
            print(f"WebSocket stop timeout: {e}")

    async def _close_all_with_error(self, reason: str) -> None:
        """Close all connections with error code 1101"""

        if self.connections:

            error_message: str = f"ERROR: {reason}"
            send_tasks: list[Task[Any]] = [
                asyncio.create_task(conn.send(error_message))
                for conn in self.connections.copy()
            ]
            
            if send_tasks:
                await asyncio.wait(send_tasks, timeout=2.0)
            
            close_tasks: list[Task[Any]] = [
                asyncio.create_task(conn.close(code=1101, reason=reason))
                for conn in self.connections.copy()
            ]
            
            if close_tasks:
                await asyncio.wait(close_tasks, timeout=2.0)
            
            self.connections.clear()
        
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        if self.loop and self.loop.is_running():
            self.loop.stop()
    
    def send_message(self, message: str) -> None:
        """Send message to all connected clients (callable from main thread)"""

        if not self.running or not self.loop:
            print("WebSocket is not running")
            return
            
        if not self.connections:
            print("No WebSocket clients connected")
            return
            
        asyncio.run_coroutine_threadsafe(self._send_to_all(message), self.loop)
        print(f"Message sent to {len(self.connections)} client(s): {message}")
    
    async def _send_to_all(self, message: str) -> None:
        """Send message to all clients (async)"""

        if self.connections:

            await asyncio.wait(
                [asyncio.create_task(conn.send(message)) for conn in self.connections],
            )
    
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
        window_size: Tuple[int, int] = (1200, 800), http_port: int = 8000
    ) -> None:
        """Init PyQtWebApp with some data"""

        self.web_folder: str = os.path.abspath(web_folder)
        self.window_title: str = window_title
        self.window_size: Tuple[int, int] = window_size
        self.http_port: int = http_port
        
        self.app: Optional[QApplication] = None
        self.window: Optional[QMainWindow] = None
        self.web_view: Optional[QWebEngineView] = None
        self.file_server: Optional[StaticFileServer] = None
        
    def start(self) -> None:
        """Start PySide6 application and file server"""

        self.file_server = StaticFileServer(self.web_folder, self.http_port)
        self.file_server.start()
        
        time.sleep(1)
        
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        try:
            self.window.setStyle('Fusion') # type: ignore
        except: ...
        self.window.setWindowTitle(self.window_title)
        self.window.resize(*self.window_size)
        
        central_widget: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.web_view = QWebEngineView()
        url: QUrl = QUrl(f"http://localhost:{self.http_port}")
        self.web_view.load(url)
        
        layout.addWidget(self.web_view)
        self.window.setCentralWidget(central_widget)
        
        print(f"PySide6 application started - loading: {url.toString()}")
    
    def show(self) -> None:
        """Show the window"""

        if self.window:
            self.window.show()
    
    def close(self) -> None:
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
    
    def __init__(self) -> None:
        """Init SystemRequirementsChecker"""

        self.system_info: Dict[str, str] = self._get_system_info()
        self.requirements_met: bool = False
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

        system: str = self.system_info['os']

        if system.lower() == "windows":
            return os.path.splitdrive(os.environ.get('PROGRAMFILES', 'C:'))[0] + '\\'

        elif system.lower() == "darwin":
            return "/Applications/"

        else:
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

            drive: str = self._get_system_drive()
            disk_usage: Any = psutil.disk_usage(drive)
            free_gb: float = disk_usage.free / (1024 ** 3)
            
            success: bool = free_gb >= required_gb
            message: str = f"Disk space: {free_gb:.1f}GB free of {required_gb}GB required on {drive}"

            return success, message
            
        except Exception as e:

            return False, f"Disk space check failed: {str(e)}"
    
    def check_operating_system(self) -> Tuple[bool, str]:
        """
        Check if operating system meets requirements.
        
        Required:
        - Windows 10+ x86_64
        - macOS BigSur+ arm64
        - Linux Ubuntu amd64
        
        Returns:
            Tuple of (success, message)
        """
        system: str = self.system_info['os']
        arch: str = self.system_info['architecture']
        release: str = self.system_info['os_release']
        
        if system.lower() == "windows":
            try:

                major_version: int = int(release.split('.')[0])

                if major_version >= 10 and arch in ['x86_64', 'AMD64']:
                    return True, f"Windows {release} {arch} - compatible"

                else:
                    return False, f"Windows {release} {arch} - requires Windows 10+ x86_64"

            except (ValueError, IndexError):

                return False, f"Windows version check failed"
                
        elif system == "Darwin":

            try:
                version_str: str = platform.mac_ver()[0]
                major_version = int(version_str.split('.')[0]) if version_str else 0

                if major_version >= 11 and arch in ['arm64']:
                    return True, f"macOS {version_str} {arch} - compatible"

                else:
                    return False, f"macOS {version_str} {arch} - requires macOS 11.0+ (BigSur) arm64"

            except (ValueError, IndexError):
                return False, "macOS version check failed"
                
        elif system == "Linux":
            distro_info: "Dict[str, str] | None" = self._get_linux_distro()
            distro_name: str = distro_info['name'].lower() if distro_info else "unknown"
            distro_like: str = distro_info['id_like'].lower() if distro_info else "unknown"
            
            is_ubuntu_based: bool = any(name in distro_name + distro_like for name in ['ubuntu', 'mint', 'elementary'])
            
            if (is_ubuntu_based) and arch.lower() in ['x86_64', 'amd64']:

                distro_msg: str = distro_info['name'] if distro_info else "Linux"
                return True, f"{distro_msg} {arch} - compatible"

            else:
                return False, f"Linux {distro_name} {arch} - requires Ubuntu amd64"
                
        else:

            return False, f"Unsupported operating system: {system}"
    
    @staticmethod
    def _get_linux_distro() -> Optional[Dict[str, str]]:
        """Get Linux distribution information"""
        try:
            with open('/etc/os-release', 'r') as f:
                lines: List[str] = f.readlines()
            
            distro_info: Dict[str, str] = {}

            for line in lines:
                if '=' in line:
                    key: str = line.strip().split('=', 1)[0]
                    value: str = line.strip().split('=', 1)[1]
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
            memory: Any = psutil.virtual_memory()
            total_gb: int = memory.total / (1024 ** 3)
            success: bool = total_gb >= required_gb
            message: str = f"RAM: {total_gb:.1f}GB of {required_gb}GB required"

            return success, message

        except Exception as e:
            return False, f"RAM check failed: {str(e)}"
    
    def check_package_manager(self) -> Tuple[bool, str]:
        """
        Check for required package manager and install if missing.
        
        Returns:
            Tuple of (success, message)
        """

        system: str = self.system_info['os']
        
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
            result: CompletedProcess[str] = subprocess.run(['choco', '--version'], 
                                  capture_output=True, text=True, shell=True)

            if result.returncode == 0:
                return True, "Chocolatey is installed"
            
            print("Installing Chocolatey...")
            install_script: str = (
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
            result: CompletedProcess[str] = subprocess.run(['brew', '--version'], 
                                  capture_output=True, text=True)

            if result.returncode == 0:
                return True, "Homebrew is installed"
            
            print("Installing x-code...")
            xcode: CompletedProcess[str] = subprocess.run(["xcode-select", "--install"], capture_output=True, text=True)

            print("Installing Homebrew...")
            install_script: str = (
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/'
                'Homebrew/install/HEAD/install.sh)"'
            )

            xcode_success: bool = xcode.returncode in [0, 1]
            
            result = subprocess.run(install_script, shell=True,
                                  capture_output=True, text=True)
            
            if result.returncode == 0 and xcode_success:
                return True, "Homebrew installed successfully"

            else:
                return False, f"Homebrew installation failed: {result.stderr}"
                
        except Exception as e:
            return False, f"Homebrew check failed: {str(e)}"
    
    @staticmethod
    def _check_linux_package_manager() -> Tuple[bool, str]:
        """Check for apt on Linux"""
        try:
            if shutil.which('apt'):
                result: CompletedProcess[str] = subprocess.run(['apt', '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return True, "APT package manager is available"
            
            return False, "No supported package manager found apt"
            
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
        
        checks: List[Tuple[str, Tuple[bool, str]]] = [
            ("Disk Space", self.check_disk_space(required_gb=10)),
            ("Operating System", self.check_operating_system()),
            ("RAM", self.check_ram(1)),
            ("Package Manager", self.check_package_manager())
        ]
        
        all_passed: bool = True

        for check_name, (passed, message) in checks:

            status: Literal['PASS', 'FAIL'] = "PASS" if passed else "FAIL"
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

        report: List[str] = []
        report.append("System Requirements Check Report")
        report.append("=" * 40)
        report.append(f"Operating System: {self.system_info['os']}")
        report.append(f"Architecture: {self.system_info['architecture']}")
        report.append(f"Platform: {self.system_info['platform']}")
        report.append("")
        
        for check_name, (passed, message) in self.check_results.items():

            status: Literal['PASS', 'FAIL'] = "PASS" if passed else "FAIL"
            report.append(f"{check_name}: {status}")
            report.append(f"  {message}")
            report.append("")
        
        report.append(f"Overall: {'PASS' if self.requirements_met else 'FAIL'}")
        return "\n".join(report)
    
    def is_compatible(self) -> bool:
        """Check if system is compatible (OS and architecture only)"""

        os_check: bool
        _: str

        os_check, _ = self.check_operating_system()
        return os_check

    def show_error_dialog(self) -> None:
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
            
            app: "QCoreApplication | None" = QApplication.instance() # type: ignore
            if not app:
                raise Exception("Failed to recognize application")
            
            error_text: str = "System requirements check failed:\n\n"
            error_text += "\n".join(self.error_messages)
            
            error_text += "\n\nPlease resolve these issues and restart the application."
            
            msg_box: QMessageBox = QMessageBox()
            msg_box.setWindowTitle("System Requirements Not Met")
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setText("Your system does not meet the minimum requirements")
            msg_box.setDetailedText(error_text)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            
            msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msg_box.resize(600, 400)
            
            print("Displaying system requirements error dialog...")
            msg_box.exec()
            
        except Exception as e:

            print(f"Failed to show error dialog: {e}")
            print("Error details:")
            for error in self.error_messages:
                print(f"\t{error}")


class ApplicationInstaller:
    """
    Multi-platform application installer that handles dependency installation
    and application setup across Windows, macOS, and Linux.
    """
    
    def __init__(
        self, 
        app_version: str,
        local_dir: Path,
        zip_extractor: LZMAZipExtractor,
        app_name: str = "SNES-IDE",
    ) -> None:
        """Init class ApplicationInstaller"""

        self.app_name: str = app_name
        self.app_version: str = app_version
        self.system_info: Dict[str, str] = self._get_system_info()
        self.app_dir: Path = self._get_app_directory()
        self.temp_dir: Path = self._get_temp_directory()
        self.desktop_dir: Path = self._get_desktop_directory()
        self.local_dir: Path = local_dir
        self.zip_extractor: LZMAZipExtractor = zip_extractor
        
        # Create necessary directories
        os.makedirs(self.app_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def _get_system_info(self) -> Dict[str, str]:
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

        system: str = self.system_info['os']

        if system == "Windows":
            return Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')) / self.app_name

        elif system == "Darwin":
            return Path("/Applications") / f"{self.app_name}.app"

        else:
            return Path("/opt") / self.app_name
    
    def _get_temp_directory(self) -> Path:
        """Get temporary directory for downloads"""

        temp_base: Path = Path(os.environ.get('TEMP', tempfile.gettempdir()))
        return temp_base / f"{self.app_name}_install"
    
    def _get_desktop_directory(self) -> Path:
        """Get desktop directory for shortcuts"""

        return Path.home().resolve() / 'Desktop'
        
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


            command_str: str = " ".join(command)
            
            result: CompletedProcess[str] = subprocess.run(
                [command_str],
                shell=shell,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            success: bool = result.returncode == 0
            output: str = result.stdout if success else result.stderr
            
            return success, output
            
        except subprocess.TimeoutExpired:
            return False, "Command timed out after 10 minutes"

        except Exception as e:
            return False, f"Command execution failed: {str(e)}"
    
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

            print(f"Failed to make executable: {str(e)}")
            return False
    
    def install_make_cmake_gpp(self) -> bool:
        """
        Install make (gmake for macOS)
        
        Returns:
            bool: True if installation successful
        """
        system: str = self.system_info['os']
        print("Installing make...")

        success: bool
        output: str
        
        if system == "Windows":
            success, output = self._run_command(['choco', 'install', 'make', '-y'])

            if success:
                print(f"make installed via Chocolatey: {output}")
            
            success, output = self._run_command(['choco', 'install', 'cmake', "--installargs 'ADD_CMAKE_TO_PATH=System'", '-y'])

            if success:
                print(f"cmake installed via Chocolatey: {output}")

            success, output = self._run_command(['choco', 'install', 'visualstudio2022buildtools', '-y'])

            if success:
                print(f"C++ installed via Chocolatey: {output}")

            return success
            
        elif system == "Darwin":
            success, output = self._run_command(['brew', 'install', 'make', 'cmake', 'gcc'])
            if success:
                print("gmake installed via Homebrew")
            return success
            
        else:
            if shutil.which('apt'):
                success, output = self._run_command(['sudo', 'apt', 'update'])
                success, output = self._run_command(['sudo', 'apt', 'install', '-y', 'make', 'cmake', 'g++'])
            else:
                print("No supported package manager found for make installation")
                return False
            
            if success:
                print("make installed via package manager")

            return success
    
    def install_dotnet_sdk_8(self) -> bool:
        """
        Install .NET SDK 8
        
        Returns:
            bool: True if installation successful
        """
        system: str = self.system_info['os']
        print("Installing .NET SDK 8...")

        success: bool
        output: str
        
        commands: List[List[str]]

        if system == "Windows":
            success, output = self._run_command(['choco', 'install', 'dotnet-8.0-sdk', '-y'])

            if success:
                print(".NET SDK 8 installed via Chocolatey")

            return success
            
        elif system == "Darwin":
            success, output = self._run_command(['brew', 'install', '--cask', 'dotnet-sdk'])

            if success:
                print(".NET SDK 8 installed via Homebrew")

            return success
            
        else:
            if shutil.which('apt'):
                commands = [
                    ['wget', 'https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb', '-O', '/tmp/packages-microsoft-prod.deb'],
                    ['sudo', 'dpkg', '-i', '/tmp/packages-microsoft-prod.deb'],
                    ['sudo', 'apt', 'update'],
                    ['sudo', 'apt', 'install', '-y', 'dotnet-sdk-8.0'],
                ]
            else:
                print("Unsupported Linux distribution for .NET SDK installation")
                return False
            
            for cmd in commands:
                success, output = self._run_command(cmd)
                if not success:
                    print(f".NET SDK installation failed: {output}")
                    return False
            
            print(".NET SDK 8 installed")
            return True
    
    def move_executables_to_app_dir(self) -> bool:
        """
        Move executables to application directory
        
        Returns:
            bool: True if successful
        """
        print("Moving executables to app directory...")
        
        source_dir: Path = get_executable_path() / "SNES-IDE"
        dest_dir: Path = self.app_dir
        
        try:
            if source_dir.exists():

                if dest_dir.exists():
                    shutil.rmtree(dest_dir)

                os.makedirs(dest_dir.parent, exist_ok=True)
                shutil.copytree(source_dir, dest_dir)
                print(f"Executables moved to: {dest_dir}")

                return True

            else:

                print("No executables found to move")
                return True
                
        except Exception as e:

            print(f"Failed to move executables: {str(e)}")
            return False
    
    def install_jdk_8_with_fx(self) -> bool:
        """
        Install JDK 8 with JavaFX
        
        Returns:
            bool: True if installation successful
        """

        print("Installing JDK 8 with JavaFX...")
        
        self.zip_extractor: LZMAZipExtractor

        jdk_path: Path = Path(
            self.app_dir / "bin" / "jdk8" / "jdk8.zip"
        )

        out_path: str = self.zip_extractor.extract_zip(
            zip_path=jdk_path,
            extract_to=jdk_path.parent,
            create_subdir=False
        )

        os.unlink(jdk_path)
        
        if self.system_info['os'].lower() == 'linux':
            
            self._run_command(["chmod", "-R", "+x", out_path])
        
        return True
    
    def run_install_scripts(self) -> bool:
        """
        Run required installation scripts
        
        Returns:
            bool: True if all scripts successful
        """

        print("Running installation scripts...")
        
        if self.system_info['os'].lower() == 'linux':

            schism_installer_path: Path = self.app_dir / "bin" / "schismtracker" / "install.sh"

            if not schism_installer_path.exists():
                return False
            
            if not self._run_command([str(schism_installer_path)], shell=True)[0]:
                return False
            
            if not self._run_command(["chmod", "-R", "+x", str(schism_installer_path.parent)], shell=True)[0]:
                return False

            sprite_editor: Path = self.app_dir / "bin" / "sprite-editor"
            if not sprite_editor.exists():
                return False
            
            if not self._run_command(["chmod", "-R", "+x", str(sprite_editor)], shell=True)[0]:
                return False

            tmx_editor: Path = self.app_dir / "bin" / "tmx-editor"
            if not tmx_editor.exists():
                return False
                
            if not self._run_command(["chmod", "-R", "+x", str(tmx_editor)], shell=True)[0]:
                return False

        elif os.name == "nt":

            if not self._run_command(["choco", "install", "tiled", "--version=1.9.2", "-y"], shell=True)[0]:
                return False
               
        return True

    def create_shortcut(self) -> bool:
        """
        Create desktop shortcut (Windows) or .desktop file (Linux) or symlink (macOS)
        
        Returns:
            bool: True if shortcut creation successful
        """
        print("Creating shortcut...")
        
        system: str = self.system_info['os']
        main_executable: Path = self.app_dir / f"{self.app_name.lower()}.exe" if system == "Windows" else self.app_dir / "bin" / self.app_name.lower()
        
        success: bool
        _: str

        if not main_executable.exists():
            print(f"Main executable not found: {main_executable}")
            return False
        
        if system.lower() == "windows":
            shortcut_path: Path = self.desktop_dir / f"{self.app_name}.lnk"
            
            ps_script: str = f"""
            $WshShell = New-Object -comObject WScript.Shell
            $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
            $Shortcut.TargetPath = "{main_executable}"
            $Shortcut.WorkingDirectory = "{self.app_dir}"
            $Shortcut.IconLocation = "{self.app_dir / "icon.ico"}"
            $Shortcut.Description = "{self.app_name} Application"
            $Shortcut.Save()
            """
            
            success, _ = self._run_command(['powershell', '-Command', ps_script])
            if success:
                print(f"Windows shortcut created: {shortcut_path}")
            return success
            
        elif system.lower() == "darwin":
            apps_dir: Path = Path("/Applications")
            app_link: Path = apps_dir / f"{self.app_name}.app"
            
            try:

                if app_link.exists():
                    app_link.unlink()
                
                app_link.symlink_to(self.app_dir)
                print(f"macOS application link created: {app_link}")

                return True

            except Exception as e:

                print(f"Failed to create macOS shortcut: {str(e)}")
                return False
                
        else:
            desktop_file: Path = self.desktop_dir / f"{self.app_name}.desktop"
            desktop_content: str = f"""[Desktop Entry]
Version={self.app_version}
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
                
                desktop_file.chmod(desktop_file.stat().st_mode | stat.S_IEXEC)
                
                bin_link: Path = Path("/usr/local/bin") / self.app_name.lower()

                if bin_link.exists():
                    bin_link.unlink()

                bin_link.symlink_to(main_executable)
                
                print(f"Linux .desktop file created: {desktop_file}")
                return True
                
            except Exception as e:
                print(f"Failed to create Linux shortcut: {str(e)}")
                return False
    
    @staticmethod
    def check_if_path(program: str) -> bool:
        """
        Check if a program is available in the system PATH.
    
        Args:
            program (str): The name of the program to check (e.g., 'make', 'tiled')
        
        Returns:
            bool: True if the program is found in PATH, False otherwise
        """
        return shutil.which(program) is not None

    def verify_installation(self) -> bool:
        """
        Verify that installation was successful
        
        Returns:
            bool: True if verification passed
        """
        print("Verifying installation...")
        
        checks: List[Tuple[str,bool]] = []
        success: bool
        output: str
        
        checks.append(("App directory", self.app_dir.exists() and any(self.app_dir.iterdir())))
        
        system: str = self.system_info['os']
        main_executable: Path = self.app_dir / f"{self.app_name.lower()}.exe" if system == "Windows" else self.app_dir / "bin" / self.app_name.lower()
        checks.append(("Main executable", main_executable.exists()))
        
        success, output = self._run_command(['dotnet', '--version'])
        checks.append((".NET SDK", success and '8.' in output))
        
        make_cmd: "Literal['gmake']|Literal['make']" = 'gmake' if system == "Darwin" else 'make'
        success, output = self._run_command([make_cmd, '--version'])
        checks.append(("Make tool", success))

        tiled_cmd: Literal['tiled'] = 'tiled'
        if os.name == "nt":
            success, output = self._run_command([tiled_cmd, '--version'])
        else:
            success = True
        checks.append(("Tiled tool", success))

        schism_cmd: Literal['schismtracker'] = 'schismtracker'
        if system.lower() == "linux":
            success = self.check_if_path(schism_cmd)
        else:
            success = True
        checks.append(("Schimstracker tool", success))
        
        jdk_dir: Path = self.app_dir / "bin" / "jdk8"

        if jdk_dir.exists():
            java_exec: Path = jdk_dir / "bin" / "java"

            if system == "Darwin":
                java_exec = jdk_dir / "Contents/Home/bin/java"
            
            success, output = self._run_command([str(java_exec), '-version'])
            checks.append(("Java Runtime", success))
        
        all_passed: bool = True
        for check_name, passed in checks:
            status: Literal['PASS', 'FAIL'] = "PASS" if passed else "FAIL"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("Installation verification successful!")

        else:
            print("Some installation checks failed")
        
        return all_passed
    
    def cleanup_temp_files(self) -> bool:
        """
        Clean up temporary installation files
        
        Returns:
            bool: True if cleanup successful
        """
        print("Cleaning up temporary files...")
        
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)

            print("Temporary files cleaned up")
            return True

        except Exception as e:
            print(f"Failed to clean up temp files: {str(e)}")
            return False


def check_if_admin() -> bool:
    """Check if the script is being executed by an admin user."""

    if os.name == "posix":
        return os.getuid() == 0
    
    else:

        try:
            return ctypes.windll.shell32.IsUserAnAdmin()

        except Exception as e:
            print(f"Error while checking if user is admin: {e}")
            return False


def get_executable_path() -> Path:
    """Get the path of the executable or script based on whether the script is frozen 
    (PyInstaller) or not."""

    if getattr(sys, 'frozen', False):
        print("executable path mode chosen")
        return Path(sys.executable).resolve().parent
        
    else:
        print("Python script path mode chosen")
        return Path(__file__).resolve().parent


def install(
    ws: WebSocketManager, zip_extractor: LZMAZipExtractor, local_dir: Path
) -> "Literal[True]|Tuple[Literal[False], str]":
    """
    Execute all installation steps
        
    Returns:
        bool: True if all steps successful
    """

    installer: ApplicationInstaller = ApplicationInstaller(
        app_version="5.0.0", local_dir=local_dir, zip_extractor=zip_extractor,
        app_name="SNES-IDE"
    )

    print(f"Starting {installer.app_name} installation...")
    print(f"Install directory: {installer.app_dir}")
    print(f"Platform: {installer.system_info['os']} {installer.system_info['architecture']}")
    print()
        
    installation_steps: List[Tuple[str, Callable[..., bool]]] = [
        ("Installing make", installer.install_make_cmake_gpp),
        ("Installing .NET SDK 8", installer.install_dotnet_sdk_8),
        ("Moving executables", installer.move_executables_to_app_dir),
        ("Installing JDK 8 with JavaFX", installer.install_jdk_8_with_fx),
        ("Running install scripts", installer.run_install_scripts),
        ("Creating shortcut", installer.create_shortcut),
        ("Verifying installation", installer.verify_installation),
        ("Cleaning up", installer.cleanup_temp_files),
    ]
        
    for step_name, step_function in installation_steps:
        print(f"\n{'='*50}")
        print(f"Step: {step_name}")
        print(f"{'='*50}")
        ws.send_message(step_name)
            
        if not step_function():
            return False, f"Instalation of SNES-IDE failed in step: {step_name}"
            
    print(f"\n{'='*50}")
    print(f"{installer.app_name} installation completed successfully!")
    print(f"Location: {installer.app_dir}")
    print(f"{'='*50}")
        
    return True


def main() -> None:
    """Main Logic of the INSTALL application"""
    app: "None|PyQtWebApp" = None
    temp_dir: "str|None" = None
    ws: "WebSocketManager|None" = None

    if not check_if_admin():
        print("Error: Administrator privileges required")
        exit(-1)
        
    if os.name == 'posix':
        try:
            subprocess.run(
                ["chmod", "-R", "+x", "./SNES-IDE"],
                shell=False, check=True, cwd=get_executable_path()
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to set permissions: {e}")

    checker: SystemRequirementsChecker = SystemRequirementsChecker()
    print("System Requirements Checker")
    print("=" * 30)

    requirements_met: bool = checker.check_all_requirements()
    
    zip_extractor: LZMAZipExtractor = LZMAZipExtractor()
    ws = WebSocketManager()
    
    try:
        ws.start()
        print("WebSocket server started")

        temp_dir = tempfile.mkdtemp(prefix="snes_ide_installer_")
        print(f"Created temp directory: {temp_dir}")

        web_path: str = zip_extractor.extract_zip(
            get_executable_path() / "gui" / "installer-gui.zip", 
            temp_dir, 
            create_subdir=True
        )
        print(f"Web interface extracted to: {web_path}")

        if not requirements_met:
            print("System requirements not met")
            checker.show_error_dialog()
            time.sleep(5)
            exit(-1)

        app = PyQtWebApp(
            str(Path(web_path) / "installer-gui"), 
            window_title="SNES-IDE Installer"
        )
        app.start()
        app.show()
        print("PyQt application started")

        print("Waiting for WebSocket connection...")
        max_wait_seconds: int = 30
        wait_interval: float = 0.5
        max_attempts = int(max_wait_seconds / wait_interval)
        
        connected = False
        for attempt in range(max_attempts):
            if ws.get_connection_count() > 0:
                connected = True
                print("WebSocket client connected")
                break
            time.sleep(wait_interval)
            
            if attempt % 10 == 0:
                elapsed = attempt * wait_interval
                print(f"Still waiting... ({elapsed:.1f}s / {max_wait_seconds}s)")

        if not connected:
            print("Timeout: No WebSocket connection established")
            ws.stop_with_error("Connection timeout - no client connected")
            exit(-1)

        print("Starting installation process...")
        return_install: "Tuple[Literal[False], str] | Literal[True]"
        return_install = install(ws, zip_extractor, get_executable_path())
        
        if return_install != True:
            error_msg = return_install[1]
            print(f"Installation failed: {error_msg}")
            ws.stop_with_error(error_msg)
            exit(-1)
            
        else:
            print("Installation completed successfully")
            ws.send_message("Installation completed successfully")
            time.sleep(3)

    except Exception as e:
        print(f"Critical error during installation: {e}")
        if ws:
            try:
                ws.stop_with_error(f"Unexpected error: {str(e)}")
            except:
                pass
        try:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("Installation Error")
            msg_box.setText(f"An unexpected error occurred:\n{str(e)}")
            msg_box.exec()
        except:
            print("Could not display error dialog")

    finally:
        print("Cleaning up resources...")
        
        try:
            if app:
                print("Closing application...")
                app.close()
        except Exception as e:
            print(f"Error closing application: {e}")
        
        try:
            if ws:
                print("Stopping WebSocket...")
                ws.stop()
        except Exception as e:
            print(f"Error stopping WebSocket: {e}")
        
        try:
            if temp_dir and os.path.exists(temp_dir):
                print(f"Cleaning temp directory: {temp_dir}")
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            print(f"Error cleaning temp directory: {e}")
        
        print("Cleanup completed")

if __name__ == "__main__":
    main()

