#!/usr/bin/env python

import os
import setuptools


# Absolute pathname of directory containing this `setup.py' script.
SOURCE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Absolute pathname of file containing generated version number.
VERSION_FILE = os.path.join(SOURCE_DIRECTORY, 'VERSION')


def read_version_number():
    """Get the version number from a text file."""
    with open(VERSION_FILE) as handle:
        return handle.read().strip()


tests_require = [
    'pytest-pep8==1.0.5',
    'pytest==2.5.1',
]

setuptools.setup(
    name='balrog',
    packages=setuptools.find_packages(),
    version=read_version_number(),
    install_requires=[
    ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    }
)
