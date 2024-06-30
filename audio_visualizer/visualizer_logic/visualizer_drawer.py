def draw_vertical(frame_buffer, cols, rows, scaled_fft):
    """
    Draws the audio data in a vertical visualization format.

    Args:
        frame_buffer (list): The buffer where the frame data is stored.
        cols (int): The number of columns in the terminal.
        rows (int): The number of rows in the terminal.
        scaled_fft (array): The scaled FFT data used to determine the height
        of the bars.
    """
    for col in range(min(cols, len(scaled_fft))):
        bar_height = scaled_fft[col]
        for row in range(rows - bar_height, rows):
            frame_buffer[row] = frame_buffer[row][:col] + \
                '█' + frame_buffer[row][col+1:]


def draw_horizontal_ltr(frame_buffer, cols, rows, scaled_fft):
    """
    Draws the audio data in a horizontal left-to-right visualization format.

    Args:
        frame_buffer (list): The buffer where the frame data is stored.
        cols (int): The number of columns in the terminal.
        rows (int): The number of rows in the terminal.
        scaled_fft (array): The scaled FFT data used to determine the height
        of the bars.
    """
    for row in range(min(rows, len(scaled_fft))):
        bar_width = scaled_fft[row]
        frame_buffer[row] = '█' * bar_width + ' ' * (cols - bar_width)


def draw_horizontal_rtl(frame_buffer, cols, rows, scaled_fft):
    """
    Draws the audio data in a horizontal right-to-left visualization format.

    Args:
        frame_buffer (list): The buffer where the frame data is stored.
        cols (int): The number of columns in the terminal.
        rows (int): The number of rows in the terminal.
        scaled_fft (array): The scaled FFT data used to determine the height
        of the bars.
    """
    for row in range(min(rows, len(scaled_fft))):
        bar_width = scaled_fft[row]
        frame_buffer[row] = ' ' * (cols - bar_width) + '█' * bar_width
