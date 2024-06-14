import pyaudio
import numpy as np
import os
import time
import logging


class AudioVisualizer:
    """Audio Visualizer for terminal.

    This class handles the visualization of audio data in the terminal using
    either a vertical or horizontal bar chart

    Attributes:
        mode (str): Visualization mode ('vertical' or 'horizontal').
        alpha (float): Smoothing factor for FFT.
        chunk (int): Number of frames per buffer.
        rate (int): Sampling rate.
        bar_count (int): Number of bars in the visualization.
        FORMAT (int): Audio format.
        CHANNELS (int): Number of audio channels.
        audio (pyaudio.PyAudio): PyAudio object for audio streaming.
        stream (pyaudio.Stream): Stream object for audio input
        smoothed_fft (np.ndarray): Smoothed FFT result.
        window (np.ndarray): Hamming window applied to audio data.
    """

    def __init__(self, mode='vertical', alpha=0.4, chunk=2048, rate=44100,
                 bar_count=75):
        """Initializes the AudioVisualizer with given parameters.

        Args:
            mode (str): Visualization mode ('vertical' or 'horizontal').
            alpha (float): Smoothing factor for FFT.
            chunk (int): Number of frames per buffer.
            rate (int): Sampling rate.
            bar_count (int): Number of bars in the visualization.
        """
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = rate
        self.CHUNK = chunk
        self.audio = pyaudio.PyAudio()
        self.stream = None

        # List available audio devices
        self.device_index = None
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            # print(f"Device {i}: {info['name']}")
            if 'BlackHole 2ch' in info['name']:
                self.device_index = i
                # print(f"Selected Device {i}: {info['name']}")
                # print(f"Device {i} Max Input Channels: {info['maxInputChannels']}")
                # print(f"Device {i} Max Output Channels: {info['maxOutputChannels']}")
        
        if self.device_index is None:
            raise ValueError("BlackHole 2ch device not found")

        try:
            self.stream = self.audio.open(format=self.FORMAT,
                                          channels=self.CHANNELS,
                                          rate=self.RATE,
                                          input=True,
                                          input_device_index=self.device_index,
                                          frames_per_buffer=self.CHUNK)
        except Exception as e:
            logging.error(f"Failed to open stream: {e}")
        
        self.smoothed_fft = np.zeros(self.CHUNK // 2)
        self.window = np.hamming(self.CHUNK)
        self.mode = mode
        self.alpha = alpha
        self.bar_count = bar_count
        self.previous_frame = None
        logging.basicConfig(level=logging.INFO)

    def start(self):
        """Starts the audio visualization process.
        Continuously reads audio data from the stream and updates the terminal
        visualization until interrupted.
        """
        if self.stream is None:
            logging.error("Stream is not open. Exiting.")
            return

        try:
            if self.mode == 'vertical':
                self.visualize_vertical()
            elif self.mode == 'horizontal':
                self.visualize_horizontal()
        except KeyboardInterrupt:
            logging.info("Visualization stopped by user.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self.cleanup()

    def visualize_vertical(self):
        """Visualizes audio data in a vertical bar chart
        --from left to right."""
        while True:
            try:
                data = np.frombuffer(self.stream.read(self.CHUNK, exception_on_overflow=False), dtype=np.int16)
                data = data.reshape(-1, 2).mean(axis=1) # Average the two channels
            except IOError as e:
                logging.warning(f"Input overflowed: {e}")
                continue

            # Apply window function
            windowed_data = data * self.window
            fft = np.abs(np.fft.fft(windowed_data).real)
            fft = fft[:int(len(fft)/2)]  # keep only the first half

            # Smoothing factor
            self.smoothed_fft = (
                self.alpha * self.smoothed_fft
                + (1 - self.alpha) * fft
            )

            max_fft = (
                np.max(self.smoothed_fft) if np.max(self.smoothed_fft)
                > 0 else 1  # Avoid division by zero
            )

            # Double buffering
            # buffer = []

            # Visualization logic
            indices = np.logspace(0, np.log10(len(self.smoothed_fft)),
                                  num=self.bar_count + 1, endpoint=True,
                                  base=10).astype(int) - 1
            # Ensure unique indices within bounds
            indices = np.unique(np.clip(indices, 0, len(self.smoothed_fft)-1))

            current_frame = {}
            for i in range(len(indices) - 1):
                bar_values = self.smoothed_fft[indices[i]:indices[i+1]]
                if bar_values.size > 0:
                    # Apply a weighting decreasing with frequency
                    weights = np.linspace(1, 0.1, num=len(bar_values))
                    bar_value = np.average(bar_values, weights=weights)
                else:
                    bar_value = 0

                # Calculate the number of characters to print
                num_chars = (int(np.sqrt(bar_value / max_fft) * 50)
                             # Normalize and apply sqrt to enhance visibility
                             if not np.isnan(bar_value) else 0
                             )
                for j in range(num_chars):
                    current_frame[(i, j)] = '█'
                for j in range(num_chars, 50):
                    current_frame[(i, j)] = ' '
            
            # Update the terminal once per frame
            frame_buffer = []
            for y in range(50):
                line = ''.join(current_frame.get((x, y), ' ') for x in range(self.bar_count))
                frame_buffer.append(line)

            # Clear the screen and print the frame buffer
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\n'.join(frame_buffer), end="", flush=True)

            self.previous_frame = current_frame
            time.sleep(0.1)  # control frame rate

    def visualize_horizontal(self):
        """Visualizes audio data in a horizontal bar chart
        --from bottom to top."""
        # Determine the size of the terminal window
        rows, columns = os.get_terminal_size()
        max_bar_height = rows - 2

        # Visualization logic
        bar_count = columns  # Num bars the width of the terminal
        bar_heights = np.zeros(bar_count, dtype=int)

        while True:
            try:
            # Get the audio data and apply the FFT
                data = np.frombuffer(self.stream.read(self.CHUNK), dtype=np.int16)
                data = data.reshape(-1, 2).mean(axis=1)  # Average the two channels
            except IOError as e:
                logging.warning(f"Input overflowed: {e}")
                continue
            
            fft = np.abs(np.fft.fft(
                data * np.hamming(self.CHUNK)).real)[:self.CHUNK // 2]

            self.smoothed_fft = (self.alpha * self.smoothed_fft
                                 + (1 - self.alpha) * fft)  # Apply smoothing
            max_fft = (np.max(self.smoothed_fft)
                       if np.max(self.smoothed_fft) > 0 else 1)  # Normalize

            # Calculate the height of each bar according to the FFT results
            log_scale_index = np.logspace(0, np.log10(len(self.smoothed_fft)),
                                          num=bar_count, endpoint=True,
                                          base=10).astype(int) - 1
            log_scale_index = np.unique(np.clip(log_scale_index, 0,
                                                # unique indices within bounds
                                                len(self.smoothed_fft)-1))

            for i in range(len(log_scale_index) - 1):
                bar_values = self.smoothed_fft[
                    log_scale_index[i]:log_scale_index[i+1]
                ]
                bar_height = (
                    int(np.mean(bar_values) / max_fft * max_bar_height)
                    if bar_values.size > 0 else 0
                )

                bar_heights[i] = bar_height

            # Update the terminal once per frame
            frame_buffer = "\n".join("".join("█" if bar_heights[col] >= row else " "  # noqa: E501
                                             for col in range(bar_count - 1)) for row in range(max_bar_height - 1, -1, -1))  # noqa: E501

            # Clear the terminal and print the entire frame at once
            os.system('cls' if os.name == 'nt' else 'clear')
            print(frame_buffer, end="", flush=True)

            time.sleep(0.1)  # control frame rate

    def cleanup(self):
        """Stops the audio stream and terminates PyAudio."""
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
