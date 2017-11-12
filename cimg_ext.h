#define cimg_use_zlib 1
#define cimg_use_jpeg 1
#define cimg_use_png  1 
#include <png.h>
#include <CImg.h>
#include <half.hpp>
#include <iostream>
#include <utility>

namespace cimg_library{

template<class T>
CImg<T> load_float16(const char* filename)
{
  CImg<half_float::half> im;
  im.load_cimg(filename);
  return std::move(CImg<T>(im));
}

}
