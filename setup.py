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

# Get the long description from the README file
long_description = read('README.rst')

__version__ = "2.0.2" 

extra_compile_args = []
extra_link_args = []
library_dirs = []
libraries = []
include_dirs = []

if 'linux' in sys.platform:
    extra_compile_args = ["-fopenmp","-std=c++11", "-fPIC"]
    extra_link_args = ["-std=c++11","-fopenmp",]
    libraries = ["pthread", "X11"]

elif 'darwin' in sys.platform:
    # Newer versions of MacOS X come with an incomplete XLib.h
    os.environ['CC'] = 'clang -I/usr/X11R6/include -L/usr/X11R6/lib'
    extra_compile_args = ["-std=c++11", "-fPIC", "-stdlib=libc++", "-mmacosx-version-min=10.15"]
    extra_link_args = ["-std=c++11", "-mmacosx-version-min=10.15"]
    include_dirs = ["/usr/X11R6/include"]
    library_dirs = ["/usr/X11R6/lib"]
    libraries = ["pthread", "X11"]

elif sys.platform == 'win32':
#    extra_compile_args = ["-Zi", "/Od"]
    extra_compile_args = ["/MT", "/openmp", "/std:c++17"]
    extra_link_args = ["/NODEFAULTLIB:libcmt"]
    libraries = ["gdi32", "user32", "shell32"]

else:
    raise RuntimeError("pycimg is not yet supported on platform '{}'".format(sys.platform))


if os.path.exists('conanbuildinfo.json'):
    with open('conanbuildinfo.json', 'r') as f:
        bi = json.loads(f.read())
        for d in bi['dependencies']:
            include_dirs.extend(d['include_paths'])
            library_dirs.extend(d['lib_paths'])
            libraries.extend(d['libs'])
            for define in d['defines']:
                if sys.platform == 'win32':
                    extra_compile_args.append(f"/D{define}")
                else:
                    extra_compile_args.append(f"-D{define}")
                
else:
    print('Not using conan packages.')

ext_modules = [
    Pybind11Extension("pycimg.cimg_bindings",
        ["src/cimg_bindings.cpp"],
        include_dirs = include_dirs + ['./thirdparty/CImg-3.1.6'],
        library_dirs = library_dirs,
        libraries = libraries,
        extra_compile_args = extra_compile_args,
        extra_link_args = extra_link_args,
        # Example: passing in the version to the compiled code
        define_macros = [('VERSION_INFO', __version__)]
        ),
]

setup(
    name="pycimg",
    version=__version__,
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
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11"
            ],
    keywords="image processing library", 
    packages=find_packages(exclude=['tests', 'docs']),
    ext_modules=ext_modules,
    install_requires=["numpy"],
    extras_require={"test": "pytest"},
    cmdclass={"build_ext": build_ext},
    zip_safe=False
)

