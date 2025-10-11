import os
import sys
import platform
import subprocess
from pathlib import Path

class JarRunner:
    """
    Cross-platform JAR executor using a local JDK installation.
    Handles Windows, Linux, and macOS (including .app bundles).
    """
    
    def __init__(self, jdk_folder="jdk8", jar_file=None):
        # Get the directory where this script is located
        self.current_dir = Path(__file__).parent
        # JDK directory path (relative to script location)
        self.jdk_dir = self.current_dir / jdk_folder
        # JAR file to execute (auto-detected if not specified)
        self.jar_file = jar_file or self._find_jar_file()
        
    def _find_jar_file(self) -> Path:
        """
        Automatically find JAR files in the project root directory.
        
        Returns:
            Path to the first JAR file found
            
        Raises:
            FileNotFoundError: If no JAR files are found in the root directory
        """
        # Find all .jar files in the current directory
        jar_files = list(self.current_dir.glob("*.jar"))
        
        if not jar_files:
            raise FileNotFoundError("No JAR files found in project root directory")
        
        # If multiple JARs found, use the first one and show warning
        if len(jar_files) > 1:
            print("⚠️  Multiple JAR files found. Using the first one:")
            for jar in jar_files:
                print(f"   - {jar.name}")
        
        return jar_files[0]
    
    def _find_java_executable(self) -> Path:
        """
        Locate the Java executable within the JDK directory structure.
        Handles different platform-specific layouts including macOS .app bundles.
        
        Returns:
            Path to the Java executable
            
        Raises:
            FileNotFoundError: If no Java executable is found in the JDK directory
        """
        system = platform.system().lower()
        
        # Platform-specific Java executable paths
        if system == "windows":
            # Windows: standard JDK structure
            java_path = self.jdk_dir / "bin" / "java.exe"
            # Alternative: some installations might have JRE separately
            if not java_path.exists():
                java_path = self.jdk_dir / "jre" / "bin" / "java.exe"
                
        elif system == "darwin":  # macOS
            # macOS has multiple possible structures:
            
            # 1. Standard JDK folder structure (like Linux)
            java_path = self.jdk_dir / "bin" / "java"
            
            # 2. .app bundle structure (common for downloaded JDKs)
            if not java_path.exists():
                java_path = self.jdk_dir / "Contents" / "Home" / "bin" / "java"
            
            # 3. Look for .app files in the JDK directory
            if not java_path.exists():
                app_bundles = list(self.jdk_dir.glob("*.app"))
                if app_bundles:
                    # Use the first .app bundle found
                    app_path = app_bundles[0]
                    java_path = app_path / "Contents" / "Home" / "bin" / "java"
                    
        else:  # Linux and other Unix-like systems
            # Standard Linux JDK structure
            java_path = self.jdk_dir / "bin" / "java"
            # Alternative: JRE subdirectory
            if not java_path.exists():
                java_path = self.jdk_dir / "jre" / "bin" / "java"
        
        # If standard paths don't work, search recursively through the directory
        if not java_path.exists():
            java_executable_name = "java.exe" if system == "windows" else "java"
            
            for java_exe in self.jdk_dir.rglob(java_executable_name):
                if java_exe.is_file():
                    # On Unix-like systems, check if the file is executable
                    if system != "windows":
                        if not os.access(java_exe, os.X_OK):
                            continue
                    return java_exe
            
            # If we still haven't found it, raise an error
            raise FileNotFoundError(
                f"Java executable not found in: {self.jdk_dir}\n"
                f"Directory structure:\n{self._print_directory_structure()}"
            )
        
        return java_path
    
    def _print_directory_structure(self, max_depth=3) -> str:
        """
        Print directory structure for debugging purposes.
        
        Args:
            max_depth: Maximum depth to display in the tree
            
        Returns:
            String representation of the directory structure
        """
        structure = []
        for root, dirs, files in os.walk(self.jdk_dir):
            # Calculate indentation level based on directory depth
            level = root.replace(str(self.jdk_dir), '').count(os.sep)
            if level <= max_depth:
                indent = '  ' * level
                structure.append(f"{indent}{os.path.basename(root)}/")
                # Only show files if we're not at maximum depth
                if level < max_depth:
                    for file in files[:10]:  # Limit to 10 files per directory
                        structure.append(f"{indent}  {file}")
        return '\n'.join(structure)
    
    def _check_java_version(self, java_executable: Path) -> bool:
        """
        Verify that the found Java executable is version 8 (or compatible).
        
        Args:
            java_executable: Path to the Java executable to check
            
        Returns:
            True if Java is found and appears to be version 8, False otherwise
        """
        try:
            # Run java -version to get version information
            result = subprocess.run(
                [str(java_executable), "-version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # Version info is typically in stderr for java -version
            version_output = result.stderr or result.stdout
            
            # Check for Java 8 indicators
            if "1.8" in version_output or "8" in version_output:
                version_line = version_output.splitlines()[0] if version_output else "Unknown version"
                print(f"✅ JDK 8 found: {version_line}")
                return True
            else:
                version_line = version_output.splitlines()[0] if version_output else "Cannot determine version"
                print(f"⚠️  Warning: Found Java doesn't appear to be version 8:")
                print(f"   {version_line}")
                # Continue execution anyway - might be compatible
                return True
                
        except subprocess.TimeoutExpired:
            print("⚠️  Timeout while checking Java version")
            return True
        except Exception as e:
            print(f"⚠️  Error checking Java version: {e}")
            return True
    
    def run_jar(self, jar_args=None, jvm_args=None) -> bool:
        """
        Execute the JAR file using the local JDK installation.
        
        Args:
            jar_args: List of arguments to pass to the JAR application
            jvm_args: List of JVM arguments (e.g., memory settings)
            
        Returns:
            True if execution was successful, False otherwise
        """
        try:
            # Verify JDK directory exists
            if not self.jdk_dir.exists():
                raise FileNotFoundError(f"JDK directory not found: {self.jdk_dir}")
            
            # Verify JAR file exists
            if not self.jar_file.exists():
                raise FileNotFoundError(f"JAR file not found: {self.jar_file}")
            
            # Find the Java executable
            java_executable = self._find_java_executable()
            print(f"🔍 Java executable found: {java_executable}")
            
            # Optional: Check Java version
            self._check_java_version(java_executable)
            
            # Prepare arguments (use empty lists if None)
            if jvm_args is None:
                jvm_args = []
            if jar_args is None:
                jar_args = []
            
            # Build the complete command
            command = [str(java_executable)] + jvm_args + ["-jar", str(self.jar_file)] + jar_args
            
            print(f"🚀 Executing: {' '.join(command)}")
            print(f"📂 Working directory: {self.current_dir}")
            print("-" * 50)
            
            # Execute the JAR file
            process: CompletedProcess[bytes] = subprocess.run(
                command,
                cwd=self.current_dir,  # Run from project root directory
                check=False  # Don't automatically raise exception on non-zero exit
            )
            
            print("-" * 50)
            if process.returncode == 0:
                print("✅ JAR executed successfully!")
            else:
                print(f"❌ JAR returned error code: {process.returncode}")
            
            return process.returncode == 0
            
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False

def main() -> NoReturn:
    """
    Main function with command-line argument parsing.
    Provides a user-friendly interface for running JAR files.
    """
    import argparse
    
    parser: ArgumentParser = argparse.ArgumentParser(description='Execute JAR using local JDK installation')
    parser.add_argument('--jdk-dir', default='jdk8', 
                       help='JDK directory name (default: jdk8)')
    parser.add_argument('--jar-file', 
                       help='Specific JAR file to execute (default: first .jar in root)')
    parser.add_argument('--jvm-args', nargs='*', 
                       help='JVM arguments (e.g., -Xmx512m -Dproperty=value)')
    parser.add_argument('jar_args', nargs='*', 
                       help='Arguments to pass to the JAR application')
    
    args: Namespace = parser.parse_args()
    
    try:
        # Create runner instance with specified parameters
        runner: JarRunner = JarRunner(jdk_folder=args.jdk_dir, jar_file=args.jar_file)
        # Execute the JAR and exit with appropriate code
        success: bool = runner.run_jar(jar_args=args.jar_args, jvm_args=args.jvm_args)
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ Critical failure: {e}")
        sys.exit(1)

def run_simple(jdk_folder="jdk8", jar_file=None, jar_args=None, jvm_args=None):
    """
    Simplified function for programmatic JAR execution.
    
    Args:
        jdk_folder: Name of the JDK directory
        jar_file: Specific JAR file to execute
        jar_args: Arguments for the JAR application
        jvm_args: JVM arguments
        
    Returns:
        True if execution was successful, False otherwise
        
    Example:
        success = run_simple(jdk_folder="jdk8", jar_args=["--help"])
    """
    runner: JarRunner = JarRunner(jdk_folder, jar_file)
    return runner.run_jar(jar_args, jvm_args)

if __name__ == "__main__":
    # Entry point when script is executed directly
    main()