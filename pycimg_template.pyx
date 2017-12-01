from libcpp.vector cimport vector

cdef class CImg_{T}:
    cdef CImg[{T}] _cimg

    def load(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg.load(fn)

#    def load_cimg(self, filename, axis='z', align=0):
#        byte_string = filename.encode('UTF-8')
#        cdef char* fn = byte_string
#        self._cimg.load_cimg(fn, axis, align)


    def load_cimg_float16(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg = load_float16[{T}](fn)

    def save_cimg_float16(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        save_float16[{T}](self._cimg, fn)

    def save(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg.save(fn)

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
        self._cimg.atan2(<CImg[{T}]&>img._cimg)
        return self

    def mul(self, img):
        self._cimg.mul(<CImg[{T}]&>img._cimg)
        return self

    def div(self, img):
        self._cimg.div(<CImg[{T}]&>img._cimg)
        return self

    def pow(self, p):
        self._cimg.pow(p)
        return self


    # ...

    # Value manipulation
    def fill(self, val):
        self._cimg.fill(val)
        return self
    # ...

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
    
    # TODO: index, map

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

    ############################################################################
    # Drawing functions
    ############################################################################
    def draw_rectangle(self, x0, y0, x1, y1, color, opacity):
        cdef vector[{T}] _color = color
        self._cimg.draw_rectangle(x0, y0, x1, y1, _color.data(), opacity)
        return self

    def draw_polygon(self, points, color, opacity):
       cdef vector[{T}] _color = color
       cdef CImg_{T} _points = CImg_{T}()
       _points.fromarray(points)
       self._cimg.draw_polygon(_points._cimg, _color.data(), opacity)

    def draw_circle(self, x0, y0, radius, color, opacity):
       cdef vector[{T}] _color = color
       self._cimg.draw_circle(x0, y0, radius, _color.data(), opacity)
        

    # def draw_polygon(self, points, color, opacity):
    #     cdef vector[{T}] _color = color
    #     cdef int n = len(points)
    #     cdef CImg_{T} _cp = CImg_{T}()
    #     _cp.resize(n, 2, 1, 1, 0, 1, 0, 0, 0, 0)
    #     _points = _cp.asarray().transpose((3,2,1,0)).squeeze()
    #     for i in range(n):
    #         _points[i,0] = points[i][0]
    #         _points[i,1] = points[i][1]
    #     self._cimg.draw_polygon(_cp._cimg, _color.data(), opacity)

    cpdef display(self):
        self._cimg.display()

