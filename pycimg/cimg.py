import numbers
import os.path
import numpy as np
from .pycimg import CImg_int8, CImg_int16, CImg_int32 
from .pycimg import CImg_uint8, CImg_uint16, CImg_uint32
from .pycimg import CImg_float32, CImg_float64

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
                self._cimg.fromarray(args[0])
            elif isinstance(args[0], CImg):
                self._cimg.fromarray(args[0].asarray())
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

    def __eq__(self, img):
        return self._cimg._equal(img._cimg)

    def __neq__(self, img):
        return self._cimg._not_equal(img._cimg)

    def isempty(self):
        return self.width == 0 and  \
               self.height == 0 and \
               self.depth == 0 and  \
               self.spectrum == 0

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


    def load(self, filename):
        """ Load image from a file.

            Args:
                filename (str): Filename of image.
            Raises:
                RuntimeError: If file does not exist.
        """
        if os.path.isfile(filename):
            self._cimg.load(filename)
        else:
            raise RuntimeError("File '{}' does not exist".format(filename))

    def load_bmp(self, filename):
        """ Load image from a BMP file.

            Args:
                filename (str): Filename of image.
            Raises:
                RuntimeError: If file does not exist.
        """
        if os.path.isfile(filename):
            self._cimg.load_bmp(filename)
        else:
            raise RuntimeError("File '{}' does not exist".format(filename))


    def load_jpeg(self, filename):
        """ Load image from a JPEG file.

            Args:
                filename (str): Filename of image.
            Raises:
                RuntimeError: If file does not exist.
        """
        if os.path.isfile(filename):
            self._cimg.load_jpeg(filename)
        else:
            raise RuntimeError("File '{}' does not exist".format(filename))

    def load_png(self, filename):
        """ Load image from a PNG file.

            Args:
                filename (str): Filename of image.
            Returns:
                Bits per pixel
            Raises:
                RuntimeError: If file does not exist.
        """
        if os.path.isfile(filename):
            return self._cimg.load_png(filename)
        else:
            raise RuntimeError("File '{}' does not exist".format(filename))

    def load_tiff(self, filename, first_frame=0, last_frame=0xFFFFFFFF, step_frame=1):
        """ Load image from a TIFF file.

            Args:
                filename (str): Filename of image.
                first_frame: First frame to read (for multi-pages tiff).
                last_frame: Last frame to read (for multi-pages tiff).
                step_frame: Step value of frame reading.
            Returns:
                Voxel size, as stored in the filename.
            Raises:
                RuntimeError: If file does not exist.
        """
        if os.path.isfile(filename):
            return self._cimg.load_tiff(filename, first_frame, last_frame, step_frame)
        else:
            raise RuntimeError("File '{}' does not exist".format(filename))


    def load_cimg(self, filename, axis='z', align=0):
        """ Load image from a .cimg[z] file.

            Args:
                filename (str): Filename of image.
                axis: Appending axis, if file contains multiple images.
                      Can be { 'x' | 'y' | 'z' | 'c' }.
                align: Appending alignment.
            Raises:
                RuntimeError: If file does not exist or axis is invalid.
        """
        if axis not in "xyzc":
            raise RuntimeError("Invalid axis.")
        if os.path.isfile(filename):
            return self._cimg.load_cimg(filename, axis, align)
        else:
            raise RuntimeError("File '{}' does not exist".format(filename))

    def save(self, filename, number=-1, digits=6):
        """ Save image as a file.

            The used file format is defined by the file extension
            in the filename.

            Args:
                filename (str): Filneame of image.
                number: When positive, represents an index added to the filename.
                        Otherwise, no number is added.
                digits: Number of digits used for adding the number to the filename.
        """
        self._cimg.save(filename, number, digits)

    def save_bmp(self, filename):
        """ Save image as a BMP file.

            Args:
                filename (str): Filename of image.
        """
        self._cimg.save_bmp(filename)

    def save_jpeg(self, filename, quality=100):
        """ Save image as a JPEG file.

            Args:
                filename (str): Filename of image.
                quality: Image quality (in %).
        """
        self._cimg.save_jpeg(filename, quality)

    def save_png(self, filename, bytes_per_pixel=0):
        """ Save image as a PNG file.

            Args:
                filename (str): Filename of image.
                bytes_per_pixel: Force the number of bytes per pixels for
                                 saving, when possible.
        """
        self._cimg.save_png(filename, bytes_per_pixel)

    def save_tiff(self, filename, compression_type=C_NONE, voxel_size=0,
                  description="", use_bigtiff=True):
        """ Save image as a TIFF file.

            Args:
                filename (str): Filename of image.
                compression_type:    Type of data compression.
                    Can be: C_NONE, C_LZW, C_JPEG.
                voxel_size: Voxel size, to be stored in the filename.
                description: Description, to be stored in the filename.
                use_bigtiff: Allow to save big tiff files (>4Gb).
        """
        self._cimg.save_tiff(filename, compression_type, voxel_size,
                             description, use_bigtiff)

    def save_cimg(self, filename, is_compressed=False):
        """ Save image as a .cimg file.

            Args:
                filename (str): Filename of image.
                is_compressed: Tells if the file contains compressed image data.
        """
        self._cimg.save_cimg(filename, is_compressed)

    def load_cimg_float16(self, filename):
        """ Load image from a .cimg file with half precision
            pixel values.

            Args:
                filename (str): Filename of image.
            Raises:
                RuntimeError: If file does not exist.
        """
        if os.path.isfile(filename):
            self._cimg.load_cimg_float16(filename)
        else:
            raise RuntimeError("File '{}' does not exist".format(filename))

    def save_cimg_float16(self, filename):
        """ Save image to a .cimg file with half precision pixel values.

            Args:
                filename (str): Filename of image.
        """
        self._cimg.save_cimg_float16(filename)

    ###########################################################################
    # Instance characteristics
    ###########################################################################
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

    def asarray(self):
        """ Convert image to a numpy array.

            Note that the data of the array is shared
            with the image instance. Changes to the array
            therefore propagate to the image.

        """
        return self._cimg.asarray()

    def fromarray(self, arr):
        """ Convert numpy array to cimg.

            Args:
                arr (ndarray) : numpy array

            Raises:
                RuntimeError: if array has more than 4 dimensions
        """
        self._cimg.fromarray(arr)
        return self

    def linear_atX(self, fx, y=0, z=0, c=0):
        """ Return pixel value, using linear interpolation
            and Neumann boundary conditions for the X-coordinate.
            Warning: No bounds check for y, z, and c. They must be
            within image bounds.

            Args:
                fx (float): X-coordinate of the pixel value.
                y (int):    Y-coordinate of the pixel value.
                z (int):    Z-coordinate of the pixel value.
                c (int):    C-coordinate of the pixel value.

            Returns: a linearly-interpolated pixel value of the image
                     instance located at (fx,y,z,c), or the value of the
                     nearest pixel location in the image instance in case
                     of out-of-bounds access along the X-axis.
        """
        return self._cimg.linear_atX(fx, y, z, c)

    def linear_atXY(self, fx, fy, z=0, c=0):
        """ Return pixel value, using linear interpolation
            and Neumann boundary conditions for the X and Y-coordinates.

            Args:
                fx (float): X-coordinate of the pixel value.
                fy (float): Y-coordinate of the pixel value.
                z (int):    Z-coordinate of the pixel value.
                c (int):    C-coordinate of the pixel value.

            Returns: a linearly-interpolated pixel value of the image
                     instance located at (fx,fy,z,c).
        """
        return self._cimg.linear_atXY(fx, fy, z, c)

    def linear_atXYZ(self, fx, fy, fz, c=0):
        """ Return pixel value, using linear interpolation
            and Neumann boundary conditions for the X,Y and Z-coordinates.

            Args:
                fx (float): X-coordinate of the pixel value.
                fy (float): Y-coordinate of the pixel value.
                fz (float): Z-coordinate of the pixel value.
                c (int):    C-coordinate of the pixel value.

            Returns: a linearly-interpolated pixel value of the image
                     instance located at (fx,fy,fz,c).
        """

        return self._cimg.linear_atXYZ(fx, fy, fz, c)

    def linear_atXYZC(self, fx, fy, fz, fc):
        """ Return pixel value, using linear interpolation
            and Neumann boundary conditions for the X,Y,Z and C-coordinates.

            Args:
                fx (float): X-coordinate of the pixel value.
                fy (float): Y-coordinate of the pixel value.
                fz (float): Z-coordinate of the pixel value.
                fc (float): C-coordinate of the pixel value.

            Returns: a linearly-interpolated pixel value of the image
                     instance located at (fx,fy,fz,fc).
        """
        return self._cimg.linear_atXYZC(fx, fy, fz, fc)

    ###########################################################################
    # Mathmatical functions
    ###########################################################################
    def sqr(self):
        """ Compute the square value of each pixel value. """
        self._cimg.sqr()
        return self

    def sqrt(self):
        """ Compute the square root of each pixel value. """
        self._cimg.sqrt()
        return self

    def exp(self):
        """ Compute the exponential of each pixel value. """
        self._cimg.exp()
        return self

    def log(self):
        """ Compute the logarithm of each pixel value. """
        self._cimg.log()
        return self

    def log2(self):
        """ Compute base-2 logarithm of each pixel value. """
        self._cimg.log2()
        return self

    def log10(self):
        """ Compute the base-10 logarithm of each pixel value. """
        self._cimg.log10()
        return self

    def abs(self):
        """ Compute the absolute value of each pixel value. """
        self._cimg.abs()
        return self

    def sign(self):
        """ Compute the sign of each pixel value. """
        self._cimg.sign()
        return self

    def cos(self):
        """ Compute the cosine of each pixel value. """
        self._cimg.cos()
        return self

    def sin(self):
        """ Compute the sine of each pixel value. """
        self._cimg.sin()
        return self

    def sinc(self):
        """ Compute the sinc of each pixel value. """
        self._cimg.sinc()
        return self

    def tan(self):
        """ Compute the tangent of each pixel value. """
        self._cimg.tan()
        return self

    def sinh(self):
        """ Compute the hyperbolic sine of each pixel value. """
        self._cimg.sinh()
        return self

    def tanh(self):
        """ Compute the hyperbolic tangent of each pixel value. """
        self._cimg.tanh()
        return self

    def acos(self):
        """ Compute the arccosine of each pixel value. """
        self._cimg.acos()
        return self

    def asin(self):
        """ Compute the arcsine of each pixel value. """
        self._cimg.asin()
        return self

    def atan(self):
        """ Compute the arctangent of each pixel value. """
        self._cimg.atan()
        return self

    def atan2(self, img):
        """ Compute the arctangent2 of each pixel value.

            Args:
                img (CImg): Image whose pixel values specify the second
                            argument of the atan2() function.

        """
        self._cimg.atan2(img._cimg)
        return self

    def mul(self, img):
        """ In-place pointwise multiplication.

            Compute the pointwise multiplication between
            the image instance and the specified input image img.

            Args:
                img (CImg): Input image, second operand of the multiplication.
        """
        self._cimg.mul(img._cimg)
        return self

    def div(self, img):
        """ In-place pointwise division.

            Compute the pointwise division between
            the image instance and the specified input image img.

            Args:
                img (CImg): Input image, second operand of the division.
        """
        self._cimg.div(img._cimg)
        return self

    def pow(self, p):
        """ Raise each pixel value to the specified power.

            Args:
                p (int): Exponent value.
        """
        self._cimg.pow(p)

    def min_max(self):
        """ Returns: tuple with minimum and maximum pixel value. """
        return self._cimg.min_max()

    def max_min(self):
        """ Returns: tuple with maximum and minimum pixel value. """
        return self._cimg.max_min()

    def kth_smallest(self, k):
        """ Returns the kth smallest pixel value.

            Args:
                k (int): Rank of the search smallest element.

            Returns: kth smallest pixel value.
        """
        return self._cimg.kth_smallest(k)

    def variance(self, variance_method=BEST_UNBIASED):
        """ Returns the variance of the pixel values.

            Args:
                variance_method (int): Method used to estimate the variance.
                                       Can be: SECOND_MOMENT
                                               BEST_UNBIASED
                                               LEAST_MEDIAN_SQ
                                               LEAST_TRIMMED_SQ

            Returns: Variance of pixel values.
        """
        return self._cimg.variance(variance_method)

    def variance_mean(self, variance_method=BEST_UNBIASED):
        """ Returns variance and average of pixel values.

            Args:
                variance_method (int): Method used to estimate the variance.

            Returns: Tuple with variance and mean of pixel values.
        """
        return self._cimg.variance_mean(variance_method)

    def variance_noise(self, variance_method=LEAST_MEDIAN_SQ):
        """ Returns estimated variance of noise.

            Args:
                variance_method (int): Method used to estimate the variance.

            Returns: Estimated variance of noise.
        """
        return self._cimg.variance_noise(variance_method)

    def mse(self, img):
        """ Compute the MSE (Mean-Squared Error) between two images.

            Args:
                img (CImg): Image used as the second argument of the MSE operator.

            Returns: mean squared error between self and img.
        """
        return self._cimg.mse(img._cimg)

    def psnr(self, img, max_value=255):
        """ Compute the PSNR (Peak Signal-to-Noise Ratio) between two images.

            Args:
                img (CImg): Image used as the second argument of the PSNR operator.
                max_value (float): Maximum theoretical value of the signal.

            Returns: peak signal-to-noise ratio between self and img.
        """
        return self._cimg.psnr(img._cimg, max_value)

    ###########################################################################
    # Vector / Matrix Operations
    ###########################################################################
    def magnitude(self, magnitude_type):
        """ Compute norm of the image, viewed as a matrix.

            Args:
                magnitude_type (int): Norm type. Can be:
                    LINF_NORM
                    L0_NORM
                    L1_NORM
                    L2_NORM

            Returns: Norm of image.
        """
        return self._cimg.magnitude(magnitude_type)

    def dot(self, img):
        """ Compute the dot product between instance and argument, viewed as matrices"

            Args:
                img (CImg): Image used as a second argument of the dot product.

            Returns: Dot product between self and img.
        """
        return self._cimg.dot(img._cimg)

    ###########################################################################
    # Value Manipulation
    ###########################################################################
    def fill(self, val):
        """ Fill all pixel values with specified value.

            Args:
                val (float): Fill value.
        """
        self._cimg.fill(val)
        return self

    def invert_endianness(self):
        """ Invert endianness of all pixel values. """
        self._cimg.invert_endianness()
        return self

    def rand(self, val_min, val_max):
        """ Fill image with random values in specified range.

            Args:
                val_min (float): Minimal authorized random value.
                val_max (float): Maximal authorized random value.
        """
        self._cimg.rand(val_min, val_max)
        return self

    def round(self, y=1, rounding_type=R_NEAREST):
        """ Round pixel values.

            Args:
                y (int): Rounding precision.
                rounding_type (int): Rounding type. Can be:
                    R_BACKWARD, R_NEAREST, R_FORWARD
        """
        self._cimg.round(y, rounding_type)
        return self

    def noise(self, sigma, noise_type=GAUSSIAN):
        """ Add random noise to pixel values.

            Args:
                sigma (float): Amplitude of the random additive noise.
                               If sigma<0, it stands for a percentage of
                               the global value range.

                noise_type (int): Type of additive noise (can be
                                  GAUSSIAN,
                                  UNIFORM,
                                  SALT_AND_PEPPER,
                                  POISSON or
                                  RICIAN).

        """
        self._cimg.noise(sigma, noise_type)
        return self

    def normalize(self, min_value, max_value):
        """ Linearly normalize pixel values.

            Args:
                min_value (float): Minimum desired value of resulting image.
                max_value (float): Maximum desired value of resulting image.
        """
        self._cimg.normalize(min_value, max_value)
        return self

    def normalize_l2(self):
        """ Normalize multi-valued pixels of the image instance,
            with respect to their L2-norm.
        """
        self._cimg.normalize_l2()
        return self

    def norm(self, norm_type=L2_NORM):
        """ Compute Lp-norm of each multi-valued pixel of the
            image instance.

            Args:
                norm_type (int): Type of computed vector norm. Can be:
                LINF_NORM, L0_NORM, L1_NORM, L2_NORM, or value p>2
        """
        self._cimg.norm(norm_type)
        return self

    def cut(self, min_value, max_value):
        """ Cut pixel values in specified range.

            Args:
                min_value (float): Minimum desired value of resulting image.
                max_value (float): Maximum desired value of resulting image.
        """
        self._cimg.cut(min_value, max_value)
        return self

    def quantize(self, nb_levels, keep_range=True):
        """ Uniformly quantize pixel values.

            Args:
                nb_levels (int): Number of quantization levels.
                keep_range (bool): Tells if resulting values keep the same
                                   range as the original ones.

        """
        self._cimg.quantize(nb_levels, keep_range)
        return self

    def threshold(self, value, soft_threshold=False, strict_threshold=False):
        """ Threshold pixel values.

            Args:
                value (float): Threshold value.
                soft_threshold (bool): Tells if soft thresholding must be
                                        applied (instead of hard one).
                strict_threshold (bool): Tells if threshold value is strict.
        """
        self._cimg.threshold(value, soft_threshold, strict_threshold)
        return self

    def histogram(self, nb_levels, min_value, max_value):
        """ Compute the histogram of pixel values.

            Args:
                nb_levels (int): Number of desired histogram levels.
                min_value (float): Minimum pixel value considered for the
                                   histogram computation. All pixel values
                                   lower than min_value will not be counted.
                max_value (float): Maximum pixel value considered for the
                                   histogram computation. All pixel values
                                   higher than max_value will not be counted.
        """
        self._cimg.histogram(nb_levels, min_value, max_value)
        return self

    def equalize(self, nb_levels, min_value, max_value):
        """ Equalize histogram of pixel values.

            Args:
                nb_levels (int): Number of desired histogram levels.
                min_value (float): Minimum pixel value considered for the
                                   histogram computation. All pixel values
                                   lower than min_value will not be counted.
                max_value (float): Maximum pixel value considered for the
                                   histogram computation. All pixel values
                                   higher than max_value will not be counted.
        """
        self._cimg.equalize(nb_levels, min_value, max_value)
        return self

    def index(self, colormap, dithering=1, map_indexes=False):
        """ Index multi-valued pixels regarding to a specified colormap.

            Args:
                colormap (CImg): Multi-valued colormap used as the basis for
                                 multi-valued pixel indexing.
                dithering (int): Level of dithering (0=disable, 1=standard level).
                map_indexes (bool): Tell if the values of the resulting image are
                                    the colormap indices or the colormap vectors.
        """
        self._cimg.index(colormap._cimg, dithering, map_indexes)
        return self

    def map(self, colormap, boundary_conditions=DIRICHLET):
        """ Map predefined colormap on the scalar (indexed) image instance.

            Args:
                colormap (CImg): Multi-valued colormap used for
                                 mapping the indexes.
                boundary_conditions (int): The border condition type. Can be:
                    DIRICHLET, NEUMANN, PERIODIC, or MIRROR.

        """
        self._cimg.map(colormap._cimg, boundary_conditions)
        return self

    def label(self, is_high_connectivity=False, tolerance=0.0):
        """ Label connected components.

            Args:
                is_high_connectivity (bool): Choose between 4(false)
                - or 8(true)-connectivity in 2d case, and between 6(false)
                - or 26(true)-connectivity in 3d case.
                tolerance (float): Tolerance used to determine if two neighboring
                                   pixels belong to the same region.
        """
        self._cimg.label(is_high_connectivity, tolerance)
        return self

    ###########################################################################
    # Geometric / Spatial Manipulation
    ###########################################################################
    def resize(self, size_x, size_y=-100, size_z=-100, size_c=-100,
               interpolation_type=NEAREST, boundary_conditions=DIRICHLET,
               centering_x=0,
               centering_y=0,
               centering_z=0,
               centering_c=0):
        """ Resize image to new dimensions.

            Args:
                size_x (int): Number of columns (new size along the X-axis).
                size_y (int): Number of rows (new size along the Y-axis).
                size_z (int): Number of slices (new size along the Z-axis).
                size_c (int): Number of vector-channels (new size along the C-axis).
                interpolation_type (int):  Method of interpolation:
                    NONE_RAW = no interpolation: raw memory resizing.
                    NONE = no interpolation: additional space is filled according to boundary_conditions.
                    NEAREST = nearest-neighbor interpolation.
                    MOVING_AVERAGE = moving average interpolation.
                    LINEAR = linear interpolation.
                    GRID = grid interpolation.
                    CUBIC = cubic interpolation.
                    LANCZOS = lanczos interpolation.
                boundary_conditions (int): Type of boundary conditions used if
                                     necessary. Can be: DIRICHLET | NEUMANN | PERIODIC | MIRROR
                centering_x (int): Set centering type (only if interpolation_type=NONE).
                centering_y (int): Set centering type (only if interpolation_type=NONE).
                centering_z (int): Set centering type (only if interpolation_type=NONE).
                centering_c (int): Set centering type (only if interpolation_type=NONE).

        """
        self._cimg.resize(size_x, size_y, size_z, size_c,
                          interpolation_type, boundary_conditions,
                          centering_x,
                          centering_y,
                          centering_z,
                          centering_c)
        return self


    def resize_halfXY(self):
        """ Resize image to half-size along XY axes, using an optimized filter. """
        self._cimg.resize_halfXY()
        return self

    def resize_doubleXY(self):
        """ Resize image to double-size, using the Scale2X algorithm. """
        self._cimg.resize_doubleXY()
        return self

    def resize_tripleXY(self):
        """ Resize image to triple-size, using the Scale3X algorithm. """
        self._cimg.resize_tripleXY()
        return self

    def mirror(self, axes):
        """ Mirror image content along specified axes.

            Args:
                axes (str): Mirror axes as string, e.g. "x" or "xyz"
        """
        self._cimg.mirror(axes)
        return self

    def shift(self, delta_x, delta_y=0, delta_z=0, delta_c=0, boundary_conditions=DIRICHLET):
        """ Shift image content.

            Args:
                delta_x (int): Amount of displacement along the X-axis.
                delta_y (int): Amount of displacement along the Y-axis.
                delta_z (int): Amount of displacement along the Z-axis.
                delta_c (int): Amount of displacement along the C-axis.
                boundary_conditions (int): Border condition.
        """
        self._cimg.shift(delta_x, delta_y, delta_z, delta_c, boundary_conditions)
        return self

    def permute_axes(self, order):
        """ Permute axes order.

            Args:
                order (str): Axes permutations as string of length 4.

            Raises: RuntimeError if order is invalid.
        """
        if (not len(order) == 4) or (not all(o in "xyzc" for o in order)):
            raise RuntimeError("Invalid axes order.")
        self._cimg.permute_axes(order)
        return self

    def unroll(self, axis):
        """ Unroll pixel values along specified axis.

            Args:
                axis (str): 'x', 'y', 'z', or 'c'.

            Raises: RuntimeError if axis is invalid.
        """
        if not axis in "xyzc":
            raise RuntimeError("Invalid axis.")
        self._cimg.unroll(axis)
        return self

    def rotate(self, angle, interpolation=1, boundary_conditions=DIRICHLET):
        """ Rotate image with arbitrary angle.

            Args:
                angle (float): Rotation angle, in degrees.
                interpolation (int): Type of interpolation.
                               Can be { 0=nearest | 1=linear | 2=cubic | 3=mirror }.
                boundary_conditions (int): Boundary conditions.
        """
        self._cimg.rotate(angle, interpolation, boundary_conditions)
        return self

    def crop(self, x0, y0, z0, c0, x1, y1, z1, c1, boundary_conditions=DIRICHLET):
        """ Crop image region.

            Args:
               x0 (int): X-coordinate of the upper-left crop rectangle corner.
               y0 (int): Y-coordinate of the upper-left crop rectangle corner.
               z0 (int): Z-coordinate of the upper-left crop rectangle corner.
               c0 (int): C-coordinate of the upper-left crop rectangle corner.
               x1 (int): X-coordinate of the lower-right crop rectangle corner.
               y1 (int): Y-coordinate of the lower-right crop rectangle corner.
               z1 (int): Z-coordinate of the lower-right crop rectangle corner.
               c1 (int): C-coordinate of the lower-right crop rectangle corner.
               boundary_conditions (int): boundary conditions.
        """
        self._cimg.crop(x0, y0, z0, c0, x1, y1, z1, c1, boundary_conditions)
        return self

    def autocrop(self, color=0, axes="xyz"):
        """ Autocrop image region, regarding the specified background color.

            Args:
                color (int/list): Color used for the crop. If 0, color is guessed.
                axes (str): Axes used for crop.

        """
        if color != 0:
            color = self._check_color(color)
        self._cimg.autocrop(color, axes)
        return self

    def append(self, img, axis='x', align=0):
        """ Append two images along specified axis.

            Args:
                img (CImg): Image to append with instance image.
                axis (str): Appending axis. Can be { 'x' | 'y' | 'z' | 'c' }.
                align (float): Append alignment in [0,1]. 
        """
        self._cimg.append(img._cimg, axis, align)
        return self


    ############################################################################
    # Filtering / Transforms
    ############################################################################
    def correlate(self, kernel, boundary_conditions=True, is_normalized=False):
        """ Correlate image by a kernel.

            Args:
                kernel (CImg): the correlation kernel.
                boundary_conditions (bool): boundary conditions can be
                                            (False=dirichlet, True=neumann)
                is_normalized (bool): enable local normalization.
        """
        self._cimg.correlate(kernel._cimg, boundary_conditions, is_normalized)
        return self

    def convolve(self, kernel, boundary_conditions=True, is_normalized=False):
        """ Convolve image by a kernel.

            Args:
                kernel (CImg): the correlation kernel.
                boundary_conditions (bool): boundary conditions can be
                                    (False=dirichlet, True=neumann)
                is_normalized (bool): enable local normalization.
        """
        self._cimg.convolve(kernel._cimg, boundary_conditions, is_normalized)
        return self

    def cumulate(self, axes):
        """ Cumulate image values, optionally along specified axes.

            Args:
                axes (str): Cumulation axes as string, e.g. "x" or "xyz".
        """
        self._cimg.cumulate(axes)
        return self

    def erode(self, kernel, boundary_conditions=True, is_real=False):
        """ Erode image by a structuring element.

            Args:
                kernel (CImg):	Structuring element.
                boundary_conditions (bool): Boundary conditions.
                is_real (bool): Do the erosion in real (a.k.a 'non-flat') 
                                mode (true) rather than binary mode (false).
        """
        self._cimg.erode(kernel._cimg, boundary_conditions, is_real)
        return self

    def dilate(self, kernel, boundary_conditions=True, is_real=False):
        """ Dilate image by a structuring element.

            Args:
                kernel (CImg):	Structuring element.
                boundary_conditions (bool): Boundary conditions.
                is_real (bool): Do the erosion in real (a.k.a 'non-flat') 
                                mode (true) rather than binary mode (false).
        """
        self._cimg.dilate(kernel._cimg, boundary_conditions, is_real)
        return self

    def watershed(self, priority, is_high_connectivity=False):
        """ Compute watershed transform.

            Args:
                priority (CImg): Priority map.
                is_high_connectivity (bool): Choose between 4(false)- or
                                      8(true)-connectivity in 2d case,
                                      and between 6(false)- or
                                      26(true)-connectivity in 3d case.
        """
        self._cimg.watershed(priority._cimg, is_high_connectivity)
        return self

    def deriche(self, sigma, order=SMOOTH_FILTER, axis="x", boundary_conditions=True):
        """ Apply recursive Deriche filter.

            Args:
                sigma (float): Standard deviation of the filter.
                order (int): Order of the filter. Can be:
                       SMOOTH_FILTER, FIRST_DERIV, or SECOND_DERIV.
                axis (str): Axis along which the filter is computed. Can be:
                      { 'x' | 'y' | 'z' | 'c' }.
                boundary_conditions (bool): Boundary conditions. Can be:
                      { False=dirichlet | True=neumann }.
        """
        self._cimg.deriche(sigma, order, axis, boundary_conditions)
        return self

    def vanvliet(self, sigma, order, axis="x", boundary_conditions=True):
        """ Van Vliet recursive Gaussian filter.

            Args:
                sigma (float): Standard deviation of the Gaussian filter.
                order (int): Order of the filter. Can be:
                       SMOOTH_FILTER, FIRST_DERIV, SECOND_DERIV, or THIRD_DERIV.
                axis (str): Axis along which the filter is computed. Can be:
                      { 'x' | 'y' | 'z' | 'c' }.
                boundary_conditions (bool): Boundary conditions. Can be:
                      { False=dirichlet | True=neumann }.
        """
        self._cimg.vanvliet(sigma, order, axis, boundary_conditions)
        return self

    def blur(self, sigma, boundary_conditions=True, is_gaussian=False):
        """ Blur image isotropically.

            Note: The blur is computed as a 0-order Deriche filter.
            This is not a gaussian blur. This is a recursive algorithm,
            not depending on the values of the standard deviations.

            Args:
                sigma (float): Standard deviation of the blur.
                boundary_conditions (bool): Boundary conditions. Can be
                                     { False=dirichlet | True=neumann }.
                is_gaussian (bool): Tells if the blur uses a gaussian (True)
                             or quasi-gaussian (False) kernel.
        """
        self._cimg.blur(sigma, boundary_conditions, is_gaussian)
        return self

    def boxfilter(self, boxsize, order, axis="x", boundary_conditions=True, nb_iter=1):
        """ Apply box filter to image.

            Args:
                boxsize (float): Size of the box window (can be subpixel)
                order (int):   the order of the filter 0,1 or 2.
                axis (str):    Axis along which the filter is computed.
                         Can be { 'x' | 'y' | 'z' | 'c' }.
                boundary_conditions (bool): Boundary conditions. Can be
                                     { False=dirichlet | True=neumann }.
                nb_iter (int): Number of filter iterations.
        """
        self._cimg.boxfilter(boxsize, order, axis, boundary_conditions, nb_iter)
        return self

    def blur_box(self, boxsize, boundary_conditions=True):
        """ Blur image with a box filter.

            Args:
                boxsize (int): Size of the box window (can be subpixel).
                boundary_conditions (bool): Boundary conditions. Can be
                                     { False=dirichlet | True=neumann }.
        """
        self._cimg.blur_box(boxsize, boundary_conditions)
        return self

    def blur_median(self, n, threshold=0):
        """ Blur image with the median filter.

            Args:
                n (int): Size of the median filter.
                threshold (float): Threshold used to discard pixels too far
                           from the current pixel value in the median computation.
        """
        self._cimg.blur_median(n, threshold)
        return self

    def sharpen(self, amplitude, sharpen_type=False, edge=1, alpha=0, sigma=0):
        """ Sharpen image.

            Args:
                amplitude (float): Sharpening amplitude
                sharpen_type (bool): Select sharpening method. Can be
                              { False=inverse diffusion | True=shock filters }.
                edge (int): Edge threshold (shock filters only).
                alpha (float): Gradient smoothness (shock filters only).
                sigma (float): Tensor smoothness (shock filters only).

        """
        self._cimg.sharpen(amplitude, sharpen_type, edge, alpha, sigma)
        return self

    ###########################################################################
    # Drawing functions
    ###########################################################################

    def _check_color(self, color):
        """ Raises a RuntimeError if color does not have the correct
            number of entries."""
        if isinstance(color, numbers.Number):
            color = [color]
        n = self._cimg.spectrum()
        if hasattr(color, '__len__') and not len(color) == n:
            raise RuntimeError('Color should have {} entries'.format(n))
        return color

    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color, opacity=1):
        """ Draw a filled 2d triangle.

            Args:
                x0 (int): X-coordinate of the first vertex.
                y0 (int): Y-coordinate of the first vertex.
                x1 (int): X-coordinate of the second vertex.
                y1 (int): Y-coordinate of the second vertex.
                x2 (int): X-coordinate of the third vertex.
                y2 (int): Y-coordinate of the third vertex.
                color (list): List of color value with spectrum() entries.
                opacity (float): Drawing opacity.

            Raises:
                RuntimeError: If list of color values does not have spectrum() entries.
        """
        color = self._check_color(color)
        self._cimg.draw_triangle(x0, y0, x1, y1, x2, y2, color, opacity)
        return self

    def draw_rectangle(self, x0, y0, x1, y1, color, opacity=1):
        """ Draw a filled 2d rectangle.

            Args:
                x0 (int): X-coordinate of the upper-left rectangle corner.
                y0 (int): Y-coordinate of the upper-left rectangle corner.
                x1 (int): X-coordinate of the lower-right rectangle corner.
                y1 (int): Y-coordinate of the lower-right rectangle corner.
                color (list): List of color value with spectrum() entries.
                opacity (float): Drawing opacity.

            Raises:
                RuntimeError: If list of color values does not have spectrum() entries.
        """
        color = self._check_color(color)
        self._cimg.draw_rectangle(x0, y0, x1, y1, color, opacity)
        return self

    # ...
    def draw_polygon(self, points, color, opacity=1):
        """ Draw filled 2d polygon.

        Args:
            points (ndarray): (n x 2) numpy array of polygon vertices
            color (list): List of color value with spectrum() entries.
            opacity (float): Drawing opacity.

        Raises:
            RuntimeError: If list of color values does not have spectrum() entries.
        """
        color = self._check_color(color)
        self._cimg.draw_polygon( points.T, color, opacity)
        return self

    def draw_circle(self, x0, y0, radius, color, opacity=1):
        """ Draw a filled 2d circle.

        Args:
            x0 (int):  X-coordinate of the circle center.
            y0 (int):  Y-coordinate of the circle center.
            radius (float):  Circle radius.
            color (list): List of color value with spectrum() entries.
            opacity (float): Drawing opacity.

        Raises:
            RuntimeError: If list of color values does not have spectrum() entries.
        """
        color = self._check_color(color)
        self._cimg.draw_circle(x0, y0, radius, color, opacity)
        return self

    def draw_text(self, x0, y0, text, foreground_color, 
                  background_color, opacity=1, font_height=13):
        """ Draw a text string.

            Args:
                x0 (int): X-coordinate of the text in the image instance.
                y0 (int): Y-coordinate of the text in the image instance.
                text (str): The text.
                foreground_color (list): List of color value with spectrum() entries.
                background_color (list): List of color value with spectrum() entries.
                opacity (float): Drawing opacity.
                font_height (int): Height of the text font 
                    (exact match for 13,23,53,103, interpolated otherwise). 
        """
        fc = self._check_color(foreground_color)
        bc = self._check_color(background_color)
        self._cimg.draw_text(x0, y0, text, fc, bc, opacity, font_height)
        return self

    def display(self, title=""):
        """ Display image into a CImgDisplay window.

            Args:
                title (str): Title of window.
        
        """
        self._cimg.display(title)

    def display_graph(self, plot_type=SEGMENTS, vertex_type=1,
                      labelx="", xmin=0, xmax=0,
                      labely="", ymin=0, ymax=0):
        """ Display 1d graph in an interactive window. 
        
            Args:
                plot_type (int): Plot type. 
                                 Can be POINTS | SEGMENTS | SPLINES | BARS.
                vertex_type (int): Vertex type.
                labelx (str): Title for the horizontal axis.
                xmin (int): Minimum value along the X-axis.
                xmax (int): Maximum value along the X-axis.
                labely (str): Title for the vertical axis.
                ymin (int): Minimum value along the X-axis.
                ymax (int): Maximum value along the X-axis. 
        """
        self._cimg.display_graph(plot_type, vertex_type, 
                                 labelx, xmin, xmax,
                                 labely, ymin, ymax)
