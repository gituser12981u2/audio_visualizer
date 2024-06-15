"""
vertical_visualizer.py

This module visualizes audio data in a vertical bar chart.
"""

import numpy as np
import os
import time


def visualize_vertical(
        stream, chunk, rate, alpha, bar_count, window, smoothed_fft):
    """
    Visualizes audio data in a vertical bar chart from left to right.

    Args:
        stream (AudioCapture): The audio stream object.
        chunk (int): Number of audio samples per buffer.
        rate (int): Sample rate (samples per second).
        alpha (float): Smoothing factor for FFT.
        bar_count (int): Number of bars in the visualization
        window (np.ndarray): Window function applied to the audio data.
        smoothed_fft (np.ndarray): Smoothed FFT result.
    """
    while True:
        data = stream.read_data()
        if data is None:
            continue
        data = np.frombuffer(data, dtype=np.int16)
        data = data.reshape(-1, 2).mean(axis=1)  # Average the two channels

        # Apply window function
        windowed_data = data * window
        fft = np.abs(np.fft.fft(windowed_data).real)[
            :int(len(windowed_data)/2)]  # keep only the first half

        # Smoothing factor
        smoothed_fft = (
            alpha * smoothed_fft
            + (1 - alpha) * fft
        )

        max_fft = max(np.max(smoothed_fft), 1)  # Avoid division by zero

        # Visualization logic
        indices = np.logspace(0, np.log10(len(smoothed_fft)),
                              num=bar_count + 1, endpoint=True,
                              base=10).astype(int) - 1

        # Ensure unique indices within bounds
        indices = np.unique(np.clip(indices, 0, len(smoothed_fft) - 1))

        current_frame = {}
        for i in range(len(indices) - 1):
            bar_values = smoothed_fft[indices[i]:indices[i + 1]]
            bar_value = np.average(bar_values, weights=np.linspace(
                1, 0.1, num=len(bar_values))) if bar_values.size > 0 else 0

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
            line = ''.join(current_frame.get((x, y), ' ')
                           for x in range(bar_count))
            frame_buffer.append(line)

        # Clear the screen and print the frame buffer
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n'.join(frame_buffer), end="", flush=True)

        time.sleep(0.1)  # control frame rate
