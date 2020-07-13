#define cimg_use_zlib 1
#define cimg_use_jpeg 1
#define cimg_use_png  1
#define cimg_use_tiff 1
#ifndef __APPLE__
#define cimg_use_openmp 1
#endif
#include <png.h>
#include <CImg.h>
#include <half.hpp>
#include <iostream>
#include <utility>

namespace cimg_library {

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

template<class T>
CImg<T> apply_geometric_transform(const CImg<T> &src, const float s, const CImg<T>& M, const CImg<T>& t)
{
  CImg<> dst = src;
  CImg<> Q = M.get_invert();
  cimg_pragma_openmp(parallel for cimg_openmp_collapse(3) cimg_openmp_if_size(dst.size(),4096))
  cimg_forXYZ(dst,x,y,z) {
    CImg<> p = CImg<>::vector((z-t(0))/s,(x-t(1))/s,(y-t(2))/s);
    p = Q * p;
    dst(x,y,z) = src.linear_atXYZ(p(1),p(2),p(0));
  }
  return dst;
}

} // namespace cimg_library
