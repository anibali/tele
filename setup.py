from setuptools import setup

setup(
    name='tele',
    version='0.2.0',
    packages=['tele', 'tele.console', 'tele.folder', 'tele.showoff'],
    author='Aiden Nibali',
    description='Telemetry for PyTorch',
    test_suite='tests',
    install_requires=[
        'graphviz',
        'h5py',
        'numpy',
        'Pillow',
        'requests',
        'torch',
        'torchvision',
    ],
)
