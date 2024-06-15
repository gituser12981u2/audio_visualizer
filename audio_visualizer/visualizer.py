"""
visualizer.py

This module initializes the audio visualizer
and starts the visualization process.
"""

import numpy as np
import logging

from audio_visualizer.audio_capture import AudioCapture
from audio_visualizer.horizontal_visualizer import visualize_horizontal
from audio_visualizer.vertical_visualizer import visualize_vertical


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
        window (np.ndarray): Hamming window applied to audio data.
        smoothed_fft (np.ndarray): Smoothed FFT result.
        stream (AudioCapture): Audio capture object.
    """

    def __init__(self, mode='vertical', alpha=0.4, chunk=2048, rate=44100,
                 bar_count=75):
        self.mode = mode
        self.alpha = alpha
        self.chunk = chunk
        self.rate = rate
        self.bar_count = bar_count
        self.window = np.hamming(self.chunk)
        self.smoothed_fft = np.zeros(self.chunk // 2)
        self.stream = AudioCapture(
            chunk=self.chunk, rate=self.rate, channels=2)
        self.stream.start_stream()

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
                visualize_vertical(self.stream, self.chunk, self.rate,
                                   self.alpha, self.bar_count, self.window,
                                   self.smoothed_fft)
            elif self.mode == 'horizontal':
                visualize_horizontal(self.stream, self.chunk, self.rate,
                                     self.alpha, self.bar_count, self.window,
                                     self.smoothed_fft)
        except KeyboardInterrupt:
            logging.info("Visualization stopped by user.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self.stream.stop_stream()
