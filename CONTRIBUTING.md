# SNES-IDE — Developer Introduction

This document will help you get started as a developer.

## 🚀 Project Overview

SNES-IDE is a development environment for SNES homebrew. The project includes tools, libraries, and documentation for SNES development.

## Repository Structure

- `.github/` — Automated workflows and tests.
- `build/` — Build scripts and automation.
- `docs/` — Documentation and examples.
- `gh-pages/` — Github-pages documentation.
- `installer/` — Installation scripts and automation.
- `resources/bin/<os>` — SNES-IDE development OS specifics binaries.
- `resources/libs/` — SNES development libraries.
- `src/` — Main source of SNES-IDE.
- `src/scripts/` — Scripts used by the source.
- `CODE_OF_CONDUCT.md` — Contributor guidelines.

## Building SNES-IDE

### Local Build (Windows)

1. Install [Python 3.13+](https://www.python.org/downloads/windows/)
2. Install Dependencies:  

   ```sh
   pip install -r build\requirements.txt
   ```

3. Run the build script:

   ```sh
   python build\build.py
   ```

4. Output will be in `SNES-IDE-out/`

### Local Build (UNIX)

1. Install [Python 3.13+](https://www.python.org/downloads/)
2. Install Dependencies:

   ```sh
   pip3 install -r ./build/requirements.txt
   ```

3. Run the build script:

   ```sh
   python3 ./build/build.py
   ```

4. Output will be in `SNES-IDE-out/`

## Testing

### Build Tests

[![Build (Green Light)](https://github.com/BrunoRNS/SNES-IDE/actions/workflows/Windows.yml/badge.svg?branch=windows%2Fci)](https://github.com/BrunoRNS/SNES-IDE/actions/workflows/Windows.yml)

- These should never be failing. If they do, fix the build until red
status is green and then move them.

### Green-Light Tests

[![Tests (Green Light)](https://github.com/BrunoRNS/SNES-IDE/actions/workflows/Windows.yml/badge.svg?branch=windows%2Fgreen)](https://github.com/BrunoRNS/SNES-IDE/actions/workflows/Windows.yml)

- Run automatically in CI after each build.
- Check for presence of key libraries and executables.
- Example:  
  - `libs/javasnes`, `libs/pvsneslib`, `bin/jdk8`, etc.

### Red-Light Tests

[![Tests (Red Light)](https://github.com/BrunoRNS/SNES-IDE/actions/workflows/Windows.yml/badge.svg?branch=windows%2Fred)](https://github.com/BrunoRNS/SNES-IDE/actions/workflows/Windows.yml)

- Only run on the `<os>/red` branch.
- Used for TDD: write failing tests before implementing new features.

## Contributing

- Fork the repo and create a feature branch (`<os>/feature-xyz`)
- Write tests first (Red-Light), then implement features until tests pass (Green-Light). These should be in the appropriate workflow section.
- Submit pull requests to `devel`
- See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community guidelines

## Documentation & Resources

- [docs/](docs/) — Examples and guides
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Contributor guidelines

- Open an issue for bugs or feature requests!
