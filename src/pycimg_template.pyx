from libcpp.vector cimport vector


cdef class CImg_{T}:
    cdef CImg[{T}] _cimg

    def load(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg.load(fn)

    def load_bmp(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg.load_bmp(fn)

    def load_jpeg(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg.load_jpeg(fn)

    def load_png(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        cdef unsigned int bits_per_pixel = 0
        self._cimg.load_png(fn, &bits_per_pixel)
        return bits_per_pixel

    def load_tiff(self, filename, first_frame,
                  last_frame, step_frame):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        cdef float voxel_size = 0.0
        self._cimg.load_tiff(fn, first_frame,
                             last_frame, step_frame,
                             &voxel_size, NULL)
        # TODO description out param
        return voxel_size

    def load_cimg(self, filename, axis, align):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        byte_string = axis.encode('UTF-8')
        cdef char* _axis = byte_string
        self.load_cimg(fn, _axis, align)

    def save(self, filename, number, digits):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg.save(fn, number, digits)

    def save_bmp(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg.save_bmp(fn)

    def save_jpeg(self, filename, quality):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg.save_jpeg(fn, quality)

    def save_png(self, filename, bytes_per_pixel):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg.save_png(fn, bytes_per_pixel)

    def save_tiff(self, filename, compression_type,
                  voxel_size, description, use_bigtiff):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        byte_string = description.encode('UTF-8')
        cdef char* _description = byte_string
        cdef float _voxel_size = voxel_size
        self._cimg.save_tiff(fn, compression_type, &_voxel_size,
                             _description, use_bigtiff)

    def save_cimg(self, filename, is_compressed):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self.save_cimg(fn, is_compressed)

    def load_cimg_float16(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg = load_float16[{T}](fn)

    def save_cimg_float16(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        save_float16[{T}](self._cimg, fn)

    ############################################################################
    # Equality
    ############################################################################
    def _equal(self, img):
        cdef CImg_{T} _img = img
        return self._cimg == _img._cimg

    def _not_equal(self, img):
        cdef CImg_{T} _img = img
        return self._cimg != _img._cimg

    ############################################################################
    # Instance characteristics
    ############################################################################
    def width(self):
        return self._cimg.width()

    def height(self):
        return self._cimg.height()

    def depth(self):
        return self._cimg.depth()

    def spectrum(self):
        return self._cimg.spectrum()

    def size(self):
        return self._cimg.size()

    def fromarray(self, arr):
        ndim = len(arr.shape)
        if ndim > 4:
            raise RuntimeError('Cannot convert from array with %d > 4 dimensions' % ndim)
        x = 1
        y = 1
        z = 1
        c = 1
        shape = list(reversed(arr.shape))
        if len(shape) == 1:
            x = shape[0]
        elif len(shape) == 2:
            x, y = shape
        elif len(shape) == 3:
            x, y, z = shape
        elif len(shape) == 4:
            x, y, z, c = shape
        self.resize(x, y, z, c, interpolation_type=-1,
                boundary_conditions=0,
                centering_x=0,
                centering_y=0,
                centering_z=0,
                centering_c=0
                )
        a = self.asarray()
        a[:] = arr[:]


    def asarray(self):
        cdef int width = self.width()
        cdef int height = self.height()
        cdef int depth = self.depth()
        cdef int spectrum = self.spectrum()
        cdef {T}* data = self._cimg.data()
        # For cimg storage format see: http://cimg.eu/reference/group__cimg__storage.html
        cdef {T}[:,:,:,::1] mem_view = <{T}[:spectrum,:depth,:height,:width]>data
        return np.asarray(mem_view)

    def linear_atX(self, fx, y, z, c):
        return self._cimg.linear_atX(fx, y, z, c)

    def linear_atXY(self, fx, fy, z, c):
        return self._cimg.linear_atXY(fx, fy, z, c)

    def linear_atXYZ(self, fx, fy, fz, c):
        return self._cimg.linear_atXYZ(fx, fy, fz, c)

    def linear_atXYZC(self, fx, fy, fz, fc):
        return self._cimg.linear_atXYZC(fx, fy, fz, fc)


    ############################################################################
    # Mathmatical functions
    ############################################################################
    def sqr(self):
        self._cimg.sqr()
        return self

    def sqrt(self):
        self._cimg.sqrt()
        return self

    def exp(self):
        self._cimg.exp()
        return self

    def log(self):
        self._cimg.log()
        return self

    def log2(self):
        self._cimg.log2()
        return self

    def log10(self):
        self._cimg.log10()
        return self

    def abs(self):
        self._cimg.abs()
        return self

    def sign(self):
        self._cimg.sign()
        return self

    def cos(self):
        self._cimg.cos()
        return self

    def sin(self):
        self._cimg.sin()
        return self

    def sinc(self):
        self._cimg.sinc()
        return self

    def tan(self):
        self._cimg.tan()
        return self

    def sinh(self):
        self._cimg.sinh()
        return self

    def tanh(self):
        self._cimg.tanh()
        return self

    def acos(self):
        self._cimg.acos()
        return self

    def asin(self):
        self._cimg.asin()
        return self

    def atan(self):
        self._cimg.atan()
        return self

    def atan2(self, img):
        cdef CImg_{T} _img = img
        self._cimg.atan2(_img._cimg)
        return self

    def mul(self, img):
        cdef CImg_{T} _img = img
        self._cimg.mul(_img._cimg)
        return self

    def div(self, img):
        cdef CImg_{T} _img = img
        self._cimg.div(_img._cimg)
        return self

    def pow(self, p):
        self._cimg.pow(p)
        return self

    def min_max(self):
        cdef {T} max_val = 0
        cdef {T} min_val = 0
        min_val = self._cimg.min_max(max_val)
        return (min_val, max_val)

    def max_min(self):
        cdef {T} max_val = 0
        cdef {T} min_val = 0
        max_val = self._cimg.max_min(min_val)
        return (max_val, min_val)

    def kth_smallest(self, k):
        return self._cimg.kth_smallest(k)

    def variance(self, variance_method):
        return self._cimg.variance(variance_method)

    def variance_mean(self, variance_method):
        cdef {T} mean = 0
        cdef double v = 0.0
        v = self._cimg.variance_mean(variance_method, mean)
        return (v, mean)

    def variance_noise(self, variance_method):
        return self._cimg.variance_noise(variance_method)

    def mse(self, img):
        cdef CImg_{T} _img = img
        return self._cimg.MSE(_img._cimg)

    def psnr(self, img, max_value):
        cdef CImg_{T} _img = img
        return self._cimg.PSNR(_img._cimg, max_value)

    def magnitude(self, magnitude_type):
        return self._cimg.magnitude(magnitude_type)

    def dot(self, img):
        cdef CImg_{T} _img = img
        return self._cimg.dot(_img._cimg)

    # ...

    # Value manipulation
    def fill(self, val):
        self._cimg.fill(val)
        return self

    def invert_endianness(self):
        self._cimg.invert_endianness()
        return self

    def rand(self, val_min, val_max):
        self._cimg.rand(val_min, val_max)
        return self

    def round(self, y, rounding_type):
        self._cimg.round(y, rounding_type)
        return self

    def noise(self, sigma, noise_type):
        self._cimg.noise(sigma, noise_type)
        return self

    def normalize(self, min_value, max_value):
        self._cimg.normalize(min_value, max_value)
        return self

    def normalize_l2(self):
        self._cimg.normalize()
        return self

    def norm(self, norm_type):
        self._cimg.norm(norm_type)
        return self

    def cut(self, min_value, max_value):
        self._cimg.cut(min_value, max_value)
        return self

    def quantize(self, nb_levels, keep_range):
        self._cimg.quantize(nb_levels, keep_range)
        return self

    def threshold(self, value, soft_threshold, strict_threshold):
        self._cimg.threshold(value, soft_threshold, strict_threshold)
        return self

    def histogram(self, nb_levels, min_value, max_value):
        self._cimg.histogram(nb_levels, min_value, max_value)
        return self

    def equalize(self, nb_levels, min_value, max_value):
        self._cimg.equalize(nb_levels, min_value, max_value)
        return self

    def index(self, colormap, dithering, map_indexes):
        cdef CImg_{T} _colormap = colormap
        self._cimg.index(_colormap._cimg, dithering, map_indexes)
        return self

    def map(self, colormap, boundary_conditions):
        cdef CImg_{T} _colormap = colormap
        self._cimg.map(_colormap._cimg, boundary_conditions)
        return self

    def label(self, is_high_connectivity, tolerance):
        self._cimg.label(is_high_connectivity, tolerance)
        return self

    ############################################################################
    # Geometric / Spatial Manipulation
    ############################################################################
    def resize(self, size_x, size_y, size_z, size_c,
            interpolation_type, boundary_conditions,
            centering_x,
            centering_y,
            centering_z,
            centering_c):
        self._cimg.resize(size_x, size_y, size_z, size_c,
                interpolation_type, boundary_conditions,
                centering_x,
                centering_y,
                centering_z,
                centering_c)
        return self

    def resize_halfXY(self):
        self._cimg.resize_halfXY()
        return self

    def resize_doubleXY(self):
        self._cimg.resize_doubleXY()
        return self

    def resize_tripleXY(self):
        self._cimg.resize_tripleXY()
        return self

    def mirror(self, axes):
        byte_string = axes.encode('UTF-8')
        cdef char* _axes = byte_string
        self._cimg.mirror(_axes)
        return self

    def shift(self, delta_x, delta_y, delta_z, delta_c, boundary_conditions):
        self._cimg.shift(delta_x, delta_y, delta_z, delta_c, boundary_conditions)
        return self

    def permute_axes(self, order):
        byte_string = order.encode('UTF-8')
        cdef char* _order = byte_string
        self._cimg.permute_axes(_order)
        return self

    def unroll(self, axis):
        byte_string = axis.encode('UTF-8')
        cdef char* _axis = byte_string
        self._cimg.unroll(_axis[0])
        return self

    def rotate(self, angle, interpolation, boundary_conditions):
        self._cimg.rotate(angle, interpolation, boundary_conditions)
        return self

    def warp(self, warp, mode, interpolation, boundary_conditions):
        cdef CImg_{T} _warp = warp
        self._cimg.warp(_warp._cimg, mode, interpolation, boundary_conditions)
        return self

    def apply_geometric_transform(self, s, M, t):
        cdef CImg_{T} _M = M
        cdef CImg_{T} _t = t
        self._cimg = apply_geometric_transform[{T}](self._cimg, s, _M._cimg, _t._cimg)
        return self

    def crop(self, x0, y0, z0, c0, x1, y1, z1, c1, boundary_conditions):
        self._cimg.crop(x0, y0, z0, c0, x1, y1, z1, c1, boundary_conditions)
        return self

    def autocrop(self, color, axes):
        byte_string = axes.encode('UTF-8')
        cdef char* _axes = byte_string
        cdef vector[{T}] _color
        if color != 0:
            _color = color
            self._cimg.autocrop(_color.data(), _axes)
        else:
            self._cimg.autocrop(<{T}*>0, _axes)
        return self

    def append(self, img, axis, align):
        cdef CImg_{T} _img = img
        byte_string = axis.encode('UTF-8')
        cdef char* _axis = byte_string
        self._cimg.append(_img._cimg, _axis[0], align)


    ############################################################################
    # Filtering / Transforms
    ############################################################################
    def correlate(self, kernel, boundary_conditions, is_normalized):
        cdef CImg_{T} _kernel = kernel
        self._cimg.correlate(_kernel._cimg, boundary_conditions, is_normalized)
        return self

    def convolve(self, kernel, boundary_conditions, is_normalized):
        cdef CImg_{T} _kernel = kernel
        self._cimg.convolve(_kernel._cimg, boundary_conditions, is_normalized)
        return self

    def cumulate(self, axes):
        byte_string = axes.encode('UTF-8')
        cdef char* _axes = byte_string
        self._cimg.cumulate(_axes)
        return self

    def erode(self, kernel, boundary_conditions, is_real):
        cdef CImg_{T} _kernel = kernel
        self._cimg.erode(_kernel._cimg, boundary_conditions, is_real)
        return self

    def dilate(self, kernel, boundary_conditions, is_real):
        cdef CImg_{T} _kernel = kernel
        self._cimg.dilate(_kernel._cimg, boundary_conditions, is_real)
        return self

    def watershed(self, priority, is_high_connectivity):
        cdef CImg_{T} _priority = priority
        self._cimg.watershed(_priority._cimg, is_high_connectivity)
        return self

    def deriche(self, sigma, order, axis, boundary_conditions):
        byte_string = axis.encode('UTF-8')
        cdef char* _axis = byte_string
        self._cimg.deriche(sigma, order, _axis[0], boundary_conditions)
        return self

    def vanvliet(self, sigma, order, axis, boundary_conditions):
        byte_string = axis.encode('UTF-8')
        cdef char* _axis = byte_string
        self._cimg.vanvliet(sigma, order, _axis[0], boundary_conditions)
        return self

    def blur(self, sigma, boundary_conditions, is_gaussian):
        self._cimg.blur(sigma, boundary_conditions, is_gaussian)
        return self

    def boxfilter(self, boxsize, order, axis, boundary_conditions, nb_iter):
        byte_string = axis.encode('UTF-8')
        cdef char* _axis = byte_string
        self._cimg.boxfilter(boxsize, order, _axis[0], boundary_conditions, nb_iter)
        return self

    def blur_box(self, boxsize, boundary_conditions):
        self._cimg.blur_box(boxsize, boundary_conditions)
        return self

    def blur_median(self, n, threshold):
        self._cimg.blur_median(n, threshold)
        return self

    def sharpen(self, amplitude, sharpen_type, edge, alpha, sigma):
        self._cimg.sharpen(amplitude, sharpen_type, edge, alpha, sigma)
        return self

    ############################################################################
    # Drawing functions
    ############################################################################
    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color, opacity):
        cdef vector[{T}] _color = color
        self._cimg.draw_triangle(x0, y0, x1, y1, x2, y2, _color.data(), opacity)
        return self

    def draw_rectangle(self, x0, y0, x1, y1, color, opacity):
        cdef vector[{T}] _color = color
        self._cimg.draw_rectangle(x0, y0, x1, y1, _color.data(), opacity)
        return self

    def draw_polygon(self, points, color, opacity):
        cdef vector[{T}] _color = color
        cdef CImg_uint32 _points = CImg_uint32()
        _points.fromarray(points)
        draw_polygon(self._cimg, _points._cimg, _color.data(), opacity)

    def draw_circle(self, x0, y0, radius, color, opacity):
        cdef vector[{T}] _color = color
        self._cimg.draw_circle(x0, y0, radius, _color.data(), opacity)

    def draw_text(self, x0, y0, text, foreground_color,
                  background_color, opacity, font_height):
        cdef vector[{T}] _fc = foreground_color
        cdef vector[{T}] _bc = background_color
        byte_string = text.encode('UTF-8')
        cdef char* _text = byte_string
        self._cimg.draw_text(x0, y0, _text, _fc.data(), _bc.data(),
                             opacity, font_height)

    def display(self, title):
        byte_string = title.encode('UTF-8')
        cdef char* _title = byte_string
        self._cimg.display(_title)

    def display_graph(self, plot_type, vertex_type,
                      labelx, xmin, xmax,
                      labely, ymin, ymax):
        cdef CImgDisplay disp = CImgDisplay()
        byte_string = labelx.encode('UTF-8')
        cdef char* _labelx = byte_string
        byte_string = labely.encode('UTF-8')
        cdef char* _labely = byte_string
        self._cimg.display_graph(disp, plot_type, vertex_type,
                                 _labelx, xmin, xmax,
                                 _labely, ymin, ymax)
