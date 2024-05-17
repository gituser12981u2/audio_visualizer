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

    def __init__(self, mode='vertical', alpha=0.2, chunk=2048, rate=44100,
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
        self.CHANNELS = 1
        self.RATE = rate
        self.CHUNK = chunk
        self.audio = pyaudio.PyAudio()
        self.stream = None
        try:
            self.stream = self.audio.open(format=self.FORMAT,
                                          channels=self.CHANNELS,
                                          rate=self.RATE,
                                          input=True,
                                          frames_per_buffer=self.CHUNK)
        except Exception as e:
            logging.error(f"Failed to open stream: {e}")
        self.smoothed_fft = np.zeros(self.CHUNK // 2)
        self.window = np.hamming(self.CHUNK)
        self.mode = mode
        self.alpha = alpha
        self.bar_count = bar_count
        logging.basicConfig(level=logging.INFO)

    def start(self):
        """Starts the audio visualization process.
        Continuously reads audio data from the stream and updates the terminal
        visualization until interrupted.
        """
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
            data = np.frombuffer(self.stream.read(self.CHUNK), dtype=np.int16)
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

            # Clear the screen
            os.system('cls' if os.name == 'nt' else 'clear')

            # Visualization logic
            indices = np.logspace(0, np.log10(len(self.smoothed_fft)),
                                  num=self.bar_count + 1, endpoint=True,
                                  base=10).astype(int) - 1
            # Ensure unique indices within bounds
            indices = np.unique(np.clip(indices, 0, len(self.smoothed_fft)-1))

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
                print('█' * num_chars)

            time.sleep(0.07)  # control frame rate

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
            # Get the audio data and apply the FFT
            data = np.frombuffer(self.stream.read(self.CHUNK), dtype=np.int16)
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

            # Clear the frame buffer
            frame_buffer = "\n".join("".join("█" if bar_heights[col] >= row else " "  # noqa: E501
                                             for col in range(bar_count - 1)) for row in range(max_bar_height - 1, -1, -1))  # noqa: E501

            # Clear the terminal and print the entire frame at once
            os.system('cls' if os.name == 'nt' else 'clear')
            print(frame_buffer, end="", flush=True)

            time.sleep(0.07)  # control frame rate

    def cleanup(self):
        """Stops the audio stream and terminates PyAudio."""
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
