"""
This module visualizes audio data in a horizontal bar chart
from left to right.
"""

import numpy as np
import os
import time

# NOTE rows are the width and cols are the height for os.get_terminal_size


def visualize_horizontal_left_to_right(
        stream, chunk, rate, alpha, window, smoothed_fft, stop_event):
    """
    Visualizes audio data in a horizontal left-to-right bar chart.

    Args:
        stream (AudioCapture): The audio stream to visualize.
        chunk (int): Number of audio samples per buffer.
        rate (int): Sample rate of the audio.
        alpha (float): Smoothing factor for the visualization.
        window (np.array): Window function to apply the audio data.
        smoothed_fft (np.array): Array to store the smoothed FFT values.
        stop_event (Event): Event to signal when teh visualization should stop.
    """
    # Initialize smoothed FFT with zeros
    smoothed_fft = np.zeros(chunk // 2 + 1)

    while not stop_event.is_set():
        data = stream.read_data()
        if data is None:
            continue

        data = np.frombuffer(data, dtype=np.int16)
        data = data.reshape(-1, 2).mean(axis=1)  # Average the two channels

        # Apply window function if needed
        windowed_data = data * window
        fft_data = np.abs(np.fft.rfft(windowed_data))

        # Apply exponential moving average for smoothing
        smoothed_fft = alpha * smoothed_fft + (1 - alpha) * fft_data

        cols, rows = os.get_terminal_size()
        max_fft = np.max(smoothed_fft, initial=1)  # Avoid division by zero
        scaled_fft = np.int16((smoothed_fft / max_fft) * cols)

        frame_buffer = [' ' * cols for _ in range(rows)]
        for row in range(min(rows, len(scaled_fft))):
            bar_width = scaled_fft[row]
            frame_buffer[row] = '█' * bar_width + ' ' * (cols - bar_width)

        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n'.join(frame_buffer), end='', flush=True)

        time.sleep(0.1)  # control frame rate
