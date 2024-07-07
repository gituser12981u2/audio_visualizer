"""
This script is used to set up the package distribution
for the 'audio_visualizer' project.

It specifies the package details, dependencies, and entry points
needed for the distribution and installation.
"""

from setuptools import setup, find_packages

setup(
    name="audio_visualizer",
    version="1.0.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    # List of dependencies installed via pip install -e .[dev]
    install_requires=[
        "autopep8==2.2.0",
        "flake8==7.0.0",
        "lupa==2.2",
        "mccabe==0.7.0",
        "numpy==1.26.4",
        "PyAudio==0.2.14",  # Handles audio operations
        "pycodestyle==2.11.1",
        "pyflakes==3.2.0",
        "pynput==1.7.6",  # Monitor and control user input devices
        "six==1.16.0"  # Python 2 and 3 compatibility utilities
    ],
    extras_require={
        # Additional dependencies for macOS platform
        ':sys_platform=="darwin"': [
            "pyobjc-core==10.3.1",  # Objective-C bridge
            "pyobjc-framework-ApplicationServices==10.3.1",
            "pyobjc-framework-Cocoa==10.3.1",
            "pyobjc-framework-CoreText==10.3.1",
            "pyobjc-framework-Quartz==10.3.1",
        ],
        # Dependencies only for CUDA or ROCm enabled GPU's
        'gpu': ['cupy==13.2.0']
    },
    # Defines the entry point for the console script.
    entry_points={
        "console_scripts": ["audio-visualizer=audio_visualizer.__init__:main"]
    },
    author="gituser12981u2",
    author_email="squarer.human-0t@icloud.com",
    description="A janky, yet charming, terminal audio visualizer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gituser12981u2/audio_visualizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
