from gettext import install
from setuptools import setup, find_packages

setup(
    name='visual_novel',
    version='1.0',
    packages=find_packages(),
    install_requires=['tk', 'pillow'])
