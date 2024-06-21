# Audio Visualizer

A simple, janky, yet charming terminal-based audio visualizer written in Python. It can visualize audio data from a microphone or any other audio input device.

## Features

- Visualize audio data in vertical or horizontal bar charts.
- Adjustable parameters such as smoothing factor, buffer size, sampling rate, and number of bars.
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

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    ```bash
    pip install .
    ```

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

### Hotkey mode switcher

Switch to a different view--mode--while already in a visualization.

While running a mode, press **'ctrl+l'** to switch to horizontal ltr mode, **'ctrl+r'** to switch to horizontal rtl mode, or **'ctrl+v'** to switch to vertical mode.

-'ctrl+l': horizontal ltr mode
-'ctrl+r': horizontal rtl mode
-'ctrl+v': vertical mode

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

## Contributing

1. Fork the repository.
2. Create a new branch(`git checkout -b feature-branch`).
3. Commit your changes(`git commit -am 'Add new feature'`)
4. Push to the branch(`git push origin feature-branch`)..
5. Create a new Pull Request.

### Linting and Formatting

Please ensure that any updates adhere to the project's style guidelines before committing.

- Run flake8 to check for linting issues:
```bash
flake8 audio_visualizer tests audio_capture.py horizontal_visualizer.py vertical_visualizer.py visualizer.py
```

- Run autopep8 to format the code to flake8 standards
    - Note that autopep8 doesn't work 100% so some manual formatting may be necessary

```bash
autopep8 --in-place --aggressive --aggressive audio_visualizer tests audio_capture.py horizontal_visualizer.py vertical_visualizer.py visualizer.py
```

One can also set up a pre-commit hook to automate these checks:

1. Install pre-commit:
```bash
pip install pre-commit
```

2. Create a .pre-commit-config.yaml file with the following content:
```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-autopep8
    rev: v1.5.7
    hooks:
      - id: autopep8
        args: [--aggressive, --aggressive]

  - repo: https://gitlab.com/pycqa/flake8
    rev: 3.9.2
    hooks:
      - id: flake8
```

3. Install the pre-commit hooks:
```bash
pre-commit install
```

This will ensure that autopep8 and flake8 run automatically before each commit.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributors
Thank you to the follow people for their contributions to this project:

-[@ohksith](https://github.com/ohksith) - Provided fix for the terminal to clean it self after visualization stopped