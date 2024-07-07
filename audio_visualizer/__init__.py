import sys

# Check if the --version flag is used and handle it directly
if '--version' in sys.argv:
    print("audio_visualizer 1.0.1")
    sys.exit(0)

from audio_visualizer.visualizer import AudioVisualizer
import argparse
import logging
import logging.handlers
import time
import os
from sys import platform
from lupa import LuaRuntime


# Define a function to determine the appropriate log file path
def get_log_path():
    if platform == "win32":  # Windows
        log_dir = os.path.join(os.getenv("APPDATA"), "audio_visualizer")
    elif platform in ("linux", "linux2", "darwin"):  # Unix and macOS
        log_dir = os.path.join(
            os.getenv("HOME"), ".config", "audio_visualizer")
    else:
        # Default to current directory if unknown platform
        log_dir = os.getcwd()

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Create the directory if it does not exist

    return os.path.join(log_dir, "debug.log")


# Configure logging
log_file_path = get_log_path()

# Clear existing handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Setup log rotation
logger = logging.getLogger()
handler = logging.handlers.RotatingFileHandler(
    log_file_path, maxBytes=1048576, backupCount=5)  # 1 MB
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create a console handler to log ERROR
# and higher level messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Get the root logger and add the console handler
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

# Disable propagation for the logger to prevent duplicate logging in console
logger.propagate = False


def load_config():
    """
    Dynamically loads configuration settings from a Lua file
    based on the operating system.
    The function checks common configuration directories on
    Linux, macOS, and Windows.

    Returns:
        dict: A dictionary containing configuration settings loaded
        from the Lua file.
    """
    config_filename = "config.lua"
    paths = []
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        # Unix-like systems: look in the user's home directory config folder
        paths.append(os.path.join(os.getenv("HOME"), ".config",
                     "audio_visualizer", config_filename))
    elif platform == "win32":
        # Windows: look in AppData folder
        paths.append(os.path.join(os.getenv("APPDATA"),
                     "audio_visualizer", config_filename))

    # Check the current directory last
    paths.append(os.path.join(os.getcwd(), config_filename))

    # Try each path in sequence
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r') as file:
                lua = LuaRuntime(unpack_returned_tuples=True)
                config_script = file.read()
                return lua.execute(config_script)

    # If no config file is found, log the error and return default settings
    logging.warning(f"No configuration file found in expected locations: {
        paths}. Using default settings.")

    # Alt works better for windows and ctrl works better for unix based
    default_modifier = 'alt' if sys.platform == 'win32' else 'ctrl'
    return {
        'key_binds': {
            'modifier_key': default_modifier,
            'keys': {
                'j': 'vertical',
                'h': 'horizontal-ltr',
                'l': 'horizontal-rtl'
            }
        },
        'settings': {
            'default_mode': 'vertical',
            'alpha': 0.4,
            'chunk_size': 2048,
            'sample_rate': 44100
        }
    }


def main():
    """Entry point for the audio visualizer command line interface."""
    config = load_config()

    parser = argparse.ArgumentParser(description="Terminal Audio Visualizer")
    parser.add_argument(
        "--mode",
        choices=["vertical", "horizontal-ltr", "horizontal-rtl"],
        default=config['settings']['default_mode'],
        help="Choose visualization mode: vertical or horizontal",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=config['settings']['alpha'],
        help="Smoothing factor for FFT; default is 0.4.",
    )
    parser.add_argument(
        "--chunk",
        type=int,
        default=config['settings']['chunk_size'],
        help="Number of frames per buffer; default is 2048",
    )
    parser.add_argument(
        "--rate",
        type=int,
        default=config['settings']['sample_rate'],
        help="Sampling rate; default is 44100",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="audio_visualizer 1.0.1",
        help="Show program's version number and exit."
    )
    args = parser.parse_args()

    visualizer = AudioVisualizer(
        mode=args.mode,
        alpha=args.alpha,
        chunk=args.chunk,
        rate=args.rate,
        key_binds=config['key_binds'],
        theme=config['themes'],
        audio_source=config['settings']['audio_source']
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
