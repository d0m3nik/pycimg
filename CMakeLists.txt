cmake_minimum_required(VERSION 3.28...3.31)
project(pycimg LANGUAGES CXX)

if(DEFINED SKBUILD_PROJECT_VERSION)
    set(PROJECT_VERSION "${SKBUILD_PROJECT_VERSION}")
else()
    set(PROJECT_VERSION "0.0.0")
endif()

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

find_package(JPEG REQUIRED)
find_package(PNG REQUIRED)
find_package(TIFF REQUIRED)
find_package(ZLIB REQUIRED)

pybind11_add_module(cimg_bindings MODULE src/cimg_bindings.cpp)

target_include_directories(cimg_bindings PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/CImg-3.1.6
)

target_link_libraries(cimg_bindings PRIVATE
    JPEG::JPEG
    PNG::PNG
    TIFF::TIFF
    ZLIB::ZLIB
)

target_compile_definitions(cimg_bindings PRIVATE
    VERSION_INFO="${PROJECT_VERSION}"
)

if(APPLE)
    target_compile_options(cimg_bindings PRIVATE
        -stdlib=libc++ -mmacosx-version-min=10.15
    )
    target_link_options(cimg_bindings PRIVATE
        -stdlib=libc++ -mmacosx-version-min=10.15
    )
    target_include_directories(cimg_bindings PRIVATE /usr/X11R6/include)
    target_link_directories(cimg_bindings PRIVATE /usr/X11R6/lib)
    target_link_libraries(cimg_bindings PRIVATE pthread X11)
endif()

if(WIN32)
    target_compile_options(cimg_bindings PRIVATE /MD /openmp /std:c++17)
    target_link_libraries(cimg_bindings PRIVATE gdi32 user32 shell32)
endif()

if(UNIX AND NOT APPLE)
    target_compile_options(cimg_bindings PRIVATE -fopenmp)
    target_link_libraries(cimg_bindings PRIVATE pthread X11)
    target_link_options(cimg_bindings PRIVATE -fopenmp)
endif()

install(TARGETS cimg_bindings LIBRARY DESTINATION ${PROJECT_NAME})
