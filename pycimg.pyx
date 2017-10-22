from libc.stdint cimport int8_t, int16_t, int32_t 
from libc.stdint cimport uint8_t, uint16_t, uint32_t
import numpy as np

## Supported data types
ctypedef int8_t   int8
ctypedef int16_t  int16
ctypedef int32_t  int32
ctypedef uint8_t  uint8
ctypedef uint16_t uint16
ctypedef uint32_t uint32
ctypedef float    float32
ctypedef double   float64

cdef extern from "cimg_ext.h" namespace "cimg_library":


    cdef cppclass CImg[T]:
        # Constructors
        CImg() except+
        CImg(const char* const filename) except +

        CImg& load(const char* const filename)
#        CImg& load_cimg(const char* const filename, const char axis='z', 
#                const float align=0)

        # Operators
        T& operator()(const unsigned int x) 
        T& operator()(const unsigned int x, const unsigned int y) 
        T& operator()(const unsigned int x, const unsigned int y, 
                const unsigned int z) 
        T& operator()(const unsigned int x, const unsigned int y, 
                const unsigned int z, const unsigned int c) 

        CImg& operator+(const T value)

        const CImg& display() except + 

        # Instance characteristics
        int width() const
        int height() const
        int depth() const
        int spectrum() const
        unsigned long size() const
        T* data()
        CImg& sqr()
        CImg& sqrt()
        CImg& exp()
        CImg& log()
        CImg& log2()
        CImg& log10()
        CImg& abs()
        CImg& sign()
        CImg& cos()
        CImg& sin()
        CImg& sinc()
        CImg& tan()
        CImg& sinh()
        CImg& tanh()
        CImg& acos()
        CImg& asin()
        CImg& atan()
        CImg& atan2(const CImg& img)
        CImg& mul(const CImg& img)
        CImg& div(const CImg& img)
        CImg& pow(const double p)
        
        # ...
        CImg& noise(const double sigma, const unsigned int noise_type)
        CImg& normalize(const T& min_value, const T& max_value)

    # Utility function for loading CImg[T] from a cimg
    # file with half precision floats
    CImg[T] load_float16[T](const char* const filename)


# The following files are generated from pycimg_template.pyx
# by the generate.py script
include "pycimg_int8.pyx"
include "pycimg_int16.pyx"
include "pycimg_int32.pyx"

include "pycimg_uint8.pyx"
include "pycimg_uint16.pyx"
include "pycimg_uint32.pyx"

include "pycimg_float32.pyx"
include "pycimg_float64.pyx"
