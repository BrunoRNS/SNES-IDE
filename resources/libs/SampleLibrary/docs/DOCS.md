# SampleGenerator Technical Documentation

## Overview

SampleGenerator is a cross-language toolchain designed to generate lightweight audio samples (WAV and MIDI) for use with the SNES SPC700 sound processor. The project automates the creation, validation, and playback of simple musical notes and waveforms, focusing on the technical constraints of retro hardware.

## Project Goal

The main goal is to produce audio samples that are:

- **Low sample rate:** 800 Hz (to minimize memory and CPU usage)
- **8-bit unsigned PCM WAV files:** Compatible with SNES sample conversion tools
- **Simple waveforms:** Square, triangle, and sine
- **Single-note MIDI files:** For easy conversion and testing

These constraints ensure the samples are suitable for the SPC700, which has limited RAM and processing power.

## Mathematical Background

### 1. **Sample Rate**

The sample rate (`f_s`) is the number of samples per second. For this project:

$$
f_s = 800\ \text{Hz}
$$

This means each second of audio contains 800 samples. Lower sample rates reduce file size and are sufficient for simple tones.

### 2. **Waveform Synthesis**

#### **Square Wave**

A square wave alternates between maximum and minimum amplitude:

$$
x[n] =
\begin{cases}
A, & \text{if } n \bmod T < T/2 \\
0, & \text{otherwise}
\end{cases}
$$

Where:

- $A$ is the maximum amplitude (255 for 8-bit unsigned)
- $T = \frac{f_s}{f}$ is the period in samples
- $f$ is the frequency in Hz

#### **Triangle Wave**

A triangle wave linearly rises and falls:

$$
x[n] =
\begin{cases}
\frac{2A}{T} \cdot \mod(n, T), & \text{if } \mod(n, T) < T/2 \\
2A - \frac{2A}{T} \cdot \mod(n, T), & \text{otherwise}
\end{cases}
$$

#### **Sine Wave**

A sine wave is defined by:

$$
x[n] = \frac{A}{2} \left[1 + \sin\left(2\pi \frac{n}{T}\right)\right]
$$

This formula ensures the output is always positive (for unsigned 8-bit).

## RIFF WAV File Format

The WAV files generated use the RIFF format, which consists of a header and data section:

- **Header fields:**
  - Chunk ID: "RIFF"
  - Format: "WAVE"
  - Subchunk1 ID: "fmt "
  - Audio format: PCM (1)
  - Number of channels: 1 (mono)
  - Sample rate: 800 Hz
  - Bits per sample: 8
  - Subchunk2 ID: "data"
  - Subchunk2 size: Number of samples

All fields are set to ensure compatibility with SNES sample tools.

## MIDI Note Conversion

MIDI files are generated with a single note per file. The note's pitch is converted to frequency using:

$$
f = 440 \times 2^{\frac{p - 69}{12}}
$$

Where:

- $p$ is the MIDI note number
- 440 Hz is the frequency of A4

The duration is extracted from the MIDI file and converted to seconds.

## Workflow

1. **Generate MIDI notes (Python):**
    - Each file contains one note.
    - Saved in `midi-samples/`.

2. **Convert MIDI to WAV (Julia):**
    - Extract note pitch and duration.
    - Synthesize square, triangle, and sine waves.
    - Write WAV files with custom RIFF headers.

3. **Validate WAV files (Julia):**
    - Check sample rate, bit depth, and format.

4. **Playback (Python/Julia):**
    - Play MIDI and WAV files for quick verification.

## Why 800 Hz and 8-bit?

- **800 Hz** is a compromise between quality and memory usage. The SPC700 can handle higher rates, but lower rates are preferred for longer samples and effects.
- **8-bit unsigned** is a very light format for SPC700 samples, SPC700 works with signed 16 bit BRR compressed audio samples, then using an even more lightweight format makes conversion more convinient.

## Example: Generating a 440 Hz Square Wave

For a 1-second, 440 Hz square wave at 800 Hz sample rate:

- Period $T = \frac{800}{440} \approx 1.818$ samples
- The waveform alternates every ~0.91 samples between 0 and 255.

## Extending the Project

- Add more waveforms (e.g., sawtooth, noise)
- Support multi-note MIDI files
- Integrate SNES sample conversion tools

## References

- [SPC700 Technical Reference](https://wiki.superfamicom.org/spc700)
- [MIDI.jl](https://github.com/JuliaMusic/MIDI.jl)
- [WAV.jl](https://github.com/danielmatz/WAV.jl)
- [musicpy](https://github.com/lucianzw/musicpy)
- [pygame](https://www.pygame.org/)
- [Timidity](https://github.com/erikdubbelboer/timidity)
