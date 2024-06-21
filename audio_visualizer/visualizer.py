"""
visualizer.py

This module initializes the audio visualizer
and starts the visualization process.
"""

from audio_visualizer.vertical_visualizer import visualize_vertical
import numpy as np
import logging

from audio_visualizer.audio_capture import AudioCapture
from audio_visualizer.horizontal_left_to_right_visualizer import (
    visualize_horizontal_left_to_right)
from audio_visualizer.horizontal_right_to_left_visualizer import (
    visualize_horizontal_right_to_left)
import os

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
            # Vertical bars that start from the bottom and go to the top
            if self.mode == 'vertical':
                visualize_vertical(self.stream, self.chunk, self.rate,
                                   self.alpha, self.bar_count, self.window,
                                   self.smoothed_fft)
            # Horizontal bars that start from the left and go to the right
            elif self.mode == 'horizontal-ltr':
                visualize_horizontal_left_to_right(self.stream, self.chunk,
                                                   self.rate, self.alpha,
                                                   self.bar_count, self.window,
                                                   self.smoothed_fft)
            # Horizontal bars that start from the right and go to the left
            elif self.mode == 'horizontal-rtl':
                visualize_horizontal_right_to_left(self.stream, self.chunk,
                                                   self.rate, self.alpha,
                                                   self.bar_count, self.window,
                                                   self.smoothed_fft)
        except KeyboardInterrupt:
            # Terminal cleared using cls/ clear. Print statement processed after clearing terminal.
            if os.name == 'nt':
                os.system('cls')
                print('Visualization stopped by user.')
            else:
                os.system('clear')
                print('Visualization stopped by user.')
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self.stream.stop_stream()
