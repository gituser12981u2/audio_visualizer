import unittest
import numpy as np
from audio_visualizer.visualizer import AudioVisualizer

class TestAudioVisualizer(unittest.TestCase):
    def setUp(self):
        self.visualizer = AudioVisualizer(mode='vertical')

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
        data = np.random.randint(-32768, 32767, self.visualizer.CHUNK).astype(np.int16)
        windowed_data = data * self.visualizer.window
        fft = np.abs(np.fft.fft(windowed_data).real)
        self.assertEqual(len(fft), self.visualizer.CHUNK)

    def test_visualize_vertical(self):
        # Mock the stream read to provide consisten data for testing
        original_read = self.visualizer.stream.read
        self.visualizer.stream.read = lambda x: np.random.randint(-32768, 32767, x).astype(np.int16).tobytes()
        try:
            self.visualizer.visualize_vertical()
        except KeyboardInterrupt:
            pass
        finally:
            self.visualizer.stream.read = original_read

if __name__ == '__main__':
    unittest.main()
