import pyaudio
import numpy as np
import os
import time

# Audio setup
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048
audio = pyaudio.PyAudio()

# Stream setup
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Initialize smoothing
smoothed_fft = np.zeros(CHUNK // 2)

# Determine the size of the terminal window
rows, columns = os.get_terminal_size()
max_bar_height = rows - 2

# Visualization logic
bar_count = columns  # Number of bars to match the width of the terminal window
bar_heights = np.zeros(bar_count, dtype=int)

# Buffer to hold the complete frame string
frame_buffer = ""

try:
    while True:
        # Get the audio data and apply the FFT
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        fft = np.abs(np.fft.fft(data * np.hamming(CHUNK)).real)[:CHUNK // 2]

        alpha = 0.2
        smoothed_fft = (alpha * smoothed_fft
                        + (1 - alpha) * fft)  # Apply smoothing
        max_fft = (np.max(smoothed_fft)
                   if np.max(smoothed_fft) > 0 else 1)  # Normalize

        # Calculate the height of each bar according to the FFT results
        log_scale_index = np.logspace(0, np.log10(len(smoothed_fft)),
                                      num=bar_count, endpoint=True,
                                      base=10).astype(int) - 1
        log_scale_index = np.unique(np.clip(log_scale_index, 0,
                                            # unique indices within bounds
                                            len(smoothed_fft)-1))

        for i in range(len(log_scale_index) - 1):
            bar_values = smoothed_fft[log_scale_index[i]:log_scale_index[i+1]]
            bar_height = (
                int(np.mean(bar_values) / max_fft * max_bar_height)
                if bar_values.size > 0 else 0
            )

            bar_heights[i] = bar_height

        # Clear the frame buffer
        frame_buffer = "\n".join("".join("█" if bar_heights[col] >= row else " "  # noqa: E501
                                         for col in range(bar_count - 1)) for row in range(max_bar_height - 1, -1, -1))  # noqa: E501

        # Clear the terminal and print the entire frame at once
        os.system('cls' if os.name == 'nt' else 'clear')
        print(frame_buffer, end="", flush=True)

        time.sleep(0.07)  # control frame rate
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
