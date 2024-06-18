"""
horizontal_left_to_right_visualizer.py

This module visualizes audio data in a horizontal bar chart.
"""

import numpy as np
import os
import time

# NOTE rows are the width and cols are the height for os.get_terminal_size


def visualize_horizontal_left_to_right(
        stream, chunk, rate, alpha, bar_count, window, smoothed_fft):
    # Initialize smoothed FFT with zeros
    smoothed_fft = np.zeros(chunk // 2 + 1)

    while True:
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


# def visualize_horizontal(
#         stream, chunk, rate, alpha, bar_count, window, smoothed_fft):
#     """
#     Visualizes audio data in a vertical bar chart from bottom to top.
#     """
#     rows, cols = os.get_terminal_size()  # Get terminal size dynamically
#     bar_count = rows  # Assume bar_count should use all available rows

#     while True:
#         data = stream.read_data()
#         if data is None:
#             break
#         data = np.frombuffer(data, dtype=np.int16)
#         data = data.reshape(-1, 2).mean(axis=1)  # Average two channels

#         windowed_data = data * window
#         fft = np.abs(np.fft.fft(windowed_data).real)
# [:len(windowed_data) // 2]

#         smoothed_fft = alpha * smoothed_fft + (1 - alpha) * fft
#         max_fft = max(np.max(smoothed_fft), 1)  # Normalize the max value

#         indices = np.logspace(0, np.log10(len(smoothed_fft)),
#                               num=bar_count + 1,
#                               endpoint=True, base=10).astype(int)
#         indices = np.unique(np.clip(indices, 0, len(smoothed_fft) - 1))

#         current_frame = {}
#         for i in range(len(indices) - 1):
#             bar_values = smoothed_fft[indices[i]:indices[i + 1]]
#             bar_value = np.average(bar_values, weights=np.linspace(
#                 1, 0.1, num=len(bar_values))) if bar_values.size > 0 else 0
#             num_chars = int((bar_value / max_fft) * cols)

#             for j in range(cols - num_chars, cols):
#                 current_frame[(i, j)] = '█'

#         frame_buffer = [' ' * rows for _ in range(cols)]
#         for x in range(cols):  # Iterate over each bar
#             for y in range(rows):  # Iterate over each character in the bar
#                 if (x, y) in current_frame:
#                     frame_buffer[x] = frame_buffer[x][:y] + \
#                         current_frame[(x, y)] + frame_buffer[x][y+1:]

#         os.system('cls' if os.name == 'nt' else 'clear')
#         print('\n'.join(frame_buffer), end="", flush=True)

#         time.sleep(0.1)
