#include <pybind11/pybind11.h>
//#define cimg_display 0
#include "CImg.h"

using namespace cimg_library;

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

PYBIND11_MODULE(cimg_bindings, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: python_example

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    py::class_<CImg<float>>(m, "CImg_float")
        .def(py::init<>())
        .def("load", &CImg<float>::load)
        .def("width", &CImg<float>::width)
        .def("height", &CImg<float>::height)
        .def("display", 
            (const CImg<float>& (CImg<float>::*)(const char *const, const bool, unsigned int *const, const bool) const)(&CImg<float>::display),
            "Display image", 
            py::arg("title") = "", 
            py::arg("display_info") = true, 
            py::arg("XYZ") = 0, 
            py::arg("exit_on_anykey") = false 
            );

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
