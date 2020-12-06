#include <pybind11/pybind11.h>
//#define cimg_display 0
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
    py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol())
        .def(py::init<>())
        .def("load", &Class::load)
        .def("width", &Class::width)
        .def("height", &Class::height)
        .def_buffer([](Class &c) -> py::buffer_info {
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
        })
        .def("display",
             (const Class &(Class::*)(const char *const, const bool, unsigned int *const, const bool) const)(&Class::display),
             "Display image",
             py::arg("title") = "",
             py::arg("display_info") = true,
             py::arg("XYZ") = 0,
             py::arg("exit_on_anykey") = false);
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
    declare<int>(m, "int32");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
