"""
test_vertical_visualizer.py

Unit tests for the vertical_visualizer.py module.
"""

import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import io

# Correct import for visualize_vertical function
from audio_visualizer.vertical_visualizer import visualize_vertical


class TestVisualizeVertical(unittest.TestCase):
    """
    Test cases for the visualize_vertical function.
    """
    # Mock os.system to prevent clearing the screen
    @patch('audio_visualizer.vertical_visualizer.os.system')
    # Mock time.sleep to speed up the test
    @patch('audio_visualizer.vertical_visualizer.time.sleep')
    def test_visualize_vertical(self, mock_sleep, mock_os_system):
        """
        Test cases for the visualize_vertical function.
        """
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
        bar_count = 50
        window = np.hanning(chunk)
        smoothed_fft = np.zeros(chunk // 2)

        # Capture the output of the visualizer
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            try:
                visualize_vertical(mock_stream, chunk, rate,
                                   alpha, bar_count, window, smoothed_fft)
            except StopIteration:
                pass  # Handle StopIteration gracefully in test

        output = fake_stdout.getvalue()
        # Check that the visual output contains bars
        self.assertIn('█', output)
        self.assertGreater(len(output), 0)  # Check that there is some output


if __name__ == '__main__':
    unittest.main()
