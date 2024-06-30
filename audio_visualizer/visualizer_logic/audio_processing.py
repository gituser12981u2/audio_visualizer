import os
import time
from .gpu_config import computation_lib as xp


def setup_environment(theme):
    """
    Configures the terminal environment based on the provided theme settings.

    Args:
        theme (dict): Contains settings for background and bar colors.
    """
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


def process_audio_visualization(stream, chunk, rate, alpha, window, stop_event,
                                draw_function, theme=None):
    """
    Processes and visualizes audio data in real-time using FFT
    and a specified drawing function.

    Args:
        stream (AudioCapture): The audio stream to visualize.
        chunk (int): Number of audio samples per buffer.
        rate (int): Sample rate of the audio.
        alpha (float): Smoothing factor for the visualization.
        window (np.array): Window function to apply the audio data.
        stop_event (Event): Event to signal when the visualization should stop.
        draw_function (function): A function that handles the drawing
        of audio data.
        theme (dict, optional): Theme settings for visual customization.
    """
    # Initialize smoothed FFT with zeros
    smoothed_fft = xp.zeros(chunk // 2 + 1)

    while not stop_event.is_set():
        data = stream.read_data()
        if data is None:
            continue

        data = xp.frombuffer(data, dtype=xp.int16)
        data = data.reshape(-1, 2).mean(axis=1)  # Average the two channels

        # Apply window function if needed
        windowed_data = data * window
        fft_data = xp.abs(xp.fft.rfft(windowed_data))

        # Apply exponential moving average for smoothing
        smoothed_fft = alpha * smoothed_fft + (1 - alpha) * fft_data

        cols, rows = os.get_terminal_size()
        max_fft = xp.max(smoothed_fft, initial=1)  # Avoid division by zero
        scaled_fft = xp.int16((smoothed_fft / max_fft) * rows)

        frame_buffer = [' ' * cols for _ in range(rows)]

        # Clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')

        # Setup theming
        setup_environment(theme)

        # Drawing logic plug in
        draw_function(frame_buffer, cols, rows, scaled_fft)

        print('\n'.join(frame_buffer), end='\033[0m', flush=True)

        time.sleep(0.1)  # control frame rate
