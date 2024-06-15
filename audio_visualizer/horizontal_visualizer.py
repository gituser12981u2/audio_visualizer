"""
horizontal_visualizer.py

This module visualizes audio data in a horizontal bar chart.
"""

import numpy as np
import os
import time


def visualize_horizontal(
        stream, chunk, rate, alpha, bar_count, window, smoothed_fft):
    """
    Visualizes audio data in a horizontal bar chart from bottom to top.

    Args:
        stream (AudioCapture): The audio stream object.
        chunk (int): Number of audio samples per buffer.
        rate (int): Sample rate (samples per second).
        alpha (float): Smoothing factor for FFT.
        bar_count (int): Number of bars in the visualization
        window (np.ndarray): Window function applied to the audio data.
        smoothed_fft (np.ndarray): Smoothed FFT result.
    """
    # Determine the size of the terminal window
    rows, columns = os.get_terminal_size()
    max_bar_height = rows - 2

    # Visualization logic
    bar_heights = np.zeros(bar_count, dtype=int)

    while True:
        # Get the audio data and apply the FFT
        data = stream.read_data()
        if data is None:
            continue
        data = np.frombuffer(data, dtype=np.int16)
        data = data.reshape(-1, 2).mean(axis=1)  # Average the two channels

        fft = np.abs(np.fft.fft(data * window).real)[:chunk // 2]

        smoothed_fft = (alpha * smoothed_fft + (1 - alpha)
                        * fft)  # Apply smoothing
        max_fft = max(np.max(smoothed_fft), 1)  # Avoid division by zero

        # Calculate the height of each bar according to the FFT results
        log_scale_index = np.logspace(0, np.log10(len(smoothed_fft)),
                                      num=bar_count, endpoint=True,
                                      base=10).astype(int) - 1
        log_scale_index = np.unique(np.clip(log_scale_index, 0,
                                            # unique indices within bounds
                                            len(smoothed_fft) - 1))

        for i in range(len(log_scale_index) - 1):
            bar_values = smoothed_fft[
                log_scale_index[i]:log_scale_index[i + 1]
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
