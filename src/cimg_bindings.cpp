#include <pybind11/pybind11.h>

#define cimg_use_zlib 1
#define cimg_use_jpeg 1
#define cimg_use_png  1
#define cimg_use_tiff 1
#ifndef __APPLE__
#define cimg_use_openmp 1
#endif
#include "CImg.h"

using namespace cimg_library;

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

template <typename T>
void declare(py::module &m, const std::string &typestr)
{
    using Class = CImg<T>;
    std::string pyclass_name = std::string("CImg_") + typestr;
    py::class_<Class> cl(m, pyclass_name.c_str(), py::buffer_protocol());

    // Constructor
    cl.def(py::init<>());

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
           (Class& (Class::*)(const char* const, const unsigned int, const unsigned int, const unsigned int, float* const, CImg<char>* const))&Class::load_tiff,
           "Load tiff image.",
           py::arg("filename"),
           py::arg("first_frame") = 0,
           py::arg("last_frame") = ~0U,
           py::arg("step_frame") = 1,
           py::arg("voxel_size") = 0,
           py::arg("description") = 0
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
    cl.def("save_tiff", (const Class& (Class::*)(const char* const) const)&Class::save_tiff);

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
           "Resize image",
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
        
    cl.def("linear_atXY",
           (float (Class::*)(const float, const float, const int, const int) const)(&Class::linear_atXY),
           "Return pixel value, using linear interpolation and Dirichlet boundary conditions for the X and Y-coordinates.",
           py::arg("fx"),
           py::arg("fy"),
           py::arg("z") = 0,
           py::arg("c") = 0
    );
    
    cl.def("rand", &Class::rand);
}

PYBIND11_MODULE(cimg_bindings, m)
{
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: python_example

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    declare<float>(m, "float32");
    declare<uint8_t>(m, "uint8");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
