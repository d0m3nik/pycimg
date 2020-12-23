import numbers
import numpy as np

from .cimg_bindings import CImg_uint8, CImg_uint16, CImg_uint32, CImg_float32, CImg_float64

# Supported numeric pixel type
uint8 = np.uint8
uint16 = np.uint16
uint32 = np.uint32
float32 = np.float32
float64 = np.float64

# Interpolation type
NONE_RAW = -1
NONE = 0
NEAREST = 1
MOVING_AVERAGE = 2
LINEAR = 3
GRID = 4
CUBIC = 5
LANCZOS = 6

# Boundary condition type
DIRICHLET = 0
NEUMANN = 1
PERIODIC = 2
MIRROR = 3

# Variance method
SECOND_MOMENT = 0
BEST_UNBIASED = 1
LEAST_MEDIAN_SQ = 2
LEAST_TRIMMED_SQ = 3

# Norm type
LINF_NORM = -1
L0_NORM = 0
L1_NORM = 1
L2_NORM = 2

# Rounding type
R_BACKWARD = -1
R_NEAREST = 0
R_FORWARD = 1

# Noise type
GAUSSIAN = 0
UNIFORM = 1
SALT_AND_PEPPER = 2
POISSON = 3
RICIAN = 4

# Compression type
C_NONE = 0
C_LZW = 1
C_JPEG = 2

# Filter order
SMOOTH_FILTER = 0
FIRST_DERIV = 1
SECOND_DERIV = 2
THIRD_DERIV = 3

# Plot type
POINTS = 0
SEGMENTS = 1
SPLINES = 2
BARS = 3


class CImg:
    """ CImg is a wrapper class for the CImg library: """

    def __init__(self, *args, **kwargs):
        """ Create CImg with given data type.

            Supported datatypes are int8, int16, int32,
            uint8, uint16, uint32, float32, and float64.

            Examples:
                1. Create empty image with default type float32
                im = CImg()

                2. Create image from file.
                im = CImg("filename.png")

                3. Create image from numpy array
                arr = np.zeros((100,2))
                im = CImg(arr)

                4. Create image of size 100x200 with data type uint8
                im = CImg((100, 200), dtype=uint8)

            Args:
                Either image filename, numpy array, or image size.

            Keyword arguments:
                dtype: Data type of CImg.

            Raises:
                RuntimeError: For unsupported data types.
        """
        self.dtype = kwargs.get('dtype', float32)

        if self.dtype == np.uint8:
            self._cimg = CImg_uint8()
        elif self.dtype == np.uint16:
            self._cimg = CImg_uint16()
        elif self.dtype == np.uint32:
            self._cimg = CImg_uint32()
        elif self.dtype == np.float32:
            self._cimg = CImg_float32()
        elif self.dtype == np.float64:
            self._cimg = CImg_float64()
        else:
            raise RuntimeError("Unknown data type '{}'".format(self.dtype))
        if len(args) == 1:
            if isinstance(args[0], str):
                self.load(args[0])
            elif isinstance(args[0], np.ndarray):
                self.fromarray(args[0])
            elif isinstance(args[0], CImg):
                self.fromarray(args[0].asarray())
            elif isinstance(args[0], tuple):
                shape = [max(1, sz) for sz in args[0]]
                self.resize(*shape, interpolation_type=NONE_RAW)
            elif isinstance(args[0], int):
                sz = max(1, args[0])
                self.resize(sz, interpolation_type=NONE_RAW)
            else:
                raise RuntimeError("Type of first argument not supported")
        elif len(args) > 1:
            raise RuntimeError("More than one argument not supported")

    def asarray(self, copy=False):
        return np.array(self._cimg, copy=copy)

    @property
    def width(self):
        """ Return width of image. """
        return self._cimg.width()

    @property
    def height(self):
        """ Return height of image. """
        return self._cimg.height()

    @property
    def depth(self):
        """ Return depth of image. """
        return self._cimg.depth()

    @property
    def spectrum(self):
        """ Return spectrum (number of channels) of image. """
        return self._cimg.spectrum()

    @property
    def shape(self):
        """ Return shape of image data. """
        return (self.spectrum, self.depth, self.height, self.width)

    @property
    def size(self):
        """ Return the total number of pixel values in the image. """
        return self._cimg.size()

    def isempty(self):
        return self.width == 0 and  \
               self.height == 0 and \
               self.depth == 0 and  \
               self.spectrum == 0

    def __eq__(self, img):
        return self._cimg == img._cimg

    def __neq__(self, img):
        return self._cimg != img._cimg

    def __add__(self, other):
        return CImg(self.asarray() + (other.asarray() if isinstance(other, CImg) else other))

    def __sub__(self, other):
        return CImg(self.asarray() - (other.asarray() if isinstance(other, CImg) else other))

    def __mul__(self, other):
        return CImg(self.asarray() * (other.asarray() if isinstance(other, CImg) else other))

    def __truediv__(self, other):
        return CImg(self.asarray() / (other.asarray() if isinstance(other, CImg) else other))

    def __floordiv__(self, other):
        return CImg(self.asarray() // (other.asarray() if isinstance(other, CImg) else other))

    def __iadd__(self, other):
        a = self.asarray()
        a += (other.asarray() if isinstance(other, CImg) else other)
        return self

    def __isub__(self, other):
        a = self.asarray()
        a -= (other.asarray() if isinstance(other, CImg) else other)
        return self

    def __imul__(self, other):
        a = self.asarray()
        a *= (other.asarray() if isinstance(other, CImg) else other)
        return self

    def __itruediv__(self, other):
        a = self.asarray()
        a /= (other.asarray() if isinstance(other, CImg) else other)
        return self

    def __ifloordiv__(self, other):
        a = self.asarray()
        a //= (other.asarray() if isinstance(other, CImg) else other)
        return self

    def __repr__(self):
        if self.isempty():
            return 'CImg()'
        return 'CImg(' + repr(self.asarray()) + ')'

    def __str__(self):
        if self.isempty():
            arr = None
        else:
            arr = self.asarray()
        return "%s %5d\n%s %5d\n%s %5d\n%s %5d\n%s\n%s" % \
                ("height:  ", self.height,
                 "width:   ", self.width,
                 "depth:   ", self.depth,
                 "spectrum:", self.spectrum,
                 "data:    ", arr) 

    def __getattr__(self, attr):
        if hasattr(self._cimg, attr):
            def wrapper(*args, **kwargs):
                # Unwrap CImg arguments
                cargs = [arg._cimg if isinstance(arg, CImg) else arg for arg in args]
                cargs = []
                for arg in args:
                    if isinstance(arg, CImg):
                        cargs.append(arg._cimg)
                    else:
                        cargs.append(arg)
                return getattr(self._cimg, attr)(*cargs, **kwargs)
            wrapper.__doc__ = getattr(self._cimg, attr).__doc__
            wrapper.__name__ = attr
            return wrapper
        raise AttributeError(attr)

    def _check_index(self, index):
        cls = type(self)
        def raiseError():
            msg = 'only integers and slices (`:`) are valid indices'
            raise IndexError(msg.format(cls=cls))

        # Handle special case of single index
        if isinstance(index, numbers.Integral):
            index = tuple([index])
        if isinstance(index, tuple):
            # Check number of indices
            if len(index) > 4:
                raise IndexError('Image has < 5 dimensions.')
            index = list(index)
            # Case 1: indices are a mix of integers and slices
            if any(map(lambda t: isinstance(t, slice), index)):
                # Expand integers to slices
                slice_index = []
                for idx in index:
                    if isinstance(idx, numbers.Integral):
                        slice_index.append(slice(idx, idx+1, None))
                    elif isinstance(idx, slice):
                        slice_index.append(idx)
                    else:
                        raiseError()
                index = slice_index
                # Expand slices to cover all dimensions
                while len(index) < 4:
                    index.append(slice(None, None, None))
                index = list(reversed(index))
                return (index, True)
            # Case 2: all indices are integers
            elif all(map(lambda t: isinstance(t, numbers.Integral), index)):
                # Expand indices to cover all dimensions
                while len(index) < 4:
                    index.append(0)
                index = tuple(reversed(index))
                return (index, False)
            else:
                raiseError()
        else:
            raiseError()

    def __getitem__(self, index):
        index, is_slice = self._check_index(index)
        if is_slice:
            cls = type(self)
            return cls(self.asarray()[tuple(index)])
        else:
            return self.asarray()[index]

    def __setitem__(self, index, value):
        index, is_slice = self._check_index(index)
        self.asarray()[tuple(index)] = value
