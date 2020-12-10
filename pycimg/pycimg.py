
import numpy as np

from .cimg_bindings import CImg_float32, CImg_uint8

# Supported numeric pixel type
int8 = np.int8
int16 = np.int16
int32 = np.int32
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
        dtype = kwargs.get('dtype', float32)

        if dtype == np.int8:
            self._cimg = CImg_int8()
        elif dtype == np.int16:
            self._cimg = CImg_int16()
        elif dtype == np.int32:
            self._cimg = CImg_int32()
        elif dtype == np.uint8:
            self._cimg = CImg_uint8()
        elif dtype == np.uint16:
            self._cimg = CImg_uint16()
        elif dtype == np.uint32:
            self._cimg = CImg_uint32()
        elif dtype == np.float32:
            self._cimg = CImg_float32()
        elif dtype == np.float64:
            self._cimg = CImg_float64()
        else:
            raise RuntimeError("Unknown data type '{}'".format(dtype))
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

    def __getattr__(self, name):
        return getattr(self._cimg, name)