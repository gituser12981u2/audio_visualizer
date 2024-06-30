# Audio Visualizer

A simple, janky, yet charming terminal-based audio visualizer written in Python. It can visualize audio data from a microphone or any other audio input device.

## Features

- Visualize audio data in vertical or horizontal bar charts.
- Adjustable parameters such as smoothing factor, buffer size, sampling rate, and number of bars.
- Theme support for customizing the visual output.
- Works on Linux, macOS, and Windows.
- Works best in VSC terminal, iterm2, kitty, and alacritty.

## Installation

### Prerequisites

- Python 3.6 or later

### Install the PortAudio Library

#### Linux

```bash
sudo apt-get update
```

```bash
sudo apt-get install -y portaudio19-dev
```

#### macOS

Setup a loopback device.

```bash
brew install blackhole-2ch
```

1. Open the "Audio MIDI Setup" app.
2. Create an "Aggregate Device" with the default input device and "BlackHole 2ch".
3. Set this Aggregate Device as the input device

#### Windows

Download and install the PortAudio library from [here](https://files.portaudio.com/download.html)

## Install the Python Package

1. Clone the repository:

    ```bash
    git clone https://github.com/gituser12981u2/audio_visualizer
    ```

2. Set up a virtual environment:

    ```bash
    python3 -m venv .venv
    ```

    ```bash
    source .venv/bin/activate  
    # On Windows, use '.venv\Scripts\activate'
    ```

3. Install the package:

    ```bash
    pip install .
    ```

### Optional GPU Acceleration

If your system has a compatible Nvidia or AMD GPU, you can enable GPU acceleration by installing an additional dependency:

```bash
pip install .[gpu]
```

**Note**: GPU acceleration is not recommended if your system supports AMX or uses an Apple M-series chip, as native operations may be more efficient.

Then follow these [instructions](https://docs.cupy.dev/en/stable/install.html#using-cupy-on-amd-gpu-experimental) to install the CUDA--for Nvidia--or ROCm--for AMD--toolkit.

## Usage

### Running the Visualizer

To Start the visualizer, use the following command:

```bash
audio-visualizer
```

Or run this command for the same outcome:

```bash
audio-visualizer --mode vertical
```

Or to run in horizontal mode:

```bash
audio-visualizer --mode horizontal-ltr
```

**Note**: there are two horizontal modes. One that draws bars from left to right (ltr) and one that draws bars from right to left (rtl)

### Configuration File

Modify `config.lua` to change default settings and key bindings. This file controls various aspects of the Audio Visualizer's behavior, including the visual mode, hotkeys, and audio processing parameters.

#### Config File Location

- **Linux/macOS**: Place your `config.lua` in `~/.config/audio_visualizer/`. This is teh recommended location as it follwos the standard configuration directory structure on Unix-like systems.
- **Windows**: Place your `config.lua` in `%APPDATA%\audio-visualizer\`. This location is recommended for Windows users as it aligns with the typical application data storage.

If a `config.lua` file is not found in these locations, the program will attempt to load it from the directory where the `audio-visualizer` command is executed.

### Hotkey mode switcher

Switch visualization modes dynamically with configured hotkeys.
For example, the default keybindings are:

- 'ctrl+h': horizontal ltr mode
- 'ctrl+l': horizontal rtl mode
- 'ctrl+j': vertical mode

### Themes

Themes allow you to customize the visual appearance of the audio visualizer:

- **background_color**: Set to a 'RGB' value like '255;0;0' for red, or 'default to use the terminal's default color.
- **bar_color**: Set to a 'RGB' value or 'default' to use the terminal's default color.

### Command Line Options

- `--mode`: Visualization mode('vertical or horizontal). Default is `vertical`. That is if you put no `--mode` option.
- `--alpha`: Smoothing factor for FFT. Default is `0.4`.
- `--chunk`: Number of frames per buffer. Default is `2048`.
- `--rate`: Sampling rate Default is `44100`.

Example:

```bash
audio-visualizer --mode horizontal-rtl --alpha 0.3 --chunk 1024 --rate 48000
```

## Windows Specific Instructions

On Windows, audio routing can be tricky. If you want to visualize audio from your speakers or headphones instead of just the microphone, you will need to use a virtual audio cable. Follow these steps:

1. Download and install a virtual audio cable from [VB-Audio](<https://vb-audio.com/Cable/>)
2. Set your playback device to the virtual audio cable.
3. In your recording devices, set the virtual audio cable as the default recording device.
4. Route the audio through your headphones or speakers.

This will allow for the program to render the audio that is being outputted on the device as well as continue to have the user be able to hear the same audio.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributors

Thank you to the follow people for their contributions to this project:

-[@ohksith](https://github.com/ohksith) - Provided fix for the terminal to clean it self after visualization stopped
