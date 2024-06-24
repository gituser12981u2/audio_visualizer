import numpy as np
import logging
import os
from pynput import keyboard
from threading import Thread, Event

from audio_visualizer.audio_capture import AudioCapture
from audio_visualizer.vertical_visualizer import visualize_vertical
from audio_visualizer.horizontal_left_to_right_visualizer import (
    visualize_horizontal_left_to_right)
from audio_visualizer.horizontal_right_to_left_visualizer import (
    visualize_horizontal_right_to_left)


def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_visualization_function(mode):
    """
    Returns the visualization function based on the provided mode.

    Args:
        mode (str): The mode of visualization to retrieve.

    Returns:
        function: A function that corresponds to the visualization mode.

    Raises:
        ValueError: if an unsupported visualization mode is provided.
    """
    if mode == 'vertical':
        return visualize_vertical
    elif mode == 'horizontal-ltr':
        return visualize_horizontal_left_to_right
    elif mode == 'horizontal-rtl':
        return visualize_horizontal_right_to_left
    else:
        raise ValueError("Unsupported visualization mode: {mode}")


class AudioVisualizer:
    """
    A class to manage audio visualization.

    Attributes:
        mode (str): Current visualization mode.
        alpha (float): Alpha parameter for visualization smoothing.
        chunk (int): Number of audio samples per buffer.
        rate (int): Sample rate (samples per second).
        stream (AudioCapture): Audio stream for capturing audio data.
        thread (Thread): Thread running the visualization process.
        stop_event (Event): Event to signal the thread to stop.
    """

    def __init__(self, mode='vertical', alpha=0.4, chunk=2048, rate=44100):
        """
        Initializes the AudioVisualizer object with default settings
        for audio streaming.

        Args:
            mode (str, optional): The initial visualization mode.
            alpha (float, optional): Smoothing factor for visualization.
            chunk (int, optional): Number of audio samples per buffer.
            rate (int, optional): Sampling rate of the audio in Hz.
        """
        self.mode = mode
        self.alpha = alpha
        self.chunk = chunk
        self.rate = rate
        self.stream = AudioCapture(
            chunk=self.chunk, rate=self.rate, channels=2)
        self.stream.start_stream()
        self.thread = None
        self.stop_event = Event()
        self.setup_hotkeys()
        logging.info("Audio Visualizer initialized")

    def setup_hotkeys(self):
        """
        Sets up the keyboard listener
        for hotkeys to change visualization modes.
        """
        listener = keyboard.Listener(on_press=self.on_key_press)
        listener.start()
        logging.info("Keyboard listener started")

    def on_key_press(self, key):
        """
        Handles key press events to change visualization modes based
        on Ctrl combinations.

        Args:
            key (Key): The key that was pressed.
        """
        # Check if the 'Ctrl' key is pressed
        if isinstance(key, keyboard.Key):
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.ctrl_pressed = True

        # Check for the specific character keys while 'Ctrl' is pressed
        if isinstance(key, keyboard.KeyCode):
            char = key.char
            if self.ctrl_pressed and char in ['v', 'l', 'r']:
                new_mode = {'v': 'vertical', 'l': 'horizontal-ltr',
                            'r': 'horizontal-rtl'}.get(char)
                if new_mode and new_mode != self.mode:
                    self.change_mode(new_mode)

    def on_key_release(self, key):
        """
        Handles key release events to manage the state of the Ctrl key.

        Args:
            key (Key): The key that was released.
        """
        # Check if the 'Ctrl' key is released
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            self.ctrl_pressed = False

    def change_mode(self, new_mode):
        """
        Change the mode of the visualizer and restart visualization.

        Args:
            new_mode (str): The new visualization mode to set.
        """
        logging.debug(f"Attempting to change mode from {
                      self.mode} to {new_mode}")
        self.mode = new_mode
        self.restart_visualization()

    def restart_visualization(self):
        """Restart the visualization when the mode is changed."""
        if self.thread is not None and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join()
            self.stop_event.clear()
            logging.info("Visualization thread stopped and restarted.")
        self.thread = Thread(target=self.run_visualization)
        self.thread.start()

    def run_visualization(self):
        """Run the visualization in a separate thread to keep UI responsive."""
        try:
            visualize = get_visualization_function(self.mode)
            visualize(self.stream, self.chunk, self.rate, self.alpha,
                      np.hamming(self.chunk), np.zeros(self.chunk // 2),
                      self.stop_event)
        except Exception as e:
            logging.error(f"Error during visualization: {e}")

    def start(self):
        """Start the initial visualization."""
        logging.info("Starting visualization.")
        self.restart_visualization()

    def stop(self):
        """Stop the visualization gracefully."""
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join()
        clear_screen()
        logging.info("Visualization stopped.")
