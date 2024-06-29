"""
audio_capture.py

This module captures audio from the microphone using PyAudio
"""

import pyaudio
import logging
import platform


class AudioCapture:
    """
    A class to handle audio capture using PyAudio.

    Attributes:
        FORMAT (int): Audio format (16-bit PCM).
        chunk (int): Number of audio samples per buffer.
        rate (int): Sample rate (samples per second).
        channels (int): Number of audio channels
        audio_source (str): The name of the audio input device to use.
        audio (pyaudio.PyAudio): PyAudio object for audio streaming.
        stream (pyaudio.Stream): Stream object for audio input.
    """

    def __init__(self, chunk, rate, channels=2, device_name=None):
        self.FORMAT = pyaudio.paInt16
        self.CHUNK = chunk
        self.RATE = rate
        self.CHANNELS = channels
        self.device_name = device_name
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start_stream(self):
        """
        Starts the audio stream. Selects the specified device if provided.
        """
        device_index = None

        logging.info(f"Specified device name {self.device_name}")

        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            logging.info(f"Device {i}: {info['name']}")

        # List available audio devices
        if self.device_name:
            # Attempt to find specified device
            for i in range(self.audio.get_device_count()):
                info = self.audio.get_device_info_by_index(i)
                if self.device_name in info['name']:
                    logging.info(f"Selected Device {i}: {info['name']}")
                    device_index = i
                    break
            if device_index is None:
                logging.error(f"Device '{self.device_name}' not found.")

        if device_index is None and platform.system() == 'Darwin':
            # Specific handling for macOS
            for i in range(self.audio.get_device_count()):
                info = self.audio.get_device_info_by_index(i)
                if 'BlackHole 2ch' in info['name']:
                    logging.info(f"Selected Device {i}: {info['name']}")
                    device_index = i
                    break
            if device_index is None:
                logging.error(
                    "BlackHole 2ch not found on this system.")

        # Use the default input device if no specific device name is provided
        if device_index is None:
            # Fallback to default input device
            device_index = self.audio.get_default_input_device_info()[
                'index']
            default_device_info = self.audio.get_device_info_by_index(
                device_index)
            logging.info(
                f"No specific device selected, using default input device: {
                    default_device_info['name']}")

        try:
            self.stream = self.audio.open(format=self.FORMAT,
                                          channels=self.CHANNELS,
                                          rate=self.RATE,
                                          input=True,
                                          input_device_index=device_index,
                                          frames_per_buffer=self.CHUNK)
        except Exception as e:
            logging.error(f"Failed to open stream: {e}")
            self.stream = None

    def read_data(self):
        """
        Reads audio data from the stream.

        Returns:
            bytes: The audio data.
        """
        if self.stream is not None:
            try:
                return self.stream.read(
                    self.CHUNK, exception_on_overflow=False)
            except IOError as e:
                logging.warning(f"Input overflowed: {e}")
                return None
        return None

    def stop_stream(self):
        """
        Stops the audio stream and terminates the PyAudio object
        """
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
