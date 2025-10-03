# SNES-IDE — Developer Introduction

This document will help you get started as a developer.

---

## 🚀 Project Overview

SNES-IDE is a development environment for SNES homebrew. The project includes tools, libraries, and documentation for SNES development.

---

## Repository Structure

- `build/` — Build scripts and automation
- `docs/` — Documentation and examples
- `libs/` — SNES development libraries
- `tools/` — SNES-IDE tools and utilities
- `tests/` — Automated tests
- `build-requirements.txt` — Python dependencies for building
- `INSTALL.md` — Installation instructions
- `dependencies.md` — Third-party libraries and tools
- `CODE_OF_CONDUCT.md` — Contributor guidelines

---

## Building SNES-IDE

### Local Build (Windows)

1. Install [Python 3.13+](https://www.python.org/downloads/windows/)
2. Install [PyInstaller](https://pyinstaller.org/):  
   ```
   pip install pyinstaller
   ```
3. Run the build script:
   ```
   python build\build.py
   ```
4. Output will be in `SNES-IDE-out/`

---

## Testing

### Build Tests

[![Build (Green Light)](https://github.com/BrunoRNS/SNES-IDE/actions/workflows/Windows.yml/badge.svg?branch=windows%2Fci)](https://github.com/Atomic-Germ/SNES-IDE/actions/workflows/Windows.yml)

- These should never be failing. If they do, fix the build until red
status is green and then move them.

### Green-Light Tests

[![Tests (Green Light)](https://github.com/BrunoRNS/SNES-IDE/actions/workflows/Windows.yml/badge.svg?branch=windows%2Fgreen)](https://github.com/BrunoRNS/SNES-IDE/actions/workflows/Windows.yml)

- Run automatically in CI after each build.
- Check for presence of key libraries and executables.
- Example:  
  - `libs/bsnes`, `libs/font`, `tools/snes-ide.exe`, etc.

### Red-Light Tests

[![Tests (Red Light)](https://github.com/BrunoRNS/SNES-IDE/actions/workflows/Windows.yml/badge.svg?branch=windows%2Fred)](https://github.com/BrunoRNS/SNES-IDE/actions/workflows/Windows.yml)

- Only run on the `windows/red` branch.
- Used for TDD: write failing tests before implementing new features.

## Contributing

- Fork the repo and create a feature branch (`<os>/feature-xyz`)
- Write tests first (Red-Light), then implement features until tests pass (Green-Light). These should be in the appropriate workflow section.
- Submit pull requests to `devel`
- See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community guidelines

---

## Documentation & Resources

- [docs/](docs/) — Examples and guides
- [dependencies.md](dependencies.md) — Third-party libraries and tools
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Contributor guidelines

---

- Open an issue for bugs or feature requests!