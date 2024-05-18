from audio_visualizer.visualizer import AudioVisualizer
import logging

logging.basicConfig(level=logging.DEBUG)


def main():
    """Entry point for the audio visualizer command line interface."""
    import argparse

    parser = argparse.ArgumentParser(description="Terminal Audio Visualizer")
    parser.add_argument(
        "--mode",
        choices=["vertical", "horizontal"],
        default="vertical",
        help="Choose visualization mode: vertical or horizontal",
    )  # noqa: E501
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.4,
        help="Smoothing factor for FFT; default is 0.4. Raise if you want it to be less charming",  # noqa: E501
    )
    parser.add_argument(
        "--chunk",
        type=int,
        default=2048,
        help="Number of frames per buffer; default is 2048",
    )  # noqa: E501
    parser.add_argument(
        "--rate",
        type=int,
        default=44100,
        help="Sampling rate; default is 44100",  # noqa: E501
    )
    parser.add_argument(
        "--bar_count",
        type=int,
        default=75,
        help="Number of bars in the visualization; default is 75",
    )  # noqa: E501
    args = parser.parse_args()

    visualizer = AudioVisualizer(
        mode=args.mode,
        alpha=args.alpha,
        chunk=args.chunk,
        rate=args.rate,
        bar_count=args.bar_count,
    )
    visualizer.start()


if __name__ == '__main__':
    main()
