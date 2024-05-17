# Audio Visualizer

A simple, janky, yet charming terminal-based audio visualizer written in Python. It can visualize audio data from a microphone or any other audio input device.

## Features

- Visualize audio data in vertical or horizontal bar charts.
- Adjustable parameters such as smoothing factor, buffer size, sampling rate, and number of bars.
- Works on Linux, macOS, and Windows (with some additional setup on Windows).

## Installation

### Prerequisites

- Python 3.6 or later
- PortAudio library (for PyAudio)

### Install the PortAudio Library

#### Linux

```bash
sudo apt-get update
sudo apt-get install -y portaudio19-dev
```

#### macOS

```bash
brew install portaudio
```

#### Windows

Download and install the PortAudio library from here

## Install the Python Package

1. Clone the repository:

    ```bash
    git clone https://github.com/gituser12981u2/audio_visualizer
    ```

2. Set up a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use '.venv\Scripts\activate'
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
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
audio-visualizer --mode horizontal
```

### Command Line Options

- `--mode`: Visualization mode('vertical or horizontal). Default is `vertical`. That is if you put no `--mode` option.
- `--alpha`: Smoothing factor for FFT. Default is `0.2`.
- `--chunk`: Number of frames per buffer. Default is `2048`.
- `--rate`: Sampling rate Default is `44100`.
- `--bar_count`: Number of bars in the visualization. Default is `75`.

Example:

```bash
audio-visualizer --mode horizontal --alpha 0.3 --chunk 1024 --rate 48000 -bar_count 100
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

## License

This project is licensed under the MIT License. See the LICENSE file for details.
