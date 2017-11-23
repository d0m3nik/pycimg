from libcpp cimport bool
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
        const CImg& save(const char* const filename)

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

        # Mathmatical functions
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

        # Value manipulation
        CImg& fill(const T& val)
        CImg& noise(const double sigma, const unsigned int noise_type)
        CImg& normalize(const T& min_value, const T& max_value)
        CImg& normalize()
        CImg& norm(const int norm_type)
        CImg& cut(const T& min_value, const T& max_value)
        CImg& quantize(const unsigned int nb_levels, const bool keep_range)
        CImg& threshold(const T& value, const bool soft_threshold, 
                        const bool strict_threshold)
        CImg& histogram(const unsigned int nb_levels, const T& min_value,
                        const T& max_value)
        CImg& equalize(const unsigned int nb_levels, const T& min_value,
                       const T& max_value)
        CImg& index(const CImg& colormap, const float dithering, 
                    const bool map_indexes)
        CImg& map(const CImg& colormap, 
                  const unsigned int boundary_conditions)
        CImg& label(const bool is_high_connectivity, const float tolerance)


        # Geometric / Spatial Manipulation
        CImg& resize(const int size_x, const int size_y, const int size_z,
                     const int size_c, const int interpolation_type,
                     const unsigned int boundary_conditions,
                     const float centering_x,
                     const float centering_y,
                     const float centering_z,
                     const float centering_c)

        CImg& resize_halfXY()
        CImg& resize_doubleXY()
        CImg& resize_tripleXY()
        CImg& mirror(const char* const axes)
        CImg& shift(const int delta_x, const int delta_y, const int delta_z,
                    const int delta_c, const unsigned int boundary_conditions)
        CImg& permute_axes(const char* const order)
        CImg& unroll(const char axes)
        CImg& rotate(const float angle, const unsigned int interpolation,
                     const unsigned int boundary_conditions)
        # TODO: warp
        CImg& crop(const int x0, const int y0, const int z0, const int c0, 
                   const int x1, const int y1, const int z1, const int c1, 
                   const unsigned int boundary_conditions)
                     
        CImg& autocrop(const T& value, const char* const axes)
        # ...

        # Filtering / Transforms
        CImg& correlate(const CImg& kernel, const bool boundary_conditions,
                        const bool is_normalized)

        CImg& convolve(const CImg& kernel, const bool boundary_conditions,
                       const bool is_normalized)

        CImg& erode(const CImg& kernel, const bool boundary_conditions,
                    const bool is_normalized)

        CImg& dilate(const CImg& kernel, const bool boundary_conditions,
                     const bool is_normalized)
        # ...


        # Drawing functions
        CImg& draw_rectangle(const int x0, const int y0,
                             const int x1, const int y1,
                             const T* const color)
        # ...
        


    # Utility function for loading CImg[T] from a cimg
    # file with half precision floats
    CImg[T] load_float16[T](const char* filename)
    # Utility function for saveing CImg[T] to a cimg file
    # with half precision floats
    void save_float16[T](const CImg[T]& im, const char* filename)


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
