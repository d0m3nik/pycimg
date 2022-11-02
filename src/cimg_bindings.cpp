#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/operators.h>

#define cimg_use_zlib 1
#define cimg_use_jpeg 1
#define cimg_use_png  1
#define cimg_use_tiff 1
#ifndef __APPLE__
#define cimg_use_openmp 1
#define cimg_verbosity 1
#endif
#include <CImg.h>

using namespace cimg_library;

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;


// Helper function to create CImg<T> from a python array.
template <typename T>
CImg<T> fromarray(py::array_t<T, py::array::c_style | py::array::forcecast> a)
{
    auto dims = a.ndim();
    if (dims < 1)
        throw std::runtime_error("Array should have at least 1 dimension.");
    if (dims > 4)
        throw std::runtime_error("Array should have less than 4 dimensions.");

    auto shape = a.shape();
    if (dims == 1)
    {
        return CImg<T>(a.data(), shape[0]);
    }
    else if (dims == 2)
    {
        return CImg<T>(a.data(), shape[1], shape[0]);
    }
    else if (dims == 3)
    {
        return CImg<T>(a.data(), shape[2], shape[1], shape[0]);
    }
    return CImg<T>(a.data(), shape[3], shape[2], shape[1], shape[0]);
}

// Declare CImg class of pixel type T
template <typename T>
void declare(py::module &m, const std::string &typestr)
{
    using pyarray = py::array_t<T, py::array::c_style | py::array::forcecast>;
    using pyarray_float = py::array_t<float, py::array::c_style | py::array::forcecast>;

    using Class = CImg<T>;
    using Tfloat = typename CImg<T>::Tfloat;
    using ulongT = typename CImg<T>::ulongT;
    std::string pyclass_name = std::string("CImg_") + typestr;
    py::class_<Class> cl(m, pyclass_name.c_str(), py::buffer_protocol());


    // Constructor
    cl.def(py::init<>());

    cl.def("fromarray",
           [](Class& im, pyarray a) { im = fromarray<T>(a); },
           "Create CImg from array.");

    // Operators
    cl.def(py::self == py::self);
    cl.def(py::self != py::self);

    // Load 
    cl.def("load", 
           &Class::load, 
           R"doc(
            Load image from a file.

            Args:
                filename (str): Filename of image.
            Raises:
                RuntimeError: If file does not exist.
           )doc"        
    );

    cl.def("load_bmp", 
           (Class &(Class::*)(const char* const))&Class::load_bmp,
           R"doc(
            Load image from a BMP file.

            Args:
                filename (str): Filename of image.
            Raises:
                RuntimeError: If file does not exist.
           )doc"
    );

    cl.def("load_jpeg", 
           (Class &(Class::*)(const char* const))&Class::load_jpeg,
           R"doc(
            Load image from a JPEG file.

            Args:
                filename (str): Filename of image.
            Raises:
                RuntimeError: If file does not exist.
           )doc"
    );

    cl.def("load_png", 
           (Class& (Class::*)(const char* const, unsigned int *const))&Class::load_png,
           R"doc(
              Load image from a PNG file.

              Args:
                  filename (str): Filename of image.
              Returns:
                  Bits per pixel
              Raises:
                  RuntimeError: If file does not exist.
           )doc",
           py::arg("filename"),
           py::arg("bits_per_pixel") = 0
    );

    cl.def("load_tiff", 
           [](Class& im,  const char* const filename, const unsigned int first_frame, const unsigned int last_frame, const unsigned int step_frame)
           {
               return im.load_tiff(filename, first_frame, last_frame, step_frame);
           },
           R"doc(
            Load image from a TIFF file.

            Args:
                filename (str): Filename of image.
                first_frame: First frame to read (for multi-pages tiff).
                last_frame: Last frame to read (for multi-pages tiff).
                step_frame: Step value of frame reading.
            Returns:
                Voxel size, as stored in the filename.
            Raises:
                RuntimeError: If file does not exist.
           )doc",
           py::arg("filename"),
           py::arg("first_frame") = 0,
           py::arg("last_frame") = ~0U,
           py::arg("step_frame") = 1
    );

    // Save
    cl.def("save", 
           &Class::save,
           R"doc(
              Save image as a file.

              The used file format is defined by the file extension
              in the filename.

              Args:
                  filename (str): Filneame of image.
                  number: When positive, represents an index added to the filename.
                          Otherwise, no number is added.
                  digits: Number of digits used for adding the number to the filename.
           )doc",
           py::arg("filename"),
           py::arg("number") = -1,
           py::arg("digits") = 6
    );

    cl.def("save_bmp", 
           (const Class& (Class::*)(const char* const) const)&Class::save_bmp,
           R"doc(
             Save image as a BMP file.

             Args:
                filename (str): Filename of image.
           )doc"
    );

    cl.def("save_jpeg", 
           (const Class& (Class::*)(const char* const, const unsigned int) const)&Class::save_jpeg,
           R"doc(
              Save image as a JPEG file.

              Args:
                  filename (str): Filename of image.
                  quality: Image quality (in %).
           )doc",
           py::arg("filename"),
           py::arg("quality") = 100
    );

    cl.def("save_png", 
           (const Class& (Class::*)(const char* const, const unsigned int) const)&Class::save_png,
           R"doc(
              Save image as a PNG file.

              Args:
                  filename (str): Filename of image.
                  bytes_per_pixel: Force the number of bytes per pixels for
                                   saving, when possible.
           )doc",
           py::arg("filename"),
           py::arg("bytes_per_pixel") = 0
    );

    cl.def("save_tiff", 
           [](const Class& im, const char* const filename, const unsigned int compression_type, pyarray_float voxel_size, const char* const description, bool use_bigtiff)
           {
               return im.save_tiff(filename, compression_type, voxel_size.size() == 0 ? 0 : voxel_size.data(), description, use_bigtiff);
           },
           R"doc(
              Save image as a TIFF file.

              Args:
                  filename (str): Filename of image.
                  compression_type:    Type of data compression.
                      Can be: C_NONE, C_LZW, C_JPEG.
                  voxel_size: Voxel size, to be stored in the filename.
                  description: Description, to be stored in the filename.
                  use_bigtiff: Allow to save big tiff files (>4Gb).
           )doc",
           py::arg("filename"),
           py::arg("compression_type") = 0,
           py::arg("voxel_size") = pyarray_float(),
           py::arg("description") = "",
           py::arg("use_bigtiff") = true
     );

    // Instance characteristics
    cl.def("spectrum", 
           &Class::spectrum,
           "Return spectrum (number of channels) of image."
    );

    cl.def("depth", 
           &Class::depth,
           "Return depth of image"
    );

    cl.def("height", 
           &Class::height,
           "Return height of image"
    );

    cl.def("width", 
           &Class::width,
           "Return width of image"
    );

    cl.def("size", 
           &Class::size,
           "Return the total number of pixel values in the image."
    );

    // Buffer protocol
    cl.def_buffer([](Class &c) -> py::buffer_info {
            return py::buffer_info(
                c.data(),                               /* Pointer to buffer */
                sizeof(T),                              /* Size of one scalar */
                py::format_descriptor<T>::format(),     /* Python struct-style format descriptor */
                4,                                      /* Number of dimensions */
                { c.spectrum(), c.depth(), c.height(), c.width() }, /* Buffer dimensions */
                { sizeof(T) * c.depth() * c.height() * c.width(),
                  sizeof(T) * c.height() * c.width(),
                  sizeof(T) * c.width(),                /* Strides (in bytes) for each index */
                  sizeof(T) }
            );
        });

    cl.def("display",
           (const Class& (Class::*)(const char *const, const bool, unsigned int *const, const bool) const)(&Class::display),
           R"doc(
              Display image into a CImgDisplay window.

              Args:
                  title (str): Title of window.
           )doc",
           py::arg("title") = "",
           py::arg("display_info") = true,
           py::arg("XYZ") = 0,
           py::arg("exit_on_anykey") = false
     );
    
    cl.def("resize",
           (Class& (Class::*)(const int, const int, const int, const int, const int, const unsigned int, const float, const float, const float, const float))(&Class::resize),
           R"doc(
            Resize image to new dimensions.

            Args:
                size_x (int): Number of columns (new size along the X-axis).
                size_y (int): Number of rows (new size along the Y-axis).
                size_z (int): Number of slices (new size along the Z-axis).
                size_c (int): Number of vector-channels (new size along the C-axis).
                interpolation_type (int):  Method of interpolation:
                    NONE_RAW = no interpolation: raw memory resizing.
                    NONE = no interpolation: additional space is filled according to boundary_conditions.
                    NEAREST = nearest-neighbor interpolation.
                    MOVING_AVERAGE = moving average interpolation.
                    LINEAR = linear interpolation.
                    GRID = grid interpolation.
                    CUBIC = cubic interpolation.
                    LANCZOS = lanczos interpolation.
                boundary_conditions (int): Type of boundary conditions used if
                                     necessary. Can be: DIRICHLET | NEUMANN | PERIODIC | MIRROR
                centering_x (int): Set centering type (only if interpolation_type=NONE).
                centering_y (int): Set centering type (only if interpolation_type=NONE).
                centering_z (int): Set centering type (only if interpolation_type=NONE).
                centering_c (int): Set centering type (only if interpolation_type=NONE).
                  )doc",
           py::arg("size_x"),
           py::arg("size_y") = -100,
           py::arg("size_z") = -100,
           py::arg("size_c") = -100,
           py::arg("interpolation_type") = 1,
           py::arg("boundary_conditions") = 0,
           py::arg("centering_x") = 0.0f,
           py::arg("centering_y") = 0.0f,
           py::arg("centering_z") = 0.0f,
           py::arg("centering_c") = 0.0f
    );

    cl.def("resize_halfXY",
           &Class::resize_halfXY,
           R"doc(
              Resize image to half-size along XY axes, using an optimized filter.
           )doc"
    );

    cl.def("resize_doubleXY",
           &Class::resize_doubleXY,
           R"doc(
              Resize image to double-size, using the Scale2X algorithm.
           )doc"
     );

    cl.def("resize_tripleXY",
           &Class::resize_tripleXY,
           R"doc(
              Resize image to triple-size, using the Scale3X algorithm.
           )doc"
     );

    cl.def("mirror", 
           (Class& (Class::*)(const char* const))&Class::mirror,
           R"doc(
              Mirror image content along specified axes.

              Args:
                  axes (str): Mirror axes as string, e.g. "x" or "xyz"
           )doc",
           py::arg("axes")
    );

    cl.def("shift",
           (Class& (Class::*)(const int, const int, const int, const int, const unsigned int))&Class::shift,
           R"doc(
              Shift image content.

              Args:
                  delta_x (int): Amount of displacement along the X-axis.
                  delta_y (int): Amount of displacement along the Y-axis.
                  delta_z (int): Amount of displacement along the Z-axis.
                  delta_c (int): Amount of displacement along the C-axis.
                  boundary_conditions (int): Border condition.
           )doc",
           py::arg("delta_x"),
           py::arg("delta_y") = 0,
           py::arg("delta_z") = 0,
           py::arg("delta_c") = 0,
           py::arg("boundary_conditions") = 0
    );

    cl.def("permute_axes", 
           &Class::permute_axes,
           R"doc(
              Permute axes order.

              Args:
                  order (str): Axes permutations as string of length 4.

              Raises: RuntimeError if order is invalid.
           )doc"
    );

    cl.def("unroll", 
           &Class::unroll,
           R"doc(
              Unroll pixel values along specified axis.

              Args:
                  axis (str): 'x', 'y', 'z', or 'c'.

              Raises: RuntimeError if axis is invalid.
           )doc"
    );

    cl.def("rotate",
           (Class& (Class::*)(const float, const unsigned int, const unsigned int))&Class::rotate,
           R"doc(
              Rotate image with arbitrary angle.

              Args:
                  angle (float): Rotation angle, in degrees.
                  interpolation (int): Type of interpolation.
                                 Can be { 0=nearest | 1=linear | 2=cubic | 3=mirror }.
                  boundary_conditions (int): Boundary conditions.
           )doc",
           py::arg("angle"),
           py::arg("interpolation") = 1,
           py::arg("boundary_conditions") = 0
    );

    cl.def("crop",
           (Class& (Class::*)(const int, const int, const int, const int, const int, const int, const int, const int, const unsigned int))&Class::crop,
           R"doc(
              Crop image region.

              Args:
                 x0 (int): X-coordinate of the upper-left crop rectangle corner.
                 y0 (int): Y-coordinate of the upper-left crop rectangle corner.
                 z0 (int): Z-coordinate of the upper-left crop rectangle corner.
                 c0 (int): C-coordinate of the upper-left crop rectangle corner.
                 x1 (int): X-coordinate of the lower-right crop rectangle corner.
                 y1 (int): Y-coordinate of the lower-right crop rectangle corner.
                 z1 (int): Z-coordinate of the lower-right crop rectangle corner.
                 c1 (int): C-coordinate of the lower-right crop rectangle corner.
                 boundary_conditions (int): boundary conditions.
           )doc",
           py::arg("x0"),
           py::arg("y0"),
           py::arg("z0"),
           py::arg("c0"),
           py::arg("x1"),
           py::arg("y1"),
           py::arg("z1"),
           py::arg("c1"),
           py::arg("boundary_conditions") = 0
    );

    cl.def("autocrop",
           [](Class& im, pyarray color, const char* const axes)
           {
                if(color.size() == 0)
                    return im.autocrop(nullptr, axes);
                if(color.size() != im.spectrum())
                    throw std::runtime_error("Color needs to have " + std::to_string(im.spectrum()) + " elements.");
                return im.autocrop(color.data(), axes);
           }, 
           R"doc(
              Autocrop image region, regarding the specified background color.

              Args:
                  color (int/list): Color used for the crop. If 0, color is guessed.
                  axes (str): Axes used for crop.
           )doc",
           py::arg("color") = pyarray(),
           py::arg("axes") = "czyx"
    );

    cl.def("append",
           (Class& (Class::*)(const Class&, const char, const float))&Class::append,
           R"doc(
              Append two images along specified axis.

              Args:
                  img (CImg): Image to append with instance image.
                  axis (str): Appending axis. Can be { 'x' | 'y' | 'z' | 'c' }.
                  align (float): Append alignment in [0,1].
           )doc",
           py::arg("img"),
           py::arg("axis") = 'x',
           py::arg("align") = 0
    );
       
    cl.def("linear_atX",
           (Tfloat (Class::*)(const float, const  int, const int, const int) const)(&Class::linear_atX),
           R"doc(
              Return pixel value, using linear interpolation
              and Neumann boundary conditions for the X-coordinate.

              Args:
                  fx (float): X-coordinate of the pixel value.
                  y (int):    Y-coordinate of the pixel value
                  z (int):    Z-coordinate of the pixel value.
                  c (int):    C-coordinate of the pixel value.

              Returns: a linearly-interpolated pixel value of the image
                       instance located at (fx,y,z,c).
           )doc",
           py::arg("fx"),
           py::arg("y") = 0,
           py::arg("z") = 0,
           py::arg("c") = 0
    );


    cl.def("linear_atXY",
           (Tfloat (Class::*)(const float, const float, const int, const int) const)(&Class::linear_atXY),
           R"doc(
              Return pixel value, using linear interpolation
              and Neumann boundary conditions for the X and Y-coordinates.

              Args:
                  fx (float): X-coordinate of the pixel value.
                  fy (float): Y-coordinate of the pixel value.
                  z (int):    Z-coordinate of the pixel value.
                  c (int):    C-coordinate of the pixel value.

              Returns: a linearly-interpolated pixel value of the image
                       instance located at (fx,fy,z,c).
           )doc",
           py::arg("fx"),
           py::arg("fy"),
           py::arg("z") = 0,
           py::arg("c") = 0
    );

    cl.def("linear_atXYZ",
           (Tfloat (Class::*)(const float, const float, const float, const int) const)(&Class::linear_atXYZ),
           R"doc(
              Return pixel value, using linear interpolation
              and Neumann boundary conditions for the X, Y, and Z-coordinates.

              Args:
                  fx (float): X-coordinate of the pixel value.
                  fy (float): Y-coordinate of the pixel value.
                  fz (float): Z-coordinate of the pixel value.
                  c (int):    C-coordinate of the pixel value.

              Returns: a linearly-interpolated pixel value of the image
                       instance located at (fx,fy,fz,c).
           )doc",
           py::arg("fx"),
           py::arg("fy"),
           py::arg("fz"),
           py::arg("c") = 0
    );
   
    cl.def("linear_atXYZC",
           (Tfloat (Class::*)(const float, const float, const float, const float) const)(&Class::linear_atXYZC),
           R"doc(
              Return pixel value, using linear interpolation
              and Neumann boundary conditions for the X, Y, Z, and C-coordinates.

              Args:
                  fx (float): X-coordinate of the pixel value.
                  fy (float): Y-coordinate of the pixel value.
                  fz (float): Z-coordinate of the pixel value.
                  fc (float):    C-coordinate of the pixel value.

              Returns: a linearly-interpolated pixel value of the image
                       instance located at (fx,fy,fz,fc).
           )doc",
           py::arg("fx"),
           py::arg("fy"),
           py::arg("fz"),
           py::arg("fc")
    ); 

    // Value manipulation
    cl.def("fill",
           (Class& (Class::*)(const T&))(&Class::fill),
           R"doc(
              Fill all pixel values with specified value.

              Args:
                  val (float): Fill value.
           )doc",
           py::arg("val")
    );

    cl.def("invert_endianness", 
           &Class::invert_endianness,
           "Invert endianness of all pixel values."
    );

    cl.def("rand", 
           &Class::rand,
           R"doc(
              Fill image with random values in specified range.

              Args:
                  val_min (float): Minimal authorized random value.
                  val_max (float): Maximal authorized random value.
            )doc",
            py::arg("val_min"),
            py::arg("val_max")
    );

    cl.def("round", 
           (Class& (Class::*)(const double, const int))&Class::round,
           R"doc(
              Round pixel values.

              Args:
                  y (int): Rounding precision.
                  rounding_type (int): Rounding type. Can be:
                      R_BACKWARD, R_NEAREST, R_FORWARD
           )doc",
           py::arg("y") = 1,
           py::arg("rounding_type") = 0
    );

    cl.def("noise", 
           (Class& (Class::*)(const double, const unsigned int))&Class::noise,
           R"doc(
              Add random noise to pixel values.

              Args:
                  sigma (float): Amplitude of the random additive noise.
                                 If sigma<0, it stands for a percentage of
                                 the global value range.

                  noise_type (int): Type of additive noise (can be
                                    GAUSSIAN,
                                    UNIFORM,
                                    SALT_AND_PEPPER,
                                    POISSON or
                                    RICIAN).
           )doc",
           py::arg("sigma"),
           py::arg("noise_type") = 0
    );


    cl.def("normalize", 
           (Class& (Class::*)(const T&, const T&, const float))&Class::normalize,
           R"doc(
              Linearly normalize pixel values.

              Args:
                  min_value (float): Minimum desired value of resulting image.
                  max_value (float): Maximum desired value of resulting image.
                  constant_case_ratio (float): in case of instance image having a constant value, 
                                               tell what ratio of [min_value,max_value] is used to fill the normalized image 
                                               (=0 for min_value, =1 for max_value, =0.5 for (min_value + max_value)/2).
           )doc",
           py::arg("min_value"),
           py::arg("max_value"),
           py::arg("constant_case_ratio") = 0
    );

    cl.def("norm", 
           (Class& (Class::*)(const int))&Class::norm,
           R"doc(
              Compute Lp-norm of each multi-valued pixel of the
              image instance.

              Args:
                  norm_type (int): Type of computed vector norm. Can be:
                  LINF_NORM, L0_NORM, L1_NORM, L2_NORM, or value p>2
           )doc",
           py::arg("norm_type") = 1
    );

    cl.def("cut", 
           (Class& (Class::*)(const T&, const T&))&Class::cut,
           R"doc(
              Cut pixel values in specified range.

              Args:
                  min_value (float): Minimum desired value of resulting image.
                  max_value (float): Maximum desired value of resulting image.
           )doc",
           py::arg("min_value"),
           py::arg("max_value")
    );

    cl.def("quantize", 
           (Class& (Class::*)(const unsigned int, const bool))&Class::quantize,
           R"doc(
              Uniformly quantize pixel values.

              Args:
                  nb_levels (int): Number of quantization levels.
                  keep_range (bool): Tells if resulting values keep the same
                                     range as the original ones.
           )doc",
           py::arg("nb_levels"),
           py::arg("keep_range") = true
    );

    cl.def("threshold", 
           (Class& (Class::*)(const T&, const bool, const bool))&Class::threshold,
           R"doc(
              Threshold pixel values.

              Args:
                  value (float): Threshold value.
                  soft_threshold (bool): Tells if soft thresholding must be
                                          applied (instead of hard one).
                  strict_threshold (bool): Tells if threshold value is strict.
           )doc",
           py::arg("value"),
           py::arg("soft_threshold") = false,
           py::arg("strict_threshold") = false
    );

    cl.def("histogram", 
           (Class& (Class::*)(const unsigned int, const T&, const T&))&Class::histogram,
           R"doc(
              Compute the histogram of pixel values.

              Args:
              nb_levels (int): Number of desired histogram levels.
              min_value (float): Minimum pixel value considered for the
                                   histogram computation. All pixel values
                                   lower than min_value will not be counted.
              max_value (float): Maximum pixel value considered for the
                                   histogram computation. All pixel values
                                   higher than max_value will not be counted.
           )doc",
           py::arg("nb_levels"),
           py::arg("min_value"),
           py::arg("max_value")
    );

    cl.def("equalize", 
           (Class& (Class::*)(const unsigned int, const T&, const T&))&Class::equalize,
           R"doc(
              Equalize histogram of pixel values.

              Args:
                  nb_levels (int): Number of desired histogram levels.
                  min_value (float): Minimum pixel value considered for the
                                     histogram computation. All pixel values
                                     lower than min_value will not be counted.
                  max_value (float): Maximum pixel value considered for the
                                     histogram computation. All pixel values
                                     higher than max_value will not be counted.
           )doc",
           py::arg("nb_levels"),
           py::arg("min_value"),
           py::arg("max_value")
    );

    cl.def("label", 
           (Class& (Class::*)(const bool, const Tfloat, const bool))&Class::label,
           R"doc(
              Label connected components.

              Args:
                  is_high_connectivity (bool): Choose between 4(false)
                  - or 8(true)-connectivity in 2d case, and between 6(false)
                  - or 26(true)-connectivity in 3d case.
                  tolerance (float): Tolerance used to determine if two neighboring
                                     pixels belong to the same region.
           )doc", 
           py::arg("is_high_connectivity") = false,
           py::arg("tolerance") = 0,
           py::arg("is_L2_norm") = true
    );

    cl.def("min_max", 
           [](Class& im)
           {
               T max_val;
               T min_val = im.min_max(max_val);
               return std::pair<T,T>{min_val, max_val};
           }, 
           " Returns: tuple with minimum and maximum pixel value. "
    );

    cl.def("max_min", 
           [](Class& im)
           {
               T min_val;
               T max_val = im.max_min(min_val);
               return std::pair<T,T>{max_val, min_val};
           }, 
           " Returns: tuple with maximum and minimum pixel value. "
    );

    // Filtering transforms
    cl.def("correlate",
           (Class& (Class::*)(const Class& kernel, 
                              const unsigned int, 
                              const bool, 
                              const unsigned int, 
                              const int, 
                              const int, 
                              const int, 
                              const int,
                              const int,
                              const int,
                              const int,
                              const int,
                              const int,
                              const float,
                              const float,
                              const float,
                              const float,
                              const float,
                              const float,
                              const bool
                              ))&Class::correlate,
           R"doc( 
              Correlate image by a kernel.

              Args:
                  kernel (CImg): the correlation kernel.
                  boundary_conditions (bool): boundary conditions can be
                                              (False=dirichlet, True=neumann)
                  is_normalized (bool): enable local normalization.
           )doc",
           py::arg("kernel"),
           py::arg("boundary_conditions") = 1,
           py::arg("is_normalized") = false,
           py::arg("channel_mode") = 1,
           py::arg("xcenter") = (int)(~0U>>1),
           py::arg("ycenter") = (int)(~0U>>1),
           py::arg("zcenter") = (int)(~0U>>1),
           py::arg("xstart") = 0,
           py::arg("ystart") = 0,
           py::arg("zstart") = 0,
           py::arg("xend") = (int)(~0U>>1),
           py::arg("yend") = (int)(~0U>>1),
           py::arg("zend") = (int)(~0U>>1),
           py::arg("xstride") = 1,
           py::arg("ystride") = 1,
           py::arg("zstride") = 1,
           py::arg("xdilation") = 1,
           py::arg("ydilation") = 1,
           py::arg("zdilation") = 1,
           py::arg("interpolation_type") = false
    );
    cl.def("convolve",
           (Class& (Class::*)(const Class& kernel, 
                              const unsigned int, 
                              const bool, 
                              const unsigned int, 
                              const int, 
                              const int, 
                              const int, 
                              const int,
                              const int,
                              const int,
                              const int,
                              const int,
                              const int,
                              const float,
                              const float,
                              const float,
                              const float,
                              const float,
                              const float,
                              const bool
                              ))&Class::convolve,
           R"doc( 
              Convolve image by a kernel.

              Args:
                  kernel (CImg): the correlation kernel.
                  boundary_conditions (bool): boundary conditions.
                  is_normalized (bool): enable local normalization.
           )doc",
           py::arg("kernel"),
           py::arg("boundary_conditions") = 1,
           py::arg("is_normalized") = false,
           py::arg("channel_mode") = 1,
           py::arg("xcenter") = (int)(~0U>>1),
           py::arg("ycenter") = (int)(~0U>>1),
           py::arg("zcenter") = (int)(~0U>>1),
           py::arg("xstart") = 0,
           py::arg("ystart") = 0,
           py::arg("zstart") = 0,
           py::arg("xend") = (int)(~0U>>1),
           py::arg("yend") = (int)(~0U>>1),
           py::arg("zend") = (int)(~0U>>1),
           py::arg("xstride") = 1,
           py::arg("ystride") = 1,
           py::arg("zstride") = 1,
           py::arg("xdilation") = 1,
           py::arg("ydilation") = 1,
           py::arg("zdilation") = 1,
           py::arg("interpolation_type") = false
    );

    cl.def("cumulate",
           (Class& (Class::*)(const char* const))&Class::cumulate,
           R"doc(
              Cumulate image values, optionally along specified axes.

              Args:
                  axes (str): Cumulation axes as string, e.g. "x" or "xyz".
           )doc",
           py::arg("axes")
    );

    cl.def("erode",
           (Class& (Class::*)(const Class&, const unsigned int, const bool))&Class::erode,
           R"doc(
              Erode image by a structuring element.

              Args:
                  kernel (CImg):	Structuring element.
                  boundary_conditions (int): Boundary conditions.
                  is_real (bool): Do the erosion in real (a.k.a 'non-flat')
                                  mode (true) rather than binary mode (false).
           )doc",
           py::arg("kernel"),
           py::arg("boundary_conditions") = 1,
           py::arg("is_real") = false
    );

    cl.def("dilate",
           (Class& (Class::*)(const Class&, const unsigned int, const bool))&Class::dilate,
           R"doc(
              Dilate image by a structuring element.

              Args:
                  kernel (CImg):	Structuring element.
                  boundary_conditions (int): Boundary conditions.
                  is_real (bool): Do the erosion in real (a.k.a 'non-flat')
                                  mode (true) rather than binary mode (false).
           )doc",
           py::arg("kernel"),
           py::arg("boundary_conditions") = 1,
           py::arg("is_real") = false
    );

    cl.def("watershed",
           (Class& (Class::*)(const Class&, const bool))&Class::watershed,
           R"doc(
              Compute watershed transform.

              Args:
                  priority (CImg): Priority map.
                  is_high_connectivity (bool): Choose between 4(false)- or
                                        8(true)-connectivity in 2d case,
                                        and between 6(false)- or
                                        26(true)-connectivity in 3d case.
           )doc",
           py::arg("priority"),
           py::arg("is_high_connectivity") = false
    );

    cl.def("deriche",
           (Class& (Class::*)(const float, const unsigned int, const char, const bool))&Class::deriche,
           R"doc(
              Apply recursive Deriche filter.

              Args:
                  sigma (float): Standard deviation of the filter.
                  order (int): Order of the filter. Can be:
                         SMOOTH_FILTER, FIRST_DERIV, or SECOND_DERIV.
                  axis (str): Axis along which the filter is computed. Can be:
                        { 'x' | 'y' | 'z' | 'c' }.
                  boundary_conditions (bool): Boundary conditions. Can be:
                        { False=dirichlet | True=neumann }.
           )doc",
           py::arg("sigma"),
           py::arg("order") = 0,
           py::arg("axis") = 'x',
           py::arg("boundary_conditions") = true
    );

    cl.def("vanvliet",
           (Class& (Class::*)(const float, const unsigned int, const char, const bool))&Class::vanvliet,
           R"doc(
              Van Vliet recursive Gaussian filter.

              Args:
                  sigma (float): Standard deviation of the Gaussian filter.
                  order (int): Order of the filter. Can be:
                         SMOOTH_FILTER, FIRST_DERIV, SECOND_DERIV, or THIRD_DERIV.
                  axis (str): Axis along which the filter is computed. Can be:
                        { 'x' | 'y' | 'z' | 'c' }.
                  boundary_conditions (bool): Boundary conditions. Can be:
                        { False=dirichlet | True=neumann }.
           )doc",
           py::arg("sigma"),
           py::arg("order") = 0,
           py::arg("axis") = 'x',
           py::arg("boundary_conditions") = true
    );

    cl.def("blur",
           (Class& (Class::*)(const float, const unsigned int, const bool))&Class::blur,
           R"doc(
              Blur image isotropically.

              Note: The blur is computed as a 0-order Deriche filter.
              This is not a gaussian blur. This is a recursive algorithm,
              not depending on the values of the standard deviations.

              Args:
                  sigma (float): Standard deviation of the blur.
                  boundary_conditions (int): Boundary conditions.
                  is_gaussian (bool): Tells if the blur uses a gaussian (True)
                               or quasi-gaussian (False) kernel.
           )doc",
           py::arg("sigma"),
           py::arg("boundary_conditions") = 1,
           py::arg("is_gaussian") = false
    );

    cl.def("boxfilter",
           (Class& (Class::*)(const float, const int, const char, const bool, const unsigned int))&Class::boxfilter,
           R"doc(
              Apply box filter to image.

              Args:
                  boxsize (float): Size of the box window (can be subpixel)
                  order (int):   the order of the filter 0,1 or 2.
                  axis (str):    Axis along which the filter is computed.
                           Can be { 'x' | 'y' | 'z' | 'c' }.
                  boundary_conditions (bool): Boundary conditions. Can be
                                       { False=dirichlet | True=neumann }.
                  nb_iter (int): Number of filter iterations.
           )doc",
           py::arg("boxsize"),
           py::arg("order"),
           py::arg("axis") = 'x',
           py::arg("boundary_conditions") = true,
           py::arg("nb_iter") = 1 
    );

    cl.def("blur_box",
           (Class& (Class::*)(const float, const unsigned int))&Class::blur_box,
           R"doc(
              Blur image with a box filter.

              Args:
                  boxsize (int): Size of the box window (can be subpixel).
                  boundary_conditions (int): Boundary conditions.
           )doc",
           py::arg("boxsize"),
           py::arg("boundary_conditions") = 1
    );

    cl.def("blur_median",
           (Class& (Class::*)(const unsigned int, const float))&Class::blur_median,
           R"doc(
              Blur image with the median filter.

              Args:
                  n (int): Size of the median filter.
                  threshold (float): Threshold used to discard pixels too far
                             from the current pixel value in the median computation.
           )doc",
           py::arg("n"),
           py::arg("threshold") = 0
    );

    cl.def("sharpen",
           (Class& (Class::*)(const float, const bool, const float, const float, const float))&Class::sharpen,
           R"doc(
              Sharpen image.

              Args:
                  amplitude (float): Sharpening amplitude
                  sharpen_type (bool): Select sharpening method. Can be
                                { False=inverse diffusion | True=shock filters }.
                  edge (int): Edge threshold (shock filters only).
                  alpha (float): Gradient smoothness (shock filters only).
                  sigma (float): Tensor smoothness (shock filters only).
           )doc",
           py::arg("amplitude"),
           py::arg("sharpen_type") = false,
           py::arg("edge") = 1,
           py::arg("alpha") = 0,
           py::arg("sigma") = 0
    ); 

    // Drawing
    cl.def("draw_rectangle",
           [](Class& im, const int x0, const int y0, const int x1, const int y1, pyarray color, const float opacity)
           {
                if(color.size() != im.spectrum())
                    throw std::runtime_error("Color needs to have " + std::to_string(im.spectrum()) + " elements.");
                return im.draw_rectangle(x0, y0, x1, y1, color.data(), opacity);
           }, 
           R"doc(
              Draw a filled 2d rectangle.

              Args:
                  x0 (int): X-coordinate of the upper-left rectangle corner.
                  y0 (int): Y-coordinate of the upper-left rectangle corner.
                  x1 (int): X-coordinate of the lower-right rectangle corner.
                  y1 (int): Y-coordinate of the lower-right rectangle corner.
                  color (list): List of color value with spectrum() entries.
                  opacity (float): Drawing opacity.

              Raises:
                  RuntimeError: If list of color values does not have spectrum() entries.
           )doc",
           py::arg("x0"),
           py::arg("y0"),
           py::arg("x1"),
           py::arg("y1"),
           py::arg("color"),
           py::arg("opacity") = 1
    );

    cl.def("draw_polygon",
           [](Class& im, pyarray points, pyarray color, const float opacity)
           {
                if(color.size() != im.spectrum())
                    throw std::runtime_error("Color needs to have " + std::to_string(im.spectrum()) + " elements.");
                return im.draw_polygon(fromarray<T>(points), color.data(), opacity);
           }, 
           R"doc(
              Draw filled 2d polygon.

              Args:
                  points (ndarray): (n x 2) numpy array of polygon vertices
                  color (list): List of color value with spectrum() entries.
                  opacity (float): Drawing opacity.

              Raises:
                  RuntimeError: If list of color values does not have spectrum() entries.
           )doc",
           py::arg("points"),
           py::arg("color"),
           py::arg("opacity") = 1
    );

    cl.def("draw_circle",
        [](Class& im, const int x0, const int y0, const int radius, pyarray color, const float opacity)
        {
            if(color.size() != im.spectrum())
                throw std::runtime_error("Color needs to have " + std::to_string(im.spectrum()) + " elements.");
            return im.draw_circle(x0, y0, radius, color.data(), opacity);
        },
        R"doc(
              Draw a filled 2d circle.

              Args:
                  x0 (int):  X-coordinate of the circle center.
                  y0 (int):  Y-coordinate of the circle center.
                  radius (float):  Circle radius.
                  color (list): List of color value with spectrum() entries.
                  opacity (float): Drawing opacity.

              Raises:
                  RuntimeError: If list of color values does not have spectrum() entries.
        )doc",
        py::arg("x0"),
        py::arg("y0"),
        py::arg("radius"),
        py::arg("color"),
        py::arg("opacity") = 1
    );

    cl.def("draw_triangle",
           [](Class& im, const int x0, const int y0, const int x1, const int y1, const int x2, const int y2, pyarray color, const float opacity)
           {
               if(color.size() != im.spectrum())
                   throw std::runtime_error("Color needs to have " + std::to_string(im.spectrum()) + " elements.");
               return im.draw_triangle(x0, y0, x1, y1, x2, y2, color.data(), opacity);
           },
           R"doc(
              Draw a filled 2d triangle.

              Args:
                  x0 (int): X-coordinate of the first vertex.
                  y0 (int): Y-coordinate of the first vertex.
                  x1 (int): X-coordinate of the second vertex.
                  y1 (int): Y-coordinate of the second vertex.
                  x2 (int): X-coordinate of the third vertex.
                  y2 (int): Y-coordinate of the third vertex.
                  color (list): List of color value with spectrum() entries.
                  opacity (float): Drawing opacity.

              Raises:
                  RuntimeError: If list of color values does not have spectrum() entries.
           )doc",
           py::arg("x0"),
           py::arg("y0"),
           py::arg("x1"),
           py::arg("y1"),
           py::arg("x2"),
           py::arg("y2"),
           py::arg("color"),
           py::arg("opacity") = 1
    );

    cl.def("draw_text",
           [](Class& im, const int x0, const int y0, const char* const text, pyarray foreground_color, pyarray background_color, const float opacity, const unsigned int font_height)
           {
               if(foreground_color.size() != im.spectrum() || background_color.size() != im.spectrum())
                   throw std::runtime_error("Colors needs to have " + std::to_string(im.spectrum()) + " elements.");
               return im.draw_text(x0, y0, text, foreground_color.data(), background_color.data(), opacity, font_height);
           },
           R"doc(
              Draw a text string.

              Args:
                  x0 (int): X-coordinate of the text in the image instance.
                  y0 (int): Y-coordinate of the text in the image instance.
                  text (str): The text.
                  foreground_color (list): List of color value with spectrum() entries.
                  background_color (list): List of color value with spectrum() entries.
                  opacity (float): Drawing opacity.
                  font_height (int): Height of the text font
                      (exact match for 13,23,53,103, interpolated otherwise).
           )doc",
           py::arg("x0"),
           py::arg("y0"),
           py::arg("text"),
           py::arg("foreground_color"),
           py::arg("background_color"),
           py::arg("opacity") = 1,
           py::arg("font_height") = 13
    );

    // Mathematical 
    cl.def("sqr", (Class& (Class::*)())&Class::sqr, "Compute the square value of each pixel value.");
    cl.def("sqrt", (Class& (Class::*)())&Class::sqrt, "Compute the square root of each pixel value.");
    cl.def("exp", (Class& (Class::*)())&Class::exp, "Compute the exponential of each pixel value.");
    cl.def("log", (Class& (Class::*)())&Class::log, "Compute the logarithm of each pixel value.");
    cl.def("log2", (Class& (Class::*)())&Class::log2, "Compute the base-2 logarithm of each pixel value.");
    cl.def("log10", (Class& (Class::*)())&Class::log10, "Compute the base-10 logarithm of each pixel value.");
    cl.def("abs", (Class& (Class::*)())&Class::abs, "Compute the absolute value of each pixel value.");
    cl.def("sign", (Class& (Class::*)())&Class::sign, "Compute the sign of each pixel value.");
    cl.def("cos", (Class& (Class::*)())&Class::cos, "Compute the cosine of each pixel value.");
    cl.def("sin", (Class& (Class::*)())&Class::sin, "Compute the sine of each pixel value.");
    cl.def("sinc", (Class& (Class::*)())&Class::sinc, "Compute the sinc of each pixel value.");
    cl.def("tan", (Class& (Class::*)())&Class::tan, "Compute the tangent of each pixel value.");
    cl.def("sinh", (Class& (Class::*)())&Class::sinh, "Compute the hyperbolic sine of each pixel value.");
    cl.def("tanh", (Class& (Class::*)())&Class::tanh, "Compute the hyperbolic tangent of each pixel value.");
    cl.def("acos", (Class& (Class::*)())&Class::acos, "Compute the arccosine of each pixel value.");
    cl.def("asin", (Class& (Class::*)())&Class::asin, "Compute the arcsine of each pixel value.");
    cl.def("atan", (Class& (Class::*)())&Class::atan, "Compute the arctangent of each pixel value.");

    cl.def("atan2", 
           (Class& (Class::*)(const Class&))&Class::atan2, 
           R"doc(
              Compute the arctangent2 of each pixel value.

              Args:
                  img (CImg): Image whose pixel values specify the second
                              argument of the atan2() function.
           )doc"
    );

    cl.def("mul", 
           (Class& (Class::*)(const Class&))&Class::mul, 
           R"doc(
              In-place pointwise multiplication.

              Compute the pointwise multiplication between
              the image instance and the specified input image img.

              Args:
                  img (CImg): Input image, second operand of the multiplication.
           )doc"
    );

    cl.def("div", 
           (Class& (Class::*)(const Class&))&Class::div, 
           R"doc(
              In-place pointwise division.

              Compute the pointwise division between
              the image instance and the specified input image img.

              Args:
                  img (CImg): Input image, second operand of the division.
           )doc"
    );

    cl.def("pow", 
           (Class& (Class::*)(const double))&Class::pow, 
           R"doc(
              Raise each pixel value to the specified power.

              Args:
                  p (int): Exponent value.
           )doc"
    );

    cl.def("kth_smallest", 
           (T (Class::*)(const ulongT) const)&Class::kth_smallest, 
           R"doc(
              Returns the kth smallest pixel value.

              Args:
                  k (int): Rank of the search smallest element.

              Returns: kth smallest pixel value.
           )doc"
    );

    cl.def("variance", 
           (double (Class::*)(const unsigned int) const)&Class::variance, 
           R"doc(
              Returns the variance of the pixel values.

              Args:
                  variance_method (int): Method used to estimate the variance.
                                         Can be: SECOND_MOMENT
                                                 BEST_UNBIASED
                                                 LEAST_MEDIAN_SQ
                                                 LEAST_TRIMMED_SQ

              Returns: Variance of pixel values.
           )doc",
           py::arg("variance_method") = 1
    );

    cl.def("variance_mean", 
           [](Class& im, const unsigned int variance_method)
           {
                  std::pair<double,double> var_mean;
                  var_mean.first = im.variance_mean(variance_method, var_mean.second);
                  return var_mean;
           },
           R"doc(
              Returns variance and average of pixel values.

              Args:
                  variance_method (int): Method used to estimate the variance.

              Returns: Tuple with variance and mean of pixel values.
           )doc",
           py::arg("variance_method") = 1
    );

    cl.def("mse",
           (double (Class::*)(const Class&) const)&Class::MSE,
           R"doc(
              Compute the MSE (Mean-Squared Error) between two images.

              Args:
                  img (CImg): Image used as the second argument of the MSE operator.

              Returns: mean squared error between self and img.
           )doc"
    );

    cl.def("magnitude", 
           (double (Class::*)(const int) const)&Class::magnitude, 
           R"doc(
              Compute norm of the image, viewed as a matrix.

              Args:
                  magnitude_type (int): Norm type. Can be:
                      LINF_NORM
                      L0_NORM
                      L1_NORM
                      L2_NORM

              Returns: Norm of image.
           )doc"
    );

    cl.def("dot", 
           (double (Class::*)(const Class&) const)&Class::dot, 
           R"doc(
              Compute the dot product between instance and argument, viewed as matrices

              Args:
                  img (CImg): Image used as a second argument of the dot product.

              Returns: Dot product between self and img.
           )doc"
    );

    cl.def("apply_geometric_transform",
           [](Class& im, const float s, const Class& M, const Class& t)
           {
              Class tmp = im;
              Class Q = M.get_invert();
              cimg_pragma_openmp(parallel for cimg_openmp_collapse(3) cimg_openmp_if_size(tmp.size(),4096))
              cimg_forXYZ(tmp,x,y,z) {
                  Class p = CImg<>::vector((z-t(0))/s,(x-t(1))/s,(y-t(2))/s);
                  p = Q * p;
                  tmp(x,y,z) = im.linear_atXYZ(p(1),p(2),p(0));
              }
              im = tmp;
           },
           R"doc(
              Apply a geometric transform

              Args:
                  s (float): scale
                  M (CImg) : 3x3 matrix CImg(3,3)
                  t (CImg) : 1x3 shift vector (CImg(3,1))
           )doc"
    );

}

PYBIND11_MODULE(cimg_bindings, m)
{
    py::options options;
    options.disable_function_signatures();

    m.doc() = R"doc(
       Pybind11 bindings for the CImg library.
    )doc";

    declare<uint8_t>(m, "uint8");
    declare<uint16_t>(m, "uint16");
    declare<uint32_t>(m, "uint32");
    declare<float>(m, "float32");
    declare<double>(m, "float64");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
