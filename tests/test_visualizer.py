import unittest
import numpy as np
from unittest.mock import patch, MagicMock
from audio_visualizer.visualizer import AudioVisualizer


class TestAudioVisualizer(unittest.TestCase):
    @patch('audio_visualizer.visualizer.pyaudio.PyAudio')
    def setUp(self, MockPyAudio):
        mock_stream = MagicMock()
        mock_pyaudio_instance = MockPyAudio.return_vale
        mock_pyaudio_instance.open.return_value = mock_stream

        self.visualizer = AudioVisualizer(mode='vertical')
        self.visualizer.stream = mock_stream

    def test_initialization(self):
        self.assertEqual(self.visualizer.mode, 'vertical')
        self.assertEqual(self.visualizer.RATE, 44100)
        self.assertEqual(self.visualizer.CHUNK, 2048)
        self.assertIsInstance(self.visualizer.smoothed_fft, np.ndarray)

    def test_hamming_window(self):
        self.assertEqual(len(self.visualizer.window), self.visualizer.CHUNK)
        self.assertTrue(np.all(self.visualizer.window <= 1))

    def test_cleanup(self):
        try:
            self.visualizer.cleanup()
        except Exception as e:
            self.fail(f"cleanup method raised an exception: {e}")

    def test_fft_calculation(self):
        data = (np.random.randint(-32768, 32767, self.visualizer.CHUNK)
                .astype(np.int16))
        windowed_data = data * self.visualizer.window
        fft = np.abs(np.fft.fft(windowed_data).real)
        self.assertEqual(len(fft), self.visualizer.CHUNK)


if __name__ == '__main__':
    unittest.main()
