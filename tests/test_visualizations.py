"""
test_visualizations.py

Unit tests for vertical_visualizer, horizontal_left_to_right_visualizer,
and horizontal_right_to_left_visualizer modules.
"""

import unittest
import sys
from unittest.mock import MagicMock, patch
import numpy as np
from threading import Event
import io

from audio_visualizer.visualizer_logic.audio_processing import (
    process_audio_visualization
)
from audio_visualizer.visualizer_logic.visualizer_drawer import (
    draw_horizontal_ltr, draw_horizontal_rtl, draw_vertical
)

sys.modules['pynput'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()


# Mocking os.system to prevent clearing the screen
@patch('os.system')
# Mocking os.get_terminal_size to control terminal size
@patch('os.get_terminal_size', return_value=(24, 80))
class TestVisualizations(unittest.TestCase):
    def setUp(self):
        # Create a mock stop event
        self.mock_stop_event = MagicMock(spec=Event)
        self.mock_stop_event.is_set.side_effect = [False, True]
        self.stream = MagicMock()
        self.chunk = 2048
        self.rate = 44100
        self.alpha = 0.4
        self.window = np.hanning(self.chunk)
        self.theme = None

        # Simulate some audio data (sine wave)
        t = np.linspace(0, self.chunk / self.rate, self.chunk)
        sine_wave = (np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)
        audio_data = np.vstack((sine_wave, sine_wave)
                               ).T.tobytes()  # Create stereo data
        self.stream.read_data.side_effect = [audio_data, None]

    def test_visualize_vertical(self, mock_get_terminal_size, mock_system):
        """Test visualizing audio data vertically."""
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            process_audio_visualization(
                stream=self.stream,
                chunk=self.chunk,
                rate=self.rate,
                alpha=self.alpha,
                window=self.window,
                stop_event=self.mock_stop_event,
                draw_function=draw_vertical,
                theme=self.theme
            )
            output = fake_stdout.getvalue()
        self.assertIn('█', output)
        self.assertGreater(len(output), 0)

    def test_visualize_horizontal_left_to_right(self, mock_get_terminal_size,
                                                mock_system):
        """Test visualizing audio data horizontally from left to right."""
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            process_audio_visualization(
                stream=self.stream,
                chunk=self.chunk,
                rate=self.rate,
                alpha=self.alpha,
                window=self.window,
                stop_event=self.mock_stop_event,
                draw_function=draw_horizontal_ltr,
                theme=self.theme
            )
            output = fake_stdout.getvalue()
        self.assertIn('█', output)
        self.assertGreater(len(output), 0)

    def test_visualize_horizontal_right_to_left(self, mock_get_terminal_size,
                                                mock_system):
        """Test visualizing audio data horizontally from right to left."""
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            process_audio_visualization(
                stream=self.stream,
                chunk=self.chunk,
                rate=self.rate,
                alpha=self.alpha,
                window=self.window,
                stop_event=self.mock_stop_event,
                draw_function=draw_horizontal_rtl,
                theme=self.theme
            )
            output = fake_stdout.getvalue()
        self.assertIn('█', output)
        self.assertGreater(len(output), 0)


if __name__ == '__main__':
    unittest.main()
