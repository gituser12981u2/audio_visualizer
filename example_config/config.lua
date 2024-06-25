return {
    key_binds = {
        -- The modifier key used for hotkeys. Possible values are 'ctrl', 'shift', 'alt'.
        -- Note: On macOS, using 'shift or 'alt' can alter teh character keys.
        -- For example, 'shift' + 'l' becomes 'L', and 'alt' + 'l' might result in a non-alphanumeric character '¬'.
        -- Users should adjust the 'keys' bindings accordingly if using 'shift' or 'alt'.
        modifier_key = 'ctrl',

        -- Defines the hotkeys for switching visualization modes.
        -- Ensure these keys match the output when combined with the modifier key, especially on macOS.
        keys = {  -- Hotkeys for mode-switcher (all are inherently prefaced with the 'ctrl' modifier key)
            j = 'vertical',  -- Hotkey for vertical visualization mode.
            h = 'horizontal-ltr',  -- Hotkey for horizonta left-to-right mode.
            l = 'horizontal-rtl'  -- Hotkey for horizontal right-to-left mode.
        },
    },
    settings = {
        default_mode = 'vertical',  -- The default visualization mode on startup.
        alpha = 0.4,  -- Smoothing factor for the Fast Fourier Transform (FFT).
        chunk_size = 2048,  -- Number of audio samples per buffer.
        sample_rate = 44100  -- Audio sampling rate in Hertz (samples per second).
    }
    -- Future settings for theming
    -- themes = {
    --     background_color = 'black',
    --     bar_color = 'white'
    -- }
}
