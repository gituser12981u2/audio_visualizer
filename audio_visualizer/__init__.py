from audio_visualizer.visualizer import AudioVisualizer
import argparse
import logging
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("debug.log"),
                    ])


def main():
    """Entry point for the audio visualizer command line interface."""

    parser = argparse.ArgumentParser(description="Terminal Audio Visualizer")
    parser.add_argument(
        "--mode",
        choices=["vertical", "horizontal-ltr", "horizontal-rtl"],
        default="vertical",
        help="Choose visualization mode: vertical or horizontal",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.4,
        help="Smoothing factor for FFT; default is 0.4.",
    )
    parser.add_argument(
        "--chunk",
        type=int,
        default=2048,
        help="Number of frames per buffer; default is 2048",
    )
    parser.add_argument(
        "--rate",
        type=int,
        default=44100,
        help="Sampling rate; default is 44100",
    )
    args = parser.parse_args()

    visualizer = AudioVisualizer(
        mode=args.mode,
        alpha=args.alpha,
        chunk=args.chunk,
        rate=args.rate,
    )
    visualizer.start()

    try:
        while True:
            time.sleep(1)  # Keep the main thread active
    except KeyboardInterrupt:
        visualizer.stop()
        print("Visualization stopped by user")


if __name__ == '__main__':
    main()
