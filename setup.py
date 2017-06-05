from setuptools import setup, find_packages
import unittest

def all_tests():
  test_loader = unittest.TestLoader()
  test_suite = test_loader.discover('tests', pattern='test_*.py')
  return test_suite

setup(
  name='tele',
  version='0.1.0a2',
  packages=find_packages(),
  author='Aiden Nibali',
  description='Telemetry for PyTorch',
  test_suite='setup.all_tests',
)
