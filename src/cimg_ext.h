#define cimg_use_zlib 1
#define cimg_use_jpeg 1
#define cimg_use_png  1 
#define cimg_use_tiff 1 
#include <png.h>
#include <CImg.h>
#include <half.hpp>
#include <iostream>
#include <utility>

namespace cimg_library{

template<class T>
void draw_polygon(CImg<T>& img, CImg<uint32_t> const& points, const T* const color, const float opacity)
{
  img.draw_polygon(points, color, opacity);
}

template<class T>
CImg<T> load_float16(const char* filename)
{
  CImg<half_float::half> img;
  img.load_cimg(filename);
  return std::move(CImg<T>(img));
}

template<class T>
void save_float16(CImg<T> const& img, const char* filename)
{
  CImg<half_float::half> img_half(img);
  img_half.save_cimg(filename);
}

} // namespace cimg_library 
