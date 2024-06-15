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
        chunk (int): Number of audio samples per buffer.
        rate (int): Sample rate (samples per second).
        channels (int): Number of audio channels
        FORMAT (int): Audio format (16-bit PCM).
        audio (pyaudio.PyAudio): PyAudio object for audio streaming.
        stream (pyaudio.Stream): Stream object for audio input.
    """

    def __init__(self, chunk=2048, rate=44100, channels=2):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self.CHUNK = chunk
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start_stream(self, device_name=None):
        """
        Starts the audio stream. Selects the specified device if provided.

        Args:
            device_name (str): The name of the audio input device to use.
        """
        # Handle default device selection based on platform
        if platform.system() == 'Darwin' and device_name is None:
            device_name = 'BlackHole 2ch'

        # List available audio devices
        self.device_index = None
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            logging.info(f"Device {i}: {info['name']}")
            if device_name and device_name in info['name']:
                self.device_index = i
                logging.info(f"Selected Device {i}: {info['name']}")
                logging.info(f"Device {i} Max Input Channels: {
                             info['maxInputChannels']}")
                logging.info(f"Device {i} Max Output Channels: {
                             info['maxOutputChannels']}")

        # Use the default input device if no specific device name is provided
        if self.device_index is None:
            logging.info(
                "No specific device selected, using default input device.")
            self.device_index = self.audio.get_default_input_device_info()[
                'index']

        try:
            self.stream = self.audio.open(format=self.FORMAT,
                                          channels=self.CHANNELS,
                                          rate=self.RATE,
                                          input=True,
                                          input_device_index=self.device_index,
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
                data = self.stream.read(
                    self.CHUNK, exception_on_overflow=False)
                return data
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
