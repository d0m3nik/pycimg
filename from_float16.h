#include <utility>
#include <CImg.h>
#include <half.hpp>

namespace cimg_library{

CImg<float> from_float16(const char* filename)
{
  CImg<half_float::half> im(filename);
  return std::move(CImg<float>(im));
}

}
