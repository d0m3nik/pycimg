cdef class CImg_{T}:
    cdef CImg[{T}] _cimg;

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



    # Operators
#    def __call__(self, x):
#        if isinstance(x, tuple):
#            if len(x) == 2:
#                return self._cimg(x[0], x[1])
#            elif len(x) == 3:
#                return self._cimg(x[0], x[1], x[2])
#            elif len(x) == 4:
#                return self._cimg(x[0], x[1], x[2], x[3])
#            else:
#                raise RuntimeError('Element access with >4 dimensions')
#        return self._cimg(x)
#

    # Instance characteristics
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

    def asarray(self):
        cdef int width = self.width()
        cdef int height = self.height()
        cdef int depth = self.depth()
        cdef int spectrum = self.spectrum()
        cdef {T}* data = self._cimg.data()
        # For cimg storage format see: http://cimg.eu/reference/group__cimg__storage.html
        cdef {T}[:,:,:,::1] mem_view = <{T}[:spectrum,:depth,:height,:width]>data
        return np.asarray(mem_view)

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
    def noise(self, sigma, noise_type):
        self._cimg.noise(sigma, noise_type)
        return self

    def normalize(self, min_value, max_value):
        self._cimg.normalize(min_value, max_value)
        return self

    cpdef display(self):
        self._cimg.display()

