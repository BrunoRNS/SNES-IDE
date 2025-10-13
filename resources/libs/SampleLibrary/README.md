# SampleGenerator

SampleGenerator is a cross-language toolchain for generating lightweight audio samples (WAV and MIDI) suitable for use with the SNES SPC700 sound processor. It automates the creation, validation, and playback of simple musical notes and waveforms, making it easier to produce and test samples for retro game development or hardware emulation.

## Project Goal

The main goal of SampleGenerator is to generate minimalistic audio samples (MIDI and WAV) that are compatible with the technical constraints of the SNES SPC700 processor. This includes:

- **Low sample rate (800 Hz)**
- **8-bit unsigned PCM WAV files**
- **Simple waveforms (square, triangle, sine)**
- **Single-note MIDI files for conversion**

This toolchain helps composers, developers, and enthusiasts quickly create and validate samples for SNES music and sound effects.

## Features

- Automatic MIDI note generation (Python)
- Conversion of MIDI notes to WAV files (Julia)
- Custom RIFF header construction for WAV files
- Waveform synthesis: square, triangle, sine
- Validation of WAV files for SPC700 compatibility
- Playback of generated samples for quick testing
- Cross-language build and test automation via Makefile

## Directory Structure

```sh
SampleGenerator/
├── midi-samples/           # Generated MIDI files
├── wave-samples/           # Generated WAV files
├── src/
│   ├── generateNote/       # Python MIDI generator
│   └── generateWave/       # Julia WAV generator
├── tests/
│   ├── checkWAVE/          # Julia WAV validator
│   ├── playWAVE/           # Julia WAV player
│   └── playMIDI/           # Python MIDI player
├── Makefile                # Main build/run/test automation
├── Makefile.build          # Build rules
├── Makefile.clean          # Clean rules
├── Makefile.tests          # Test rules
└── README.md               # This file
```

## Requirements

Before running the project, install the following tools:

- **Python 3.12+**
- **Julia 1.11+**
- **GNU Make**
- **Timidity** (optional, for MIDI playback: [timidity GitHub](https://github.com/erikdubbelboer/timidity))

## Installation

1. **Install prerequisites:**

    On Debian/Ubuntu:

    ```sh
    sudo apt update
    sudo apt install python3 python3-venv julia make
    # Optional for MIDI playback
    sudo apt install timidity
    ```

    On RedHat/Fedora:

    ```sh
    sudo dnf install python3 python3-virtualenv julia make
    # Optional for MIDI playback
    sudo dnf install timidity
    ```

    On Arch/Manjaro:

    ```sh
    sudo pacman -S python julia make python-virtualenv
    # Optional for MIDI playback
    sudo pacman -S timidity++
    ```

    On Alpine Linux:

    ```sh
    sudo apk update
    sudo apk add python3 py3-virtualenv julia make
    # Optional for MIDI playback
    sudo apk add timidity
    ```

    On Mandriva:

    ```sh
    sudo urpmi python3 python3-virtualenv julia make
    # Optional for MIDI playback
    sudo urpmi timidity
    ```

    Or download Timidity from [the official repository](https://github.com/erikdubbelboer/timidity).

2. **Clone the repository:**

    ```sh
    git clone https://github.com/BrunoRNS/SampleGenerator.git
    cd SampleGenerator
    ```

3. **Install all dependencies and set up environments:**

    ```sh
    make all
    ```

    This will automatically download and install all required Python and Julia packages for you.

## Usage

### 0. **Get The Samples**

You can find the generated samples in the `wave-samples/` and `midi-samples/` directories, if you want to use any of them you can just copy them to your workspace :smiley:

### 1. **Generate All Samples**

Run the full pipeline (build environments, clean old samples, generate new ones):

```sh
make run
```

This will:

- Build Python and Julia environments
- Clean previous samples
- Generate MIDI notes (Python)
- Convert MIDI notes to WAV files (Julia)
- Output samples to `midi-samples/` and `wave-samples/`

### 2. **Test and Validate Samples**

Run all tests (play and validate samples):

```sh
make test
```

- **Check WAV properties:** Ensures WAV files are 8-bit unsigned, 800 Hz, RIFF format
- **Play WAV files:** Listen to generated samples (Julia)
- **Play MIDI files:** Listen to generated MIDI notes (Python)

### 3. **Clean Environments and Samples**

Remove all generated environments and sample files:

```sh
make clean
```

## For SNES Developers

The generated WAV files are designed to be as lightweight as possible for use with SNES tools and SPC700 sample conversion utilities and also in Impulse Tracker. You can use these files directly with SNES music engines or further process them for your workflow.

## License

This project is licensed under the [GNU GPL v3](LICENSE.txt).

## References

- [MIDI.jl](https://github.com/JuliaMusic/MIDI.jl)
- [WAV.jl](https://github.com/danielmatz/WAV.jl)
- [musicpy](https://github.com/lucianzw/musicpy)
- [pygame](https://www.pygame.org/)
- [Timidity](https://github.com/erikdubbelboer/timidity)

---

Made with ❤️ by [BrunoRNS](https://github.com/BrunoRNS).
