#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is used to create the package we'll publish to PyPI.

.. currentmodule:: setup.py
.. moduleauthor:: Richard Julian <richard@rjulian.net>
"""

import importlib.util
import os
from pathlib import Path
from setuptools import setup, find_packages
from codecs import open  # Use a consistent encoding.
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

# Get the base version from the library.  (We'll find it in the `version.py`
# file in the src directory, but we'll bypass actually loading up the library.)
vspec = importlib.util.spec_from_file_location(
  "version",
  str(Path(__file__).resolve().parent /
      "scipio"/"version.py")
)
vmod = importlib.util.module_from_spec(vspec)
vspec.loader.exec_module(vmod)
version = getattr(vmod, "__version__")

# If the environment has a build number set...
if os.getenv("buildnum") is not None:
    # ...append it to the version.
    version = f"{version}.{os.getenv('buildnum')}"

setup(
    name='scipio',
    description="CLI tool to undertake cloud reconnaisance and attacks.",
    long_description=long_description,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version=version,
    install_requires=[
        # Include dependencies here
        "click>=7.0,<8"
    ],
    entry_points="""
    [console_scripts]
    scipio=scipio.cli:cli
    """,
    python_requires=">=0.0.1",
    license='MIT',  # noqa
    author='Richard Julian',
    author_email='richard@rjulian.net',
    # Use the URL to the github repo.
    url= 'https://github.com/rjulian/scipio',
    download_url=(
        f'https://github.com/rjulian/'
        f'scipio/archive/{version}.tar.gz'
    ),
    keywords=[
        # Add package keywords here.
    ],
    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      "Development Status :: 3 - Alpha",

      # Indicate who your project is intended for.
      "Intended Audience :: Developers",
      "Topic :: Software Development :: Libraries",

      # Pick your license.  (It should match "license" above.)
        # noqa
      """License :: OSI Approved :: MIT License""",
        # noqa
      # Specify the Python versions you support here. In particular, ensure
      # that you indicate whether you support Python 2, Python 3 or both.
      "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True
)
