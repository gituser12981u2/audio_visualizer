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
        mock_stream = MagicMock()
        mock_pyaudio_instance = MockPyAudio.return_value
        mock_pyaudio_instance.open.return_value = mock_stream

        self.audio_capture = AudioCapture()
        self.audio_capture.stream = mock_stream

    def test_initialization(self):
        """
        Test that the AudioCapture object is initialized correctly.
        """
        self.assertEqual(self.audio_capture.RATE, 44100)
        self.assertEqual(self.audio_capture.CHUNK, 2048)
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
            'maxInputChannels': 2, 'maxOutputChannels': 2}
        self.audio_capture.start_stream(device_name='Test Device')
        self.assertIsNotNone(self.audio_capture.stream)

    def test_read_data(self):
        """
        Test reading data from the audio stream.
        """
        self.audio_capture.stream.read.return_value = b'\x00' * 2048
        data = self.audio_capture.read_data()
        self.assertIsNotNone(data)

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
