from setuptools import setup, Extension, distutils, find_packages
from Cython.Build import cythonize
import codecs
import os
import re
import sys

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

extra_compile_args = []
extra_link_args = []
library_dirs = []
libraries = []
include_dirs = []

if 'linux' in sys.platform:
    extra_compile_args = ["-std=c++11", "-fPIC"]
    extra_link_args = ["-std=c++11"]
    library_dirs = ["./thirdparty/zlib/build",
                    "./thirdparty/libjpeg-turbo/build/.libs",
                    "./thirdparty/libpng/build",
                    "./thirdparty/libtiff/build/libtiff"]
    libraries = ["pthread", "X11", ":libz.a", ":libjpeg.a", ":libpng.a", ":libtiff.a"]

elif 'darwin' in sys.platform:
    extra_compile_args = ["-std=c++11", "-stdlib=libc++", "-fPIC"]
    extra_link_args = ["-std=c++11",
                       "./thirdparty/zlib/build/libz.a",
                       "./thirdparty/libjpeg-turbo/build/.libs/libjpeg.a",
                       "./thirdparty/libpng/build/libpng.a",
                       "./thirdparty/libtiff/build/libtiff/libtiff.a"]
    include_dirs = ["/usr/X11R6/include"]
    library_dirs = ["/usr/X11R6/lib"]
    libraries = ["pthread", "X11"]

elif sys.platform == 'win32':
#    extra_compile_args = ["-Zi", "/Od"]
    extra_compile_args = ["/MD"]
    extra_link_args = ["/NODEFAULTLIB:libcmt"]
    library_dirs = ["./thirdparty/zlib/build/Release",
                    "./thirdparty/libpng/build/Release",
                    "./thirdparty/libjpeg-turbo/build/Release",
                    "./thirdparty/libtiff/build/libtiff/Release"]
    libraries = ["gdi32", "user32", "shell32", "zlibstatic", "libpng16_static", "jpeg-static", "tiff"]

else:
    raise RuntimeError("pycimg is not yet supported on platform '{}'".format(sys.platform))
                
ext = Extension("pycimg.pycimg", 
                sources=["./src/pycimg.pyx"],
                include_dirs=include_dirs + ["./src",
                        "./thirdparty/half/include",
                        "./thirdparty/CImg-2.0.4",
                        "./thirdparty/zlib",
                        "./thirdparty/libpng",
                        "./thirdparty/libjpeg-turbo",
                        "./thirdparty/libtiff/libtiff"],
                library_dirs=library_dirs,
                libraries=libraries,
                language="c++",
                extra_compile_args=extra_compile_args,
                extra_link_args=extra_link_args)

setup(name="pycimg",
      version=find_version("pycimg", "__init__.py"),
      description="Python extension for the CImg library.",
      long_description=long_description,
      url="https://github.com/d0m3nik/pycimg",
      author="Dominik Brugger",
      license="GPL-3.0",
      classifiers=[
              "Development Status :: 3 - Alpha",
              "Intended Audience :: Developers",
              "Topic :: Software Development :: Libraries",
              "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3.5",
              "Programming Language :: Python :: 3.6"
              ],
      keywords="image processing library",
      install_requires=["numpy"],
      python_requires=">=3.5",
      packages=find_packages(exclude=['test', 'docs']),
      ext_modules=cythonize(ext))
