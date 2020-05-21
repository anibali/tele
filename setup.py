from setuptools import setup

setup(
    name='tele',
    version='0.2.3',
    packages=['tele', 'tele.console', 'tele.folder', 'tele.showoff',
              'tele.sacred'],
    author='Aiden Nibali',
    description='Telemetry for PyTorch',
    test_suite='tests',
    install_requires=[
        'graphviz',
        'h5py',
        'numpy',
        'Pillow',
        'plotly',
        'requests',
        'torch',
        'torchvision',
    ],
)
