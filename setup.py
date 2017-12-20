from setuptools import setup, find_packages

setup(
    name='tele',
    version='0.2.0',
    packages=find_packages(),
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
        'torchnet',
        'torchvision',
        'pyshowoff==0.1.0a1',
    ],
    dependency_links=[
        'git+https://github.com/anibali/pyshowoff.git@cfef2201547cbe3f8fb1e74ff62336d8d397d1dd#egg=pyshowoff-0.1.0a1',
    ]
)
