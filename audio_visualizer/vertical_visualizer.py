"""
This module visualizes audio data in a vertical bar chart.
"""

import numpy as np
import os
import time
import logging

# NOTE rows are the width and cols are the height for os.get_terminal_size


def visualize_vertical(
    stream, chunk, rate, alpha, window, smoothed_fft,
        stop_event, theme=None):
    """
    Visualizes audio data in a horizontal vertical bar chart.

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
        scaled_fft = np.int16((smoothed_fft / max_fft) * rows)

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

        for col in range(min(cols, len(scaled_fft))):
            bar_height = scaled_fft[col]
            for row in range(rows - bar_height, rows):
                frame_buffer[row] = frame_buffer[row][:col] + \
                    '█' + frame_buffer[row][col+1:]

        print('\n'.join(frame_buffer), end='\033[0m', flush=True)

        time.sleep(0.1)  # control frame rate


"""Old logic"""
# def visualize_vertical(
#         stream, chunk, rate, alpha, bar_count, window, smoothed_fft):
#     """
#     Visualizes audio data in a vertical bar chart from left to right.

#     Args:
#         stream (AudioCapture): The audio stream object.
#         chunk (int): Number of audio samples per buffer.
#         rate (int): Sample rate (samples per second).
#         alpha (float): Smoothing factor for FFT.
#         bar_count (int): Number of bars in the visualization
#         window (np.ndarray): Window function applied to the audio data.
#         smoothed_fft (np.ndarray): Smoothed FFT result.
#     """
#     while True:
#         data = stream.read_data()
#         if data is None:
#             continue
#         data = np.frombuffer(data, dtype=np.int16)
#         data = data.reshape(-1, 2).mean(axis=1)  # Average the two channels

#         # Apply window function
#         windowed_data = data * window
#         fft = np.abs(np.fft.fft(windowed_data).real)[
#             :len(windowed_data) // 2]  # discard complex conjugate half

#         # Smoothing factor with exponential moving average
#         smoothed_fft = (
#             alpha * smoothed_fft
#             + (1 - alpha) * fft
#         )

#         max_fft = max(np.max(smoothed_fft), 1)  # Avoid division by zero

#         rows, cols = os.get_terminal_size()
#         bar_count = rows

#         # Visualization logic
#         indices = np.logspace(0, np.log10(len(smoothed_fft)),
#                               num=bar_count + 1, endpoint=True,
#                               base=10).astype(int)

#         # Ensure unique indices within bounds
#         indices = np.unique(np.clip(indices, 0, len(smoothed_fft) - 1))

#         current_frame = {}
#         for i in range(len(indices) - 1):
#             bar_values = smoothed_fft[indices[i]:indices[i + 1]]
#             bar_value = np.average(bar_values, weights=np.linspace(
#                 1, 0.1, num=len(bar_values))) if bar_values.size > 0 else 0

#             # Calculate the number of characters to print
#             num_chars = int(np.sqrt(bar_value / max_fft) * cols)
#             for j in range(cols - num_chars, cols):
#                 current_frame[(i, j)] = '█'

#         # Update the terminal once per frame
#         # frame_buffer = [' ' * bar_count for _ in range(cols)]
#         # for y in range(cols):
#         #     for x in range(bar_count):
#         #         frame_buffer[y] = frame_buffer[y][:x] + \
#         #             current_frame.get((x, y), ' ') + frame_buffer[y][x+1:]

#         # frame_buffer = [' ' * cols for _ in range(rows)]
#         # for x in range(rows):  # Iterate over each bar
#         #     for y in range(cols):  # Iterate over each character in the bar
#         #         if (x, y) in current_frame:
#         #             frame_buffer[x] = frame_buffer[x][:y] + \
#         #                 current_frame[(x, y)] + frame_buffer[x][y+1:]

#         frame_buffer = [' ' * rows for _ in range(cols)]
#         for x in range(cols):  # Iterate over each bar
#             for y in range(rows):  # Iterate over each character in the bar
#                 if (x, y) in current_frame:
#                     flipped_index = rows - y - 1
#                     frame_buffer[x] = frame_buffer[x][:flipped_index] + \
#                         current_frame[(x, y)] + \
#                         frame_buffer[x][flipped_index+1:]

#         # Clear the screen and print the frame buffer
#         os.system('cls' if os.name == 'nt' else 'clear')
#         print('\n'.join(frame_buffer), end="", flush=True)

#         time.sleep(0.1)  # control frame rate
