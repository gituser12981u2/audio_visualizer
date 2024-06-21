"""
test_visualizations.py

Unit tests for vertical_visualizer, horizontal_left_to_right_visualizer,
and horizontal_right_to_left_visualizer modules.
"""

from audio_visualizer.horizontal_right_to_left_visualizer import (
    visualize_horizontal_right_to_left)
from audio_visualizer.horizontal_left_to_right_visualizer import (
    visualize_horizontal_left_to_right)
from audio_visualizer.vertical_visualizer import visualize_vertical
import unittest
import sys
from unittest.mock import MagicMock, patch
import numpy as np
from threading import Event
import io

sys.modules['pynput'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()


@patch('audio_visualizer.vertical_visualizer.os.get_terminal_size')
# Mock os.system to prevent clearing the screen
@patch('audio_visualizer.vertical_visualizer.os.system')
# Mock time.sleep to speed up the test
@patch('audio_visualizer.vertical_visualizer.time.sleep')
# Mock entire pynput module
@patch('audio_visualizer.visualizer.keyboard', MagicMock())
class TestVisualizes(unittest.TestCase):
    def setUp(self):
        # Create a mock stop event
        self.mock_stop_event = MagicMock(spec=Event)
        self.mock_stop_event.is_set.return_value = False
    """
    Test cases for visualization functions.
    """

    def test_visualize_vertical(self, mock_sleep,
                                mock_os_system, mock_get_terminal_size):
        """
        Test cases for the visualize_vertical function.

        This method mocks os.get_terminal_size to control terminal size,
        os.system to prevent clearing the screen,
        and time.sleep to speed up the test.
        """
        # Mock terminal size
        mock_get_terminal_size.return_value = (24, 80)

        # Create a mock stream
        mock_stream = MagicMock()

        # Simulate some audio data (sine wave)
        sample_rate = 44100
        chunk = 1024
        t = np.linspace(0, chunk / sample_rate, chunk)
        sine_wave = (np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)
        audio_data = np.vstack((sine_wave, sine_wave)
                               ).T.tobytes()  # Create stereo data

        # Configure the mock to continuously return the audio data then None
        mock_stream.read_data = MagicMock(
            side_effect=[audio_data, audio_data, None])

        # Parameters for the visualizer
        rate = 44100
        alpha = 0.5
        window = np.hanning(chunk)
        smoothed_fft = np.zeros(chunk // 2)

        # Capture the output of the visualizer
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            try:
                visualize_vertical(mock_stream, chunk, rate,
                                   alpha, window, smoothed_fft,
                                   self.mock_stop_event)
            except StopIteration:
                pass  # Handle StopIteration gracefully in test

        output = fake_stdout.getvalue()
        # Check that the visual output contains bars
        self.assertIn('█', output)
        self.assertGreater(len(output), 0)  # Check that there is some output

    def test_visualize_horizontal_left_to_right(self, mock_sleep,
                                                mock_os_system,
                                                mock_get_terminal_size):
        """
        Test the visualize_horizontal_left_to_right function.

        This method mocks os.get_terminal_size to control terminal size,
        os.system to prevent clearing the screen,
        and time.sleep to speed up the test.
        """
        # Mock terminal size
        mock_get_terminal_size.return_value = (24, 80)

        # Create a mock stream
        mock_stream = MagicMock()

        # Simulate some audio data (sine wave)
        sample_rate = 44100
        chunk = 1024
        t = np.linspace(0, chunk / sample_rate, chunk)
        sine_wave = (np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)
        audio_data = np.vstack((sine_wave, sine_wave)
                               ).T.tobytes()  # Create stereo data

        # Configure the mock to continuously return the audio data then None
        mock_stream.read_data = MagicMock(
            side_effect=[audio_data, audio_data, None])

        # Parameters for the visualizer
        rate = 44100
        alpha = 0.5
        window = np.hanning(chunk)
        smoothed_fft = np.zeros(chunk // 2)

        # Capture the output of the visualizer
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            try:
                visualize_horizontal_left_to_right(
                    mock_stream, chunk, rate, alpha,
                    window, smoothed_fft, self.mock_stop_event)
            except StopIteration:
                pass  # Handle StopIteration gracefully in test

        output = fake_stdout.getvalue()
        # Check that the visual output contains bars
        self.assertIn('█', output)
        self.assertGreater(len(output), 0)  # Check that there is some output

    def test_visualize_right_to_left_horizontal(self, mock_sleep,
                                                mock_os_system,
                                                mock_get_terminal_size):
        """
        Test the visualize_horizontal_right_to_left function.

        This method mocks os.get_terminal_size to control terminal size,
        os.system to prevent clearing the screen,
        and time.sleep to speed up the test.
        """
        # Mock terminal size
        mock_get_terminal_size.return_value = (24, 80)

        # Create a mock stream
        mock_stream = MagicMock()

        # Simulate some audio data (sine wave)
        sample_rate = 44100
        chunk = 1024
        t = np.linspace(0, chunk / sample_rate, chunk)
        sine_wave = (np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)
        audio_data = np.vstack((sine_wave, sine_wave)
                               ).T.tobytes()  # Create stereo data

        # Configure the mock to continuously return the audio data then None
        mock_stream.read_data = MagicMock(
            side_effect=[audio_data, audio_data, None])

        # Parameters for the visualizer
        rate = 44100
        alpha = 0.5
        window = np.hanning(chunk)
        smoothed_fft = np.zeros(chunk // 2)

        # Capture the output of the visualizer
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            try:
                visualize_horizontal_right_to_left(
                    mock_stream, chunk, rate, alpha,
                    window, smoothed_fft, self.mock_stop_event)
            except StopIteration:
                pass  # Handle StopIteration gracefully in test

        output = fake_stdout.getvalue()
        # Check that the visual output contains bars
        self.assertIn('█', output)
        self.assertGreater(len(output), 0)  # Check that there is some output


if __name__ == '__main__':
    unittest.main()
