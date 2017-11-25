from setuptools import setup, Extension, distutils
from Cython.Build import cythonize

platform = distutils.sys.platform

extra_compile_args = []
extra_link_args = []
library_dirs = []
libraries = []

if 'linux' in platform:
    extra_compile_args = ["-std=c++11", "-fPIC"]
    extra_link_args = ["-std=c++11"]
    library_dirs = ["./thirdparty/zlib/build", 
                    "./thirdparty/libjpeg-turbo/build/.libs", 
                    "./thirdparty/libpng/build" ]
    libraries = ["pthread", "X11", ":libz.a", ":libjpeg.a", ":libpng.a"]

elif platform == 'win32':
#    extra_compile_args = ["-Zi", "/Od"]
    extra_compile_args = ["/MD"]
    extra_link_args = ["/NODEFAULTLIB:libcmt"]
    library_dirs = ["./thirdparty/zlib/build/Release",
            "./thirdparty/libpng/build/Release",
            "./thirdparty/libjpeg-turbo/build/Release"
            ]
    libraries = ["gdi32", "user32", "shell32", "zlibstatic", "libpng16_static", "jpeg-static"]

else:
    raise RuntimeError("pycimg is not yet supported on platform '{}'".format(platform))
                
ext = Extension("pycimg", 
        sources = ["pycimg.pyx"],
        include_dirs = [".", 
                "./thirdparty/half/include", 
                "./thirdparty/CImg-2.0.4", 
                "./thirdparty/zlib",
                "./thirdparty/libpng",
                "./thirdparty/libjpeg-turbo"
                ],
        library_dirs = library_dirs,
        libraries = libraries,
        language = "c++",
        extra_compile_args = extra_compile_args,
        extra_link_args = extra_link_args)

setup(name="pycimg", 
      version="0.0.1a",
      description="Python extension for the CImg library",
      long_description="This package contains a single class CImg"\
                       "that provides access to the image processing"\
                       "methods of the C++ CImg library (http://www.cimg.eu).",
      url="https://github.com/d0m3nik/pycimg",
      author="Dominik Brugger",
      license="GPL-3.0",
      classifiers=[
              "Development Status :: 3 - Alpha",
              "Intended Audience :: Developers",
              "Topic :: Software Development :: Libraries",
              "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
              "Programming Language :: Python :: 3.4"
              ],
      keywords="image processing library",
      install_requires=["numpy"],
      python_requires="~=3.5",
      ext_modules=cythonize(ext))
