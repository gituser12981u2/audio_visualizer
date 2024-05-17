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

# Hamming window
window = np.hamming(CHUNK)

try:
    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        # Apply window function
        windowed_data = data * window
        fft = np.abs(np.fft.fft(windowed_data).real)
        fft = fft[:int(len(fft)/2)]  # keep only the first half
        
        # Smoothing factor
        alpha = 0.2
        smoothed_fft = alpha * smoothed_fft + (1 - alpha) * fft
        
        max_fft = np.max(smoothed_fft) if np.max(smoothed_fft) > 0 else 1  # Avoid division by zero

        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Visualization logic
        bar_count = 75
        indices = np.logspace(0, np.log10(len(smoothed_fft)), num=bar_count + 1, endpoint=True, base=10).astype(int) - 1
        indices = np.unique(np.clip(indices, 0, len(smoothed_fft)-1))  # Ensure unique indices and within bounds

        for i in range(len(indices)-1):
            bar_values = smoothed_fft[indices[i]:indices[i+1]]
            if bar_values.size > 0:
                # Apply a weighting decreasing with frequency
                weights = np.linspace(1, 0.1, num=len(bar_values))
                bar_value = np.average(bar_values, weights=weights)
            else:
                bar_value = 0

            # Calculate the number of characters to print
            num_chars = int(np.sqrt(bar_value / max_fft) * 50) if not np.isnan(bar_value) else 0
            print('█' * num_chars)  # Normalize and apply sqrt to enhance visibility

        time.sleep(0.07)  # control frame rate
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
