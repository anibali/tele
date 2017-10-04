from setuptools import setup, find_packages
import unittest

setup(
  name='tele',
  version='0.1.0a3',
  packages=find_packages(),
  author='Aiden Nibali',
  description='Telemetry for PyTorch',
  test_suite='tests',
  install_requires=[
    'graphviz',
    'h5py',
    'Pillow',
    'requests',
    'torch',
    'torchnet',
    'torchvision',
  ],
)
