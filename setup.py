"""
setup.py
"""

from setuptools import setup, find_packages

setup(
    name="audio_visualizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "autopep8==2.2.0",
        "flake8==7.0.0",
        "mccabe==0.7.0",
        "numpy==1.26.4",
        "PyAudio==0.2.14",
        "pycodestyle==2.11.1",
        "pyflakes==3.2.0",
        "pynput==1.7.7",
        "pyobjc-core==10.3.1",
        "pyobjc-framework-ApplicationServices==10.3.1",
        "pyobjc-framework-Cocoa==10.3.1",
        "pyobjc-framework-CoreText==10.3.1",
        "pyobjc-framework-Quartz==10.3.1",
        "six==1.16.0"
    ],
    entry_points={
        "console_scripts": ["audio-visualizer=audio_visualizer.__init__:main"]
    },
    author="gituser12981u2",
    author_email="",
    description="A janky, yet charming, terminal audio visualizer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gituser12981u2/audio_visualizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
