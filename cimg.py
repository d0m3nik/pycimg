from pycimg import CImg_int8, CImg_int16, CImg_int32, CImg_uint8, CImg_uint16, CImg_uint32, CImg_float16, CImg_float32, CImg_float64

class CImg:
    """ CImg is a wrapper class for the CImg library: """

    def __init__(self, filename, dtype):
        if dtype == 'int8':
            self._cimg = CImg_int8(filename)
        elif dtype == 'int16':
            self._cimg = CImg_int16(filename)
        elif dtype == 'int32':
            self._cimg = CImg_int32(filename)
        elif dtype == 'uint8':
            self._cimg = CImg_uint8(filename)
        elif dtype == 'uint16':
            self._cimg = CImg_uint16(filename)
        elif dtype == 'uint32':
            self._cimg = CImg_uint32(filename)
        elif dtype == 'float16':
            self._cimg = CImg_float16(filename)
        elif dtype == 'float32':
            self._cimg = CImg_float32(filename)
        elif dtype == 'float64':
            self._cimg = CImg_float64(filename)
        else:
            raise RuntimeError('Unknown data type ''%s''' % dtype)

    # Operators
    def __call__(self, x):
        self._cimg(x)

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
        return self._cimg.asarray()

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

    def display(self):
        self._cimg.display()


