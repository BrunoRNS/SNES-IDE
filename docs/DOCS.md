# SNES-IDE Technical Documentation

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [Build System](#build-system)
4. [Project Structure](#project-structure)
5. [Development Workflow](#development-workflow)
6. [Internal Mechanisms](#internal-mechanisms)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)

## Architecture Overview

SNES-IDE is built as a cross-platform desktop application using a hybrid architecture:

```yml
┌─────────────────────────────────────────────────┐
│                  Frontend Layer                 │
│  HTML/CSS/JavaScript (QWebEngineView)           │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│                Bridge Layer                     │
│  QWebChannel ↔ Python Communication             │
└─────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│                Backend Layer                    │
│  Python (PySide6) + Toolchain Integration       │
└─────────────────────────────────────────────────┘
```

### Core Technologies

- **Frontend**: HTML5, CSS3, JavaScript with custom SNES-themed UI
- **Bridge**: Qt WebChannel for JavaScript-Python communication
- **Backend**: Python 3.11+ with PySide6 for GUI
- **Build System**: Custom Python-based build automation
- **Toolchain Integration**: Multiple SNES development toolchains

## Core Components

### 1. Main Application (`snes-ide.py`)

The main entry point that initializes the IDE:

```python
class MainWindow(QMainWindow):
    def __init__(self):
        # Initialize Qt WebEngine with QWebChannel
        self.web_view = QWebEngineView()
        self.channel = QWebChannel()
        self.script_runner = ScriptRunner()
        self.channel.registerObject("scriptRunner", self.script_runner)
```

**Key Responsibilities:**

- Application window management
- WebEngine initialization and configuration
- WebChannel setup for JS-Python communication
- Resource loading and path resolution

### 2. Script Runner (`ScriptRunner` class)

Handles execution of IDE operations through Python scripts:

```python
class ScriptRunner(QObject):
    scriptExecuted = Signal(str, str)
    
    @Slot(str)
    def run_script(self, script_name: str):
        # Executes Python scripts from the scripts directory
        # Manages subprocess creation and output handling
```

**Features:**

- Asynchronous script execution via QProcess
- Real-time output capture (stdout/stderr)
- Error handling and status reporting
- Cross-platform process management

### 3. Build System (`build.py`)

Comprehensive build automation with multiple stages:

```python
def main():
    steps = [
        ("Cleaning SNES-IDE-out", clean_all),
        ("Restoring big files", restore_big_files),
        ("Copying root files", copy_root),
        ("Copying libs", copy_lib),
        # ... more build steps
    ]
```

**Build Pipeline:**

1. **Clean**: Remove previous build artifacts
2. **File Reconstruction**: Join chunked files using manifests
3. **Resource Copying**: Copy libraries, binaries, documentation
4. **Bundle Generation**: Create platform-specific distributions

### 4. Bundle Creator (`create_bundle.py`)

Platform-specific application packaging:

```python
class BundleCreator:
    def create_bundle(self):
        if self.current_platform == "windows":
            return self._create_windows_bundle()
        elif self.current_platform == "darwin":
            return self._create_macos_bundle()
        elif self.current_platform == "linux":
            return self._create_linux_bundle()
```

## Build System

### File Reconstruction System

SNES-IDE uses a sophisticated file chunking system for large binaries:

```python
class FileJoiner:
    def join(self) -> bool:
        # 1. Load reconstruction manifest
        # 2. Verify chunk integrity
        # 3. Reconstruct original file
        # 4. Validate checksum
```

**Manifest Structure:**

```json
{
    "original_filename": "large_file.bin",
    "total_size": 104857600,
    "checksum": "md5_hash",
    "chunks": [
        {
            "index": 0,
            "filename": "large_file.bin.chunk.001",
            "size": 1048576,
            "start_byte": 0,
            "end_byte": 1048575
        }
    ]
}
```

### Platform-Specific Builds

#### Windows Bundle

- Creates virtual environment in `venv/`
- Compiles C++ launcher (`SNES-IDE.cpp`)
- Packages with all dependencies

#### macOS Bundle

- Creates `.app` bundle structure
- Sets up proper macOS application hierarchy
- Configures Info.plist and permissions

#### Linux Bundle

- Creates AppDir structure
- Sets up desktop integration
- Configures environment variables

## Project Structure

### Source Organization

```yml
src/
├── snes-ide.py              # Main application
├── scripts/                 # IDE operation scripts
│   ├── create-*-proj.py    # Project creation
│   ├── *-converter.py      # Asset conversion
│   └── open-emulator.py    # Emulator integration
└── assets/                 # Web UI resources
```

### Resource Management

```yml
resources/
├── bin/                    # Platform-specific binaries
│   ├── windows/
│   ├── macos/
│   └── linux/
├── libs/                   # Development libraries
│   ├── pvsneslib/
│   ├── DotnetSnesLib/
│   └── javasnes/
└── [chunked files]         # Large files split into chunks
```

## Development Workflow

### 1. Project Creation

**C/PVSnesLib Projects:**

- Copies template from pvsneslib/template
- Validates project name and path
- Sets up build configuration

**C#/DotnetSnes Projects:**

- Uses DotnetSnes template structure
- Configures C# project files
- Sets up .NET-specific build chain

**Java/JavaSnes Projects:**

- Uses JavaSnes template
- Configures Java build environment
- Sets up JVM dependencies

### 2. Build Process

**Multi-language Support:**

- **C**: Uses 816-tcc and wla-dx compilers
- **Assembly**: WLA-DX assembler for 65816
- **C#**: Dntc compiler from DotnetSnes
- **Java**: JavaSnes framework

**Output Management:**

- ROM file generation (.sfc format)
- Debug symbol generation
- Asset embedding

## Internal Mechanisms

### 1. Cross-Platform Path Handling

```python
def get_executable_path() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    else:
        return Path(__file__).resolve().parent
```

### 2. Process Management

```python
def run_script(self, script_name: str):
    self.process = QProcess()
    self.process.readyReadStandardOutput.connect(self.handle_stdout)
    self.process.readyReadStandardError.connect(self.handle_stderr)
    self.process.finished.connect(self.handle_finished)
```

### 3. Environment Configuration

**Platform Detection:**

```python
system = platform.system().lower()
if system == 'darwin':
    system = 'macos'
```

**Toolchain Setup:**

- Sets `PVSNESLIB_HOME` environment variable
- Configures compiler paths
- Manages emulator executables

### 4. Error Handling

**Comprehensive Error Reporting:**

- Script execution status via signals
- Process exit code analysis
- Standard error capture and display

## API Reference

### JavaScript → Python Bridge

**Available Methods:**

```javascript
scriptRunner.runScript(scriptName);

scriptRunner.scriptExecuted.connect(function(script, result) {
    console.log(script + ": " + result);
});
```

### Script Runner API

**Public Methods:**

- `run_script(script_name: str)`: Execute script by name
- `runScript(scriptName: str)`: JavaScript-compatible alias

**Signals:**

- `scriptExecuted(str, str)`: Emits (script_name, result)

### Available Scripts

**Project Management:**

- `create-pvsneslib-proj.py`: C project creation
- `create-dotnetsnes-proj.py`: C# project creation  
- `create-javasnes-proj.py`: Java project creation

**Asset Processing:**

- `gfx-tmx-tmj-converter.py`: Tilemap conversion
- `audio-wav-brr-converter.py`: Audio conversion
- `audio-sample-generator.py`: Sample generation

**Development Tools:**

- `open-emulator.py`: ROM testing
- Various build and utility scripts

## Troubleshooting

### Common Issues

#### 1. Script Execution Failures

```python
script_path = self.scripts_dir / script_name
if script_path.exists():
```

#### 2. File Reconstruction Issues

- Verify chunk manifest integrity
- Check available disk space
- Validate MD5 checksums

#### 3. Platform-Specific Problems

**Windows:**

- Ensure Visual C++ Redistributables
- Check antivirus interference

**macOS:**

- Gatekeeper permissions
- App notarization requirements

**Linux:**

- Library dependencies (glibc version)
- Desktop integration

### Debug Mode

Enable verbose logging by setting environment variables:

```bash
export QT_DEBUG_PLUGINS=1
export QTWEBENGINE_CHROMIUM_FLAGS="--enable-logging --v=1"
```

### Performance Optimization

**Memory Management:**

- Chunked file loading for large assets
- Lazy loading of toolchain components
- Process isolation for resource-intensive operations

**Build Optimization:**

- Incremental build support
- Parallel compilation where possible
- Cache intermediate build artifacts

## Extension Development

### Adding New Scripts

1. Place Python script in `src/scripts/`
2. Ensure proper error handling and output
3. Update web interface to expose new functionality
4. Add to build system if required

### Custom Toolchain Integration

1. Place binaries in `resources/bin/<platform>/`
2. Update environment configuration
3. Create appropriate project templates
4. Add build support in relevant scripts
