from setuptools import setup, find_packages

setup(
    name='audio_visualizer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pyaudio'
    ],
    entry_points={
        'console_scripts': [
            'audio-visualizer=audio_visualizer.__init__:main'
        ]
    },
    author='ME',
    author_email='your.email@example.com',
    description='A janky, yet charming, terminal audio visualizer',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

