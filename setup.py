from distutils.core import setup, Extension
from Cython.Build import cythonize
import distutils.cmd
import distutils.log

class GenerateCommand(distutils.cmd.Command):
    """ Custom command to generate pycimg_<type>.pyx files."""
    description = 'generate pycimg_<type>.pyx files.'
    user_options = [('dtypes=', None, 'Data types to generate')]

    def initialize_options(self):
        """ Set default values for options."""
        self.dtypes = ['int8', 'int16', 'int32',
                      'uint8', 'uint16', 'uint32',
                      'float32', 'float64'
                    ]
    def finalize_options(self):
        """ Post-process options."""
        pass


    def run(self):
        """ Run command. """
        with open('pycimg_template.pyx') as f:
            code = f.read()
            #print(code)
            for dtype in self.dtypes:
                out = code.format(T = dtype)
                print(out)
                outname = 'pycimg_{}.pyx'.format(dtype)
                with open(outname, 'w') as fout:
                    fout.write(out)       

                


ext = Extension("pycimg", 
        sources = ["pycimg.pyx"], 
        include_dirs = [".", "./thirdparty/half/include", "./thirdparty/CImg-2.0.4"],
        language = "c++",
        extra_compile_args = ["-std=c++11"],
        extra_link_args = ["-std=c++11"],
        libraries = ["pthread", "X11"])

setup(name="pycimg", 
      ext_modules=cythonize(ext),
      cmdclass={'generate': GenerateCommand})
