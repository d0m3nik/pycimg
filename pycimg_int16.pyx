cdef class CImg_int16:
    cdef CImg[int16] _cimg;

    # Constructors
#    def __cinit__(self, filename):
#        byte_string = filename.encode('UTF-8')
#        cdef char* fn = byte_string
#        self._cimg = CImg[int16](fn)

    def load(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg.load(fn)

    def load_cimg_float16(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        self._cimg = from_float16[int16](fn)



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
#    # TODO: Not working atm
#    def __add__(self, rhs):
#        return self._cimg + rhs


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
        cdef int16* data = self._cimg.data()
        # For cimg storage format see: http://cimg.eu/reference/group__cimg__storage.html
        cdef int16[:,:,:,::1] mem_view = <int16[:spectrum,:depth,:height,:width]>data
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

    # ...
    def noise(self, sigma, noise_type):
        self._cimg.noise(sigma, noise_type)
        return self

    def normalize(self, min_value, max_value):
        self._cimg.normalize(min_value, max_value)
        return self



    cpdef display(self):
        self._cimg.display()




