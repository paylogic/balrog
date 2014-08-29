#!/usr/bin/env python
"""Balrog library setup file."""

import os
import codecs
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


# Absolute pathname of directory containing this `setup.py' script.
SOURCE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Absolute pathname of file containing generated version number.
VERSION_FILE = os.path.join(SOURCE_DIRECTORY, 'VERSION')


def read_version_number():
    """Get the version number from a text file."""
    with open(VERSION_FILE) as handle:
        return handle.read().strip()


class ToxTestCommand(TestCommand):

    """Test command which runs tox under the hood."""

    def finalize_options(self):
        """Add options to the test runner (tox)."""
        TestCommand.finalize_options(self)
        self.test_args = ['--recreate']
        self.test_suite = True

    def run_tests(self):
        """Invoke the test runner (tox)."""
        # import here, cause outside the eggs aren't loaded
        import detox.main
        errno = detox.main.main(self.test_args)
        sys.exit(errno)

long_description = []

for text_file in ['README.rst', 'CHANGES.rst']:
    with codecs.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), text_file), encoding="utf-8") as f:
        long_description.append(f.read())

tests_require = [
    'pytest-pep8==1.0.5',
    'pytest==2.5.1',
]

setup(
    name="balrog",
    description="Python access control library.",
    long_description='\n'.join(long_description),
    author="Paylogic International",
    license="MIT license",
    author_email="developers@paylogic.com",
    url="https://github.com/paylogic/balrog",
    version=read_version_number(),
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ] + [("Programming Language :: Python :: %s" % x) for x in "2.6 2.7 3.4".split()],
    cmdclass={"test": ToxTestCommand},
    packages=["balrog"],
    tests_require=["detox"],

)
