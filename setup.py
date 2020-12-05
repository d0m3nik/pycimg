from setuptools import setup, find_packages

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir

import codecs
import os
import re
import sys
import json

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# Get the long description from the README file
long_description = read('README.rst')

version = find_version("pycimg.py")

os.environ['CC'] = 'clang -I /usr/X11R6/include -L /usr/X11R6/lib'
include_dirs = ['./thirdparty/CImg-2.9.4']

ext_modules = [
    Pybind11Extension("cimg_bindings",
        ["src/cimg_bindings.cpp"],
        include_dirs = include_dirs + ['/usr/X11R6/include'],
        library_dirs = ['/usr/X11R6/lib'],
        libraries = ['pthread', 'X11'],
        # Example: passing in the version to the compiled code
        define_macros = [('VERSION_INFO', version)]
        ),
]

setup(
    name="pycimg",
    version=version,
    description="Python extension for the CImg library.",
    long_description=long_description,
    author="Dominik Brugger",
    url="https://github.com/d0m3nik/pycimg",
    license="GPL-3.0",
    classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Libraries",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8"
            ],
    keywords="image processing library", 
    packages=find_packages(exclude=['tests', 'docs']),
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    cmdclass={"build_ext": build_ext},
    zip_safe=False
)

