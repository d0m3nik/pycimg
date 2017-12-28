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

    cdef cppclass CImgDisplay:
        CImgDisplay() except+

    cdef cppclass CImg[T]:
        # Constructors / Instance Management
        CImg() except+

        CImg(const char* const filename) except +

        CImg(const unsigned int x,
             const unsigned int y,
             const unsigned int z,
             const unsigned int c) except +

        CImg& load(const char* const filename) except +
        CImg& load_bmp(const char* const filename) except +
        CImg& load_jpeg(const char* const filename) except +
        CImg& load_png(const char* const filename,
                       unsigned int* const bits_per_pixel) except +
        CImg& load_tiff(const char* const filename,
                        const unsigned int first_frame,
                        const unsigned int last_frame,
                        const unsigned int step_frame,
                        float* const voxel_size,
                        CImg* const description) except +
        CImg& load_cimg(const char* const filename, 
                        const char axis, 
                        const float align) except +

        const CImg& save(const char* const filename,
                         const int number,
                         const unsigned int digits) except +
        CImg& save_bmp(const char* const filename) except +
        CImg& save_jpeg(const char* const filename,
                        const unsigned int quality) except +
        CImg& save_png(const char* const filename,
                       const unsigned int bytes_per_pixel) except +
        CImg& save_tiff(const char* const filename,
                        const unsigned int compression_type,
                        const float* const voxel_size,
                        const char* const description,
                        const bool use_bigtiff) except +
        CImg& save_cimg(const char* const filename, 
                        const bool is_compressed) except +

        # Operators
        CImg& operator+(const T value)
        bool operator==(const CImg& img)
        bool operator!=(const CImg& img)

        const CImg& display(const char* const title) except + 
        const CImg& display_graph(CImgDisplay& disp,
                                  const unsigned int plot_type,
                                  const unsigned int vertex_type,
                                  const char* const labelx,
                                  const double xmin,
                                  const double xmax,
                                  const char* const labely,
                                  const double ymin,
                                  const double ymax) except +

        # Instance characteristics
        int width() const
        int height() const
        int depth() const
        int spectrum() const
        unsigned long size() const
        T* data()
        T linear_atX(const float fx, const int y, const int z, const int c) 
        T linear_atXY(const float fx, const float fy, const int z, const int c)
        T linear_atXYZ(const float fx, const float fy, const float fz, const int c)
        T linear_atXYZC(const float fx, const float fy, const float fy, const float fc)

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
        T& min_max(T& max_val)
        T& max_min(T& min_val)
        T kth_smallest(const unsigned long k)
        double variance(const unsigned int variance_method)
        double variance_mean(const unsigned int variance_method,
                             T& mean)
        double variance_noise(const unsigned int variance_method)
        double MSE(const CImg& img)
        double PSNR(const CImg& img, 
                    const double max_value)
        # eval ...
        # Vector / Matrix Operations 
        double magnitude(const int magnitude_type)
        double dot(const CImg& img)

        # Value Manipulation
        CImg& fill(const T& val)
        CImg& invert_endianness()
        CImg& rand(const T& val_min, const T& val_max)
        CImg& round(const double y, const int rounding_type)
        CImg& noise(const double sigma,
                    const unsigned int noise_type)
        CImg& normalize(const T& min_value,
                        const T& max_value)
        CImg& normalize()
        CImg& norm(const int norm_type)
        CImg& cut(const T& min_value,
                  const T& max_value)
        CImg& quantize(const unsigned int nb_levels,
                       const bool keep_range)
        CImg& threshold(const T& value,
                        const bool soft_threshold, 
                        const bool strict_threshold)
        CImg& histogram(const unsigned int nb_levels,
                        const T& min_value,
                        const T& max_value)
        CImg& equalize(const unsigned int nb_levels,
                       const T& min_value,
                       const T& max_value)
        CImg& index(const CImg& colormap,
                    const float dithering, 
                    const bool map_indexes)
        CImg& map(const CImg& colormap, 
                  const unsigned int boundary_conditions)
        CImg& label(const bool is_high_connectivity,
                    const float tolerance)

        # Geometric / Spatial Manipulation
        CImg& resize(const int size_x, 
                     const int size_y,
                     const int size_z,
                     const int size_c,
                     const int interpolation_type,
                     const unsigned int boundary_conditions,
                     const float centering_x,
                     const float centering_y,
                     const float centering_z,
                     const float centering_c)

        CImg& resize_halfXY()
        CImg& resize_doubleXY()
        CImg& resize_tripleXY()
        CImg& mirror(const char* const axes)
        CImg& shift(const int delta_x,
                    const int delta_y,
                    const int delta_z,
                    const int delta_c,
                    const unsigned int boundary_conditions)
        CImg& permute_axes(const char* const order)
        CImg& unroll(const char axes)
        CImg& rotate(const float angle,
                     const unsigned int interpolation,
                     const unsigned int boundary_conditions)
        # TODO: warp
        CImg& crop(const int x0,
                   const int y0,
                   const int z0,
                   const int c0, 
                   const int x1,
                   const int y1,
                   const int z1,
                   const int c1, 
                   const unsigned int boundary_conditions)
                     
        CImg& autocrop(const T* const color, 
                       const char* const axes)
        # ...
        CImg& append(CImg& img,
                     const char axis,
                     const float align)
        # ...

        # Filtering / Transforms
        CImg& correlate(const CImg& kernel,
                        const bool boundary_conditions,
                        const bool is_normalized) except +

        CImg& convolve(const CImg& kernel,
                       const bool boundary_conditions,
                       const bool is_normalized) except +

        CImg& cumulate(const char* const axes) except +

        CImg& erode(const CImg& kernel,
                    const bool boundary_conditions,
                    const bool is_real) except +

        CImg& dilate(const CImg& kernel,
                     const bool boundary_conditions,
                     const bool is_real) except +

        CImg& watershed(const CImg& priority,
                        const bool is_high_connectivity) except +

        CImg& deriche(const float sigma, 
                      const unsigned int order, 
                      const char axis, 
                      const bool boundary_conditions)

        CImg& vanvliet(const float sigma, 
                       const unsigned int order,
                       const char axis,
                       const bool boundary_conditions)
                 
        CImg& blur(const float sigma,
                   const bool boundary_conditions,
                   const bool is_gaussian)

        CImg& boxfilter(const float boxsize,
                        const int order,
                        const char axis,
                        const bool boundary_conditions,
                        const unsigned int nb_iter)
 
        CImg& blur_box(const float boxsize, 
                       const bool boundary_conditions)

        CImg& blur_median(const unsigned int n,
                          const float threshold)
             
        CImg& sharpen(const float amplitude,
                      const bool sharpen_type,
                      const float edge,
                      const float alpha,
                      const float sigma)

        # Drawing functions
        CImg& draw_triangle(const int x0, 
                            const int y0,
                            const int x1, 
                            const int y1,
                            const int x2, 
                            const int y2,
                            const T* const color, 
                            const float opacity)

        CImg& draw_rectangle(const int x0, 
                             const int y0,
                             const int x1, 
                             const int y1,
                             const T* const color, 
                             const float opacity)
        # ...
        CImg& draw_polygon(const CImg& points, 
                           const T* const color,
                           const float opacity)
        # draw_ellipse
        CImg& draw_circle(const int x0,
                          const int y0,
                          int radius,
                          const T* const color,
                          const float opacity)

        CImg& draw_text(const int x0,
		        const int y0,
	        	const char *const text,
	        	const T* const foreground_color,
	        	const T* const background_color,
	        	const float opacity,
	        	const unsigned int font_height) 	
        


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
