"""
test_audio_capture.py

Unit tests for audio_capture.py module.
"""

import unittest
from unittest.mock import patch, MagicMock
from audio_visualizer.audio_capture import AudioCapture


class TestAudioCapture(unittest.TestCase):
    """
    Test cases for AudioCapture class.
    """
    @patch('audio_visualizer.audio_capture.pyaudio.PyAudio')
    def setUp(self, MockPyAudio):
        """
        Set up the test environment.
        This method patches PyAudio and creates a mock stream.
        """
        self.mock_stream = MagicMock()
        mock_pyaudio_instance = MockPyAudio.return_value
        mock_pyaudio_instance.open.return_value = self.mock_stream

        # Set parameters for testing
        self.rate = 44100
        self.chunk = 2048
        self.device_name = 'Test Device'

        self.audio_capture = AudioCapture(
            chunk=self.chunk, rate=self.rate, device_name=self.device_name)
        self.audio_capture.stream = self.mock_stream

    def test_initialization(self):
        """
        Test that the AudioCapture object is initialized correctly.
        """
        self.assertEqual(self.audio_capture.RATE, self.rate)
        self.assertEqual(self.audio_capture.CHUNK, self.chunk)
        self.assertEqual(self.audio_capture.CHANNELS, 2)

    def test_start_stream_default_device(self):
        """
        Test starting the audio stream using the default device.
        """
        self.audio_capture.start_stream()
        self.assertIsNotNone(self.audio_capture.stream)

    @patch('audio_visualizer.audio_capture.pyaudio.PyAudio.get_device_info_by_index')  # noqa: E501
    def test_start_stream_specific_device(self, mock_get_device_info_by_index):
        """
        Test starting the audio stream using the default device.
        """
        mock_get_device_info_by_index.return_value = {
            'name': 'Test Device',
            'maxInputChannels': 2, 'maxOutputChannels': 2
        }
        self.audio_capture.start_stream()
        self.assertIsNotNone(self.audio_capture.stream)

    def test_read_data(self):
        """
        Test reading data from the audio stream.
        """
        self.audio_capture.start_stream()
        self.mock_stream.read.return_value = b'\x00' * \
            (self.chunk * 2)  # Stereo data

        data = self.audio_capture.read_data()
        self.assertIsNotNone(data)
        self.assertEqual(len(data), self.chunk * 2)

    def test_stop_stream(self):
        """
        Test stopping the audio stream.
        """
        try:
            self.audio_capture.stop_stream()
        except Exception as e:
            self.fail(f"stop_stream method raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()
