from distutils.core import setup
from setuptools import find_packages
import os

# Optional project description in README.md:
current_directory = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''
setup(

# Project name: 
name='headmouse',
 
packages=find_packages(),

version='1.0.7',

license='MIT',

description='An augmentative tool to use the mouse with the movement of the head.',

long_description=long_description,

long_description_content_type='text/markdown',

author='Ramiro Fontalva',

author_email='ramirofontalva@gmail.com',

url='https://github.com/rfontalva',

download_url='https://github.com/rfontalva/Headmouse',

keywords=["headmouse", "HeadMouse", "Headmouse", "augmentative", "image processing", "mouse"],

install_requires=[
    'dlib',
    'opencv-python',
    'pynput',
    'scipy',
    'numpy'
],

# https://pypi.org/classifiers/ 
classifiers=[
    'Development Status :: 4 - Beta', 
    'Topic :: Scientific/Engineering :: Image Processing', 
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: End Users/Desktop'
]
)
