from distutils.core import setup, Extension
from Cython.Build import cythonize
import distutils.cmd
import distutils.log

platform = distutils.sys.platform

extra_compile_args = []
extra_link_args = []
library_dirs = []
libraries = []

if platform == 'linux':
    extra_compile_args = ["-std=c++11"]
    extra_link_args = ["-std=c++11"]
    library_dirs = ["./thirdparty/zlib-1.2.11/build"]
    libraries = ["pthread", "X11", "z"]

elif platform == 'win32':
    library_dirs = ["./thirdparty/zlib-1.2.11/contrib/vstudio/vc14/x64/ZlibStatRelease"]
    libraries = ["gdi32", "user32", "shell32", "zlibstat"]

else:
    raise RuntimeError("pycimg is not yet supported on platform '{}'".format(platform))
                
ext = Extension("pycimg", 
        sources = ["pycimg.pyx"],
        include_dirs = [".", "./thirdparty/half/include", 
                "./thirdparty/CImg-2.0.4", "./thirdparty/zlib-1.2.11"],
        library_dirs = library_dirs,
        libraries = libraries,
        language = "c++",
        extra_compile_args = extra_compile_args,
        extra_link_args = extra_link_args)

setup(name="pycimg", 
      ext_modules=cythonize(ext))
