#!/usr/bin/env python
"""Balrog library setup file."""

import os
import codecs

from setuptools import setup

import balrog


long_description = []

for text_file in ['README.rst', 'CHANGES.rst']:
    with codecs.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), text_file), encoding="utf-8") as f:
        long_description.append(f.read())

setup(
    name="balrog",
    description="Python access control library.",
    long_description='\n'.join(long_description),
    author="Paylogic International",
    license="MIT license",
    author_email="developers@paylogic.com",
    url="https://github.com/paylogic/balrog",
    version=balrog.__version__,
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
    packages=["balrog"],
    tests_require=["tox"],

)
