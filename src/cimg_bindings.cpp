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
    cl.def("load", &Class::load);
    cl.def("load_bmp", (Class &(Class::*)(const char* const))&Class::load_bmp);
    cl.def("load_jpeg", (Class &(Class::*)(const char* const))&Class::load_jpeg);
    cl.def("load_png", 
           (Class& (Class::*)(const char* const, unsigned int *const))&Class::load_png,
           "Load png image.",
           py::arg("filename"),
           py::arg("bits_per_pixel") = 0
           );
    cl.def("load_tiff", 
           [](Class& im,  const char* const filename, const unsigned int first_frame, const unsigned int last_frame, const unsigned int step_frame)
           {
               return im.load_tiff(filename, first_frame, last_frame, step_frame);
           },
           "Load tiff image.",
           py::arg("filename"),
           py::arg("first_frame") = 0,
           py::arg("last_frame") = ~0U,
           py::arg("step_frame") = 1
           );

    // Save
    cl.def("save", 
           &Class::save,
           "Save image.",
           py::arg("filename"),
           py::arg("number") = -1,
           py::arg("digits") = 6
           );
    cl.def("save_bmp", (const Class& (Class::*)(const char* const) const)&Class::save_bmp);
    cl.def("save_jpeg", 
           (const Class& (Class::*)(const char* const, const unsigned int) const)&Class::save_jpeg,
           "Save image as jpeg.",
           py::arg("filename"),
           py::arg("quality") = 100
          );
    cl.def("save_png", 
           (const Class& (Class::*)(const char* const, const unsigned int) const)&Class::save_png,
           "Save image as png.",
           py::arg("filename"),
           py::arg("bytes_per_pixel") = 0
          );
    cl.def("save_tiff", 
           [](const Class& im, const char* const filename, const unsigned int compression_type, pyarray_float voxel_size, const char* const description, bool use_bigtiff)
           {
               return im.save_tiff(filename, compression_type, voxel_size.size() == 0 ? 0 : voxel_size.data(), description, use_bigtiff);
           },
           "Save image as a TIFF file.",
           py::arg("filename"),
           py::arg("compression_type") = 0,
           py::arg("voxel_size") = pyarray_float(),
           py::arg("description") = "",
           py::arg("use_bigtiff") = true
           );

    // Instance characteristics
    cl.def("spectrum", &Class::spectrum);
    cl.def("depth", &Class::depth);
    cl.def("height", &Class::height);
    cl.def("width", &Class::width);
    cl.def("size", &Class::size);

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
           "Display image",
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
    cl.def("resize_halfXY", &Class::resize_halfXY);
    cl.def("resize_doubleXY", &Class::resize_doubleXY);
    cl.def("resize_tripleXY", &Class::resize_tripleXY);
    cl.def("mirror", 
           (Class& (Class::*)(const char* const))&Class::mirror,
           "Mirror image content along specified axes.",
           py::arg("axes")
          );
    cl.def("shift",
           (Class& (Class::*)(const int, const int, const int, const int, const unsigned int))&Class::shift,
           "Shift image content.",
           py::arg("delta_x"),
           py::arg("delta_y") = 0,
           py::arg("delta_z") = 0,
           py::arg("delta_c") = 0,
           py::arg("boundary_conditions") = 0
    );
    cl.def("permute_axes", &Class::permute_axes);
    cl.def("unroll", &Class::unroll);
    cl.def("rotate",
           (Class& (Class::*)(const float, const unsigned int, const unsigned int))&Class::rotate,
           "Rotate image with arbitrary angle.",
           py::arg("angle"),
           py::arg("interpolation") = 1,
           py::arg("boundary_conditions") = 0
    );
    cl.def("crop",
           (Class& (Class::*)(const int, const int, const int, const int, const int, const int, const int, const int, const unsigned int))&Class::crop,
           "Crop image region.",
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
           "Autocrop image region, regarding the specified background color.",
           py::arg("color") = pyarray(),
           py::arg("axes") = "czyx"
    );
    cl.def("append",
           (Class& (Class::*)(const Class&, const char, const float))&Class::append,
           "Append two images along specified axis.",
           py::arg("img"),
           py::arg("axis") = 'x',
           py::arg("align") = 0
    );

    cl.def("linear_atXY",
           (Tfloat (Class::*)(const float, const float, const int, const int) const)(&Class::linear_atXY),
           "Return pixel value, using linear interpolation and Dirichlet boundary conditions for the X and Y-coordinates.",
           py::arg("fx"),
           py::arg("fy"),
           py::arg("z") = 0,
           py::arg("c") = 0
    );
    
    // Value manipulation
    cl.def("fill",
           (Class& (Class::*)(const T&))(&Class::fill),
           "Fill all pixel values with specified value.",
           py::arg("val")
    );
    cl.def("invert_endianness", &Class::invert_endianness);
    cl.def("rand", &Class::rand);
    cl.def("round", 
           (Class& (Class::*)(const double, const int))&Class::round,
           "Round pixel values.",
           py::arg("y") = 1,
           py::arg("rounding_type") = 0
    );
    cl.def("noise", 
           (Class& (Class::*)(const double, const unsigned int))&Class::noise,
           "Add random noise to pixel values.",
           py::arg("sigma"),
           py::arg("noise_type") = 0
    );
    cl.def("normalize", 
           (Class& (Class::*)(const T&, const T&, const float))&Class::normalize,
           "Linearly normalize pixel values.",
           py::arg("min_value"),
           py::arg("max_value"),
           py::arg("constant_case_ratio") = 0
    );
    cl.def("norm", 
           (Class& (Class::*)(const int))&Class::norm,
           "Compute Lp-norm of each multi-valued pixel of the image instance.",
           py::arg("norm_type") = 1
    );
    cl.def("cut", 
           (Class& (Class::*)(const T&, const T&))&Class::cut,
           "Cut pixel values in specified range.",
           py::arg("min_value"),
           py::arg("max_value")
    );
    cl.def("quantize", 
           (Class& (Class::*)(const unsigned int, const bool))&Class::quantize,
           "Uniformly quantize pixel values.",
           py::arg("nb_levels"),
           py::arg("keep_range") = true
    );
    cl.def("threshold", 
           (Class& (Class::*)(const T&, const bool, const bool))&Class::threshold,
           "Threshold pixel values.",
           py::arg("value"),
           py::arg("soft_threshold") = false,
           py::arg("strict_threshold") = false
    );
    cl.def("histogram", 
           (Class& (Class::*)(const unsigned int, const T&, const T&))&Class::histogram,
           "Compute the histogram of pixel values.",
           py::arg("nb_levels"),
           py::arg("min_value"),
           py::arg("max_value")
    );
    cl.def("equalize", 
           (Class& (Class::*)(const unsigned int, const T&, const T&))&Class::equalize,
           "Equalize histogram of pixel values.",
           py::arg("nb_levels"),
           py::arg("min_value"),
           py::arg("max_value")
    );
    cl.def("label", 
           (Class& (Class::*)(const bool, const Tfloat, const bool))&Class::label,
           "Label connected components.",
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
           "Return minimum and maximum value."
    );
    cl.def("max_min", 
           [](Class& im)
           {
               T min_val;
               T max_val = im.max_min(min_val);
               return std::pair<T,T>{max_val, min_val};
           }, 
           "Return maximum and minimum value."
    );

    // Filtering transforms
    cl.def("correlate",
           (Class& (Class::*)(const Class& kernel, 
                              const unsigned int, 
                              const bool, 
                              const unsigned int, 
                              const unsigned int, 
                              const unsigned int, 
                              const unsigned int, 
                              const unsigned int,
                              const unsigned int,
                              const unsigned,
                              const unsigned int,
                              const unsigned int,
                              const unsigned int,
                              const float,
                              const float,
                              const float,
                              const float,
                              const float,
                              const float
                              ))&Class::correlate,
           "Correlate image by a kernel.",
           py::arg("kernel"),
           py::arg("boundary_conditions") = 1,
           py::arg("is_normalized") = false,
           py::arg("channel_mode") = 1,
           py::arg("xcenter") = ~0U,
           py::arg("ycenter") = ~0U,
           py::arg("zcenter") = ~0U,
           py::arg("xstart") = 0,
           py::arg("ystart") = 0,
           py::arg("zstart") = 0,
           py::arg("xend") = ~0U,
           py::arg("yend") = ~0U,
           py::arg("zend") = ~0U,
           py::arg("xstride") = 1,
           py::arg("ystride") = 1,
           py::arg("zstride") = 1,
           py::arg("xdilation") = 1,
           py::arg("ydilation") = 1,
           py::arg("zdilation") = 1
    );
    cl.def("convolve",
           (Class& (Class::*)(const Class& kernel, 
                              const unsigned int, 
                              const bool, 
                              const unsigned int, 
                              const unsigned int, 
                              const unsigned int, 
                              const unsigned int, 
                              const unsigned int,
                              const unsigned int,
                              const unsigned,
                              const unsigned int,
                              const unsigned int,
                              const unsigned int,
                              const float,
                              const float,
                              const float,
                              const float,
                              const float,
                              const float
                              ))&Class::convolve,
           "Convolve image by a kernel.",
           py::arg("kernel"),
           py::arg("boundary_conditions") = 1,
           py::arg("is_normalized") = false,
           py::arg("channel_mode") = 1,
           py::arg("xcenter") = ~0U,
           py::arg("ycenter") = ~0U,
           py::arg("zcenter") = ~0U,
           py::arg("xstart") = 0,
           py::arg("ystart") = 0,
           py::arg("zstart") = 0,
           py::arg("xend") = ~0U,
           py::arg("yend") = ~0U,
           py::arg("zend") = ~0U,
           py::arg("xstride") = 1,
           py::arg("ystride") = 1,
           py::arg("zstride") = 1,
           py::arg("xdilation") = 1,
           py::arg("ydilation") = 1,
           py::arg("zdilation") = 1
    );
    cl.def("cumulate",
           (Class& (Class::*)(const char* const))&Class::cumulate,
           "Cumulate image values, along specified axes.",
           py::arg("axes")
    );
    cl.def("erode",
           (Class& (Class::*)(const Class&, const bool, const bool))&Class::erode,
           "Erode image by a structuring element.",
           py::arg("kernel"),
           py::arg("boundary_conditions") = true,
           py::arg("is_real") = false
    );
    cl.def("dilate",
           (Class& (Class::*)(const Class&, const bool, const bool))&Class::dilate,
           "Dilate image by a structuring element.",
           py::arg("kernel"),
           py::arg("boundary_conditions") = true,
           py::arg("is_real") = false
    );
    cl.def("watershed",
           (Class& (Class::*)(const Class&, const bool))&Class::watershed,
           "Compute watershed transform.",
           py::arg("priority"),
           py::arg("is_high_connectivity") = false
    );
    cl.def("deriche",
           (Class& (Class::*)(const float, const unsigned int, const char, const bool))&Class::deriche,
           "Apply recursive Deriche filter.",
           py::arg("sigma"),
           py::arg("order") = 0,
           py::arg("axis") = 'x',
           py::arg("boundary_conditions") = true
    );
    cl.def("vanvliet",
           (Class& (Class::*)(const float, const unsigned int, const char, const bool))&Class::vanvliet,
           "Van Vliet recursive Gaussian filter.",
           py::arg("sigma"),
           py::arg("order") = 0,
           py::arg("axis") = 'x',
           py::arg("boundary_conditions") = true
    );
    cl.def("blur",
           (Class& (Class::*)(const float, const bool, const bool))&Class::blur,
           "Blur image isotropically.",
           py::arg("sigma"),
           py::arg("boundary_conditions") = true,
           py::arg("is_gaussian") = false
    );
    cl.def("boxfilter",
           (Class& (Class::*)(const float, const int, const char, const bool, const unsigned int))&Class::boxfilter,
           "Apply box filter",
           py::arg("boxsize"),
           py::arg("order"),
           py::arg("axis") = 'x',
           py::arg("boundary_conditions") = true,
           py::arg("nb_iter") = 1 
    );
    cl.def("blur_box",
           (Class& (Class::*)(const float, const bool))&Class::blur_box,
           "Blur image with a box filter.",
           py::arg("boxsize"),
           py::arg("boundary_conditions") = true
    );
    cl.def("blur_median",
           (Class& (Class::*)(const unsigned int, const float))&Class::blur_median,
           "Blur image with the median filter.",
           py::arg("n"),
           py::arg("threshold") = 0
    );
    cl.def("sharpen",
           (Class& (Class::*)(const float, const bool, const float, const float, const float))&Class::sharpen,
           "Sharpen image.",
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
           "Draw a filled 2D rectangle.",
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
           "Draw a filled 2D polygon.",
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
        "Draw a filled 2D circle.",
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
           "Draw a filled 2D triangle.",
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
           "Draw a text string.",
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
    cl.def("atan2", (Class& (Class::*)(const Class&))&Class::atan2, "Compute the arctangent2 of each pixel value.");
    cl.def("mul", (Class& (Class::*)(const Class&))&Class::mul, "In-place pointwise multiplication.");
    cl.def("div", (Class& (Class::*)(const Class&))&Class::div, "In-place pointwise division.");
    cl.def("pow", (Class& (Class::*)(const double))&Class::pow, "Raise each pixel value to a specified power.");
    cl.def("kth_smallest", (T (Class::*)(const ulongT) const)&Class::kth_smallest, "Return the kth smallest pixel value.");
    cl.def("variance", 
           (double (Class::*)(const unsigned int) const)&Class::variance, 
           "Return the variance of the pixel values.",
           py::arg("variance_method") = 1
    );
    cl.def("variance_mean", 
           [](Class& im, const unsigned int variance_method)
           {
                  std::pair<double,double> var_mean;
                  var_mean.first = im.variance_mean(variance_method, var_mean.second);
                  return var_mean;
           },
           "Return the variance as well as the average of the pixel values.",
           py::arg("variance_method") = 1
    );
    cl.def("mse", (double (Class::*)(const Class&) const)&Class::MSE, "Compute the MSE (Mean-Squared Error) between two images.");
    cl.def("magnitude", (double (Class::*)(const int) const)&Class::magnitude, "Compute norm of the image, viewed as a matrix.");
    cl.def("dot", (double (Class::*)(const Class&) const)&Class::dot, "Compute the dot product between instance and argument, viewed as matrices.");

}

PYBIND11_MODULE(cimg_bindings, m)
{
    py::options options;
    options.disable_function_signatures();

    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: python_example

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

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
