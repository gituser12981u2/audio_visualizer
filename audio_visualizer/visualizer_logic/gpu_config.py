import logging


def get_computation_library():
    """
    Determines the appropriate computation library
    based on system capabilities.

    Attempts to use CuPy if it's installed and a CUDA-compatible GPU
    is available.
    Falls back to NumPy if CuPy is not available or no CUDA GPU is detected.
    """
    try:
        # Attempts to import CuPy
        import cupy as xp  # type: ignore
        if xp.cuda.runtime.getDeviceCount() > 0:
            logging.info("Using CuPy for GPU acceleration.")
            return xp
        else:
            # Fallback to NumPy if no CUDA GPU
            import numpy as np
            logging.info(
                "No GPU with CUDA cores detected. Using NumPy instead of CuPy."
            )
            return np
    except ImportError:
        # Fallback to NumPy if CuPy not installed
        import numpy as np
        logging.info(
            "No GPU with CUDA cores detected. Using NumPy instead of CuPy.")
        return np


# Initialize the computation library when the module is loaded.
computation_lib = get_computation_library()
