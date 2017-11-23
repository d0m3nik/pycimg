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
    libraries = ["pthread", "X11", "z", "jpeg", "png"]

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
      ext_modules=cythonize(ext))
