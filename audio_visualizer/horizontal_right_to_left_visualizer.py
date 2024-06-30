"""
This module visualizes audio data in a horizontal bar chart
from right to left.
"""

import numpy as np
import os
import time
import logging

# NOTE rows are the width and cols are the height for os.get_terminal_size


def visualize_horizontal_right_to_left(
    stream, chunk, rate, alpha, window, smoothed_fft,
        stop_event, theme=None):
    """
    Visualizes audio data in a horizontal right-to-left bar chart.

    Args:
        stream (AudioCapture): The audio stream to visualize.
        chunk (int): Number of audio samples per buffer.
        rate (int): Sample rate of the audio.
        alpha (float): Smoothing factor for the visualization.
        window (np.array): Window function to apply the audio data.
        smoothed_fft (np.array): Array to store the smoothed FFT values.
        stop_event (Event): Event to signal when the visualization should stop.
        theme (dict, optional): Contains color settings.
    """

    # Try to import CuPy. If it's not available or no GPU is detected,
    # fall back to NumPy.
    try:
        import cupy as xp  # type: ignore
        if xp.cuda.runtime.getDeviceCount() > 0:
            logging.info("Using CuPy for GPU acceleration.")
        else:
            import numpy as xp
            logging.info(
                "No GPU with CUDA cores detected. Using NumPy instead of CuPy."
            )
    except ImportError:
        import numpy as xp
        logging.info(
            "No GPU with CUDA cores detected. Using NumPy instead of CuPy.")

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

        # Clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')

        if theme:
            if 'background_color' in theme and (
                    theme['background_color'] != 'default'):
                bg_color = tuple(
                    map(int, theme['background_color'].split(';')))
                # Set background color
                print(f"\033[48;2;{bg_color[0]};{
                    bg_color[1]};{bg_color[2]}m", end='')

            if 'bar_color' in theme and theme['bar_color'] != 'default':
                bar_color = tuple(map(int, theme['bar_color'].split(';')))
                # set bar color
                print(f"\033[38;2;{
                    bar_color[0]};{bar_color[1]};{bar_color[2]}m", end='')

        for row in range(min(rows, len(scaled_fft))):
            bar_width = scaled_fft[row]
            frame_buffer[row] = ' ' * (cols - bar_width) + '█' * bar_width

        print('\n'.join(frame_buffer), end='\033[0m', flush=True)

        time.sleep(0.1)  # control frame rate
