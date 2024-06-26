import numpy as np
import logging
import os
from pynput import keyboard
from threading import Thread, Event

from audio_visualizer.audio_capture import AudioCapture
from audio_visualizer.visualizer_logic.audio_processing import (
    process_audio_visualization
)
from audio_visualizer.visualizer_logic.visualizer_drawer import (
    draw_horizontal_ltr, draw_horizontal_rtl, draw_vertical
)


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
        return draw_vertical
    elif mode == 'horizontal-ltr':
        return draw_horizontal_ltr
    elif mode == 'horizontal-rtl':
        return draw_horizontal_rtl
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

    def __init__(
        self, mode, alpha, chunk, rate,
            key_binds, theme=None, audio_source=None):
        """
        Initializes the AudioVisualizer object with default settings
        for audio streaming.

        Args:
            mode (str): The initial visualization mode.
            alpha (float): Smoothing factor for visualization.
            chunk (int): Number of audio samples per buffer.
            rate (int): Sampling rate of the audio in Hz.
            key_binds (dict, optional): Configuration for key bindings.
        """
        self.mode = mode
        self.alpha = alpha
        self.chunk = chunk
        self.rate = rate
        self.key_binds = key_binds
        self.theme = theme or None
        self.device_name = audio_source or None
        self.stream = AudioCapture(
            chunk=self.chunk, rate=self.rate, channels=2,
            device_name=self.device_name)
        self.stream.start_stream()
        self.thread = None
        self.stop_event = Event()
        self.modifier_pressed = False  # State flag for modifier key
        self.setup_hotkeys()
        logging.info(
            f"Audio Visualizer initialized with mode: {self.mode}, alpha: {
                self.alpha}, chunk: {self.chunk}, rate: {self.rate}"
        )

    def setup_hotkeys(self):
        """
        Sets up the keyboard listener
        for hotkeys to change visualization modes.
        """
        listener = keyboard.Listener(
            on_press=self.on_key_press, on_release=self.on_key_release)
        listener.start()
        logging.info("Keyboard listener started")

    def on_key_press(self, key):
        """
        Handles key press events to change visualization modes based
        on on configured keybindings.

        Args:
            key (Key): The key that was pressed.
        """
        try:
            if isinstance(key, keyboard.Key):
                modifier_keys = [getattr(keyboard.Key,
                                         f'{self.key_binds[
                                             "modifier_key"]}_l'),
                                 getattr(keyboard.Key,
                                         f'{self.key_binds["modifier_key"]}_r')
                                 ]
                if key in modifier_keys:
                    self.modifier_pressed = True

            if isinstance(key, keyboard.KeyCode) and self.modifier_pressed:
                if key.char in self.key_binds['keys']:
                    logging.debug(f"{key.char} is pressed")
                    new_mode = self.key_binds['keys'][key.char]
                    if new_mode and new_mode != self.mode:
                        self.change_mode(new_mode)
        except Exception as e:
            logging.error(f"Error handling key press: {e}")

    def on_key_release(self, key):
        """
        Manages the state of the Ctrl key upon its release.

        Args:
            key (Key): The key that was released.
        """
        try:
            modifier_keys = [getattr(keyboard.Key,
                                     f'{self.key_binds["modifier_key"]}_l'),
                             getattr(keyboard.Key,
                                     f'{self.key_binds["modifier_key"]}_r')]
            if key in modifier_keys:
                self.modifier_pressed = False
        except Exception as e:
            logging.error(f"Error handling key release: {e}")

    def change_mode(self, new_mode):
        """
        Change the mode of the visualizer and restart visualization.

        Args:
            new_mode (str): The new visualization mode to set.
        """
        logging.info(f"Changing mode from {
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
            drawing_function = get_visualization_function(self.mode)
            process_audio_visualization(stream=self.stream,
                                        chunk=self.chunk,
                                        rate=self.rate,
                                        alpha=self.alpha,
                                        window=np.hamming(self.chunk),
                                        stop_event=self.stop_event,
                                        draw_function=drawing_function,
                                        theme=self.theme
                                        )
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
