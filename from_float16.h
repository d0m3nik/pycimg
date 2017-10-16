#include <utility>
#define cimg_use_zlib 1
#include <CImg.h>
#include <half.hpp>
#include <iostream>

namespace cimg_library{

template<class T>
CImg<T> from_float16(const char* filename)
{
  std::cout << "from_float16" << std::endl;
  CImg<half_float::half> im;
  im.load_cimg(filename);
  return std::move(CImg<T>(im));
}

}
