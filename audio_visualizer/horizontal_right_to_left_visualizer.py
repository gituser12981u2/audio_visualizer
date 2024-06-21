"""
horizontal_right_to_left_visualizer.py

This module visualizes audio data in a horizontal bar chart
from right to left.
"""

import numpy as np
import os
import time

# NOTE rows are the width and cols are the height for os.get_terminal_size


def visualize_horizontal_right_to_left(
        stream, chunk, rate, alpha, window, smoothed_fft, stop_event):
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
            frame_buffer[row] = ' ' * (cols - bar_width) + '█' * bar_width

        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n'.join(frame_buffer), end='', flush=True)

        time.sleep(0.1)  # control frame rate
