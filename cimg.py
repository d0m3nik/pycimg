import numpy as np
import os.path
from pycimg import CImg_int8, CImg_int16, CImg_int32, CImg_uint8, CImg_uint16, CImg_uint32, CImg_float32, CImg_float64 

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

                4. Create image of size 100x200 with
                im = CImg((100, 200), dtype=float32)

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
            elif isinstance(args[0], tuple):
                self.resize(*args[0], interpolation_type=NONE_RAW)
            elif isinstance(args[0], int):
                self.resize(args[0], interpolation_type=NONE_RAW)
            else:
                raise RuntimeError("Type of first argument not supported")


    def load(self, filename):
        """ Load image from a file.
            
            Args: 
                filename: Filename of image.
            Raises:
                RuntimeError: If file does not exist.
        """
        if os.path.isfile(filename): 
            self._cimg.load(filename)
        else:
            raise RuntimeError("File '{}' does not exist".format(filename))

#    def load_cimg(self, filename, axis='z', align=0):
#        self._cimg.load_cimg(filename, axis, align)

    def load_cimg_float16(self, filename):
        """ Load image from a .cimg file with half precision
            pixel values.

             Args: 
                filename: Filename of image.
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
                filename: Filename of image.
        """
        self._cimg.save_cimg_float16(filename)

    def save(self, filename):
        """ Save image as a file.

            The used file format is defined by the file extension 
            in the filename.

            Args:
                filename: Filneame of image.
        """
        self._cimg.save(filename)

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
        """ Convert image to a numpy array. """
        return self._cimg.asarray()

    def fromarray(self, arr):
        """ Convert numpy array to cimg. 

            Args: 
                arr : numpy array

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
                fx:  X-coordinate of the pixel value (float-valued).
                y:   Y-coordinate of the pixel value.
                z:   Z-coordinate of the pixel value.
                c:   C-coordinate of the pixel value.

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
                fx:  X-coordinate of the pixel value (float-valued).
                fy:  Y-coordinate of the pixel value (float-valued).
                z:   Z-coordinate of the pixel value.
                c:   C-coordinate of the pixel value.

            Returns: a linearly-interpolated pixel value of the image 
                     instance located at (fx,fy,z,c).
        """ 
        return self._cimg.linear_atXY(fx, fy, z, c)

    def linear_atXYZ(self, fx, fy, fz, c=0):
        """ Return pixel value, using linear interpolation 
            and Neumann boundary conditions for the X,Y and Z-coordinates.

            Args:
                fx:  X-coordinate of the pixel value (float-valued).
                fy:  Y-coordinate of the pixel value (float-valued).
                fz:  Z-coordinate of the pixel value (float-valued).
                c:   C-coordinate of the pixel value.

            Returns: a linearly-interpolated pixel value of the image 
                     instance located at (fx,fy,fz,c).
        """ 

        return self._cimg.linear_atXYZ(fx, fy, fz, c)

    def linear_atXYZC(self, fx, fy, fz, fc):
        """ Return pixel value, using linear interpolation 
            and Neumann boundary conditions for the X,Y,Z and C-coordinates.

            Args:
                fx:  X-coordinate of the pixel value (float-valued).
                fy:  Y-coordinate of the pixel value (float-valued).
                fz:  Z-coordinate of the pixel value (float-valued).
                fc:  C-coordinate of the pixel value (float-valued).

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
                img: Image whose pixel values specify the second 
                     argument of the atan2() function. 
        
        """
        self._cimg.atan2(img)
        return self

    def mul(self, img):
        """ In-place pointwise multiplication.

            Compute the pointwise multiplication between 
            the image instance and the specified input image img. 

            Args: 
                img: Input image, second operand of the multiplication.
        """
        self._cimg.mul(img)
        return self

    def div(self, img):
        """ In-place pointwise division.

            Compute the pointwise division between 
            the image instance and the specified input image img. 

            Args: 
                img: Input image, second operand of the division.
        """
        self._cimg.div(img)
        return self

    def pow(self, p):
        """ Raise each pixel value to the specified power.

            Args:
                p: Exponent value.
        """
        self._cimg.pow(p)


    # ...
    def noise(self, sigma, noise_type):
        """ Add random noise to pixel values. 

            Args:
                sigma: Amplitude of the random additive noise. 
                       If sigma<0, it stands for a percentage of 
                       the global value range.

                noise_type: Type of additive noise (can be 
                            0=gaussian, 
                            1=uniform, 
                            2=Salt and Pepper, 
                            3=Poisson or 
                            4=Rician). 
        
        """
        self._cimg.noise(sigma, noise_type)
        return self

    def normalize(self, min_value, max_value):
        """ Linearly normalize pixel values.

            Args:
                min_value: Minimum desired value of resulting image.
                max_value: Maximum desired value of resulting image.
        """
        self._cimg.normalize(min_value, max_value)
        return self

    def normalize_l2(self):
        """ Normalize multi-valued pixels of the image instance, 
            with respect to their L2-norm. 
        """
        self._cimg.normalize_l2()
        return self

    def norm(self, norm_type):
        """ Compute Lp-norm of each multi-valued pixel of the 
            image instance.

            Args:
                norm_type: Type of computed vector norm 
                            (can be -1=Linf, or greater or equal than 0). 
        """
        self._cimg.norm(norm_type)
        return self

    def cut(self, min_value, max_value):
        """ Cut pixel values in specified range. 

            Args:
                min_value: Minimum desired value of resulting image.
                max_value: Maximum desired value of resulting image.
        """
        self._cimg.cut(min_value, max_value)
        return self

    def quantize(self, nb_levels, keep_range=True):
        """ Uniformly quantize pixel values.

            Args:
                nb_levels: Number of quantization levels.
                keep_range: Tells if resulting values keep the same 
                            range as the original ones. 

        """
        self._cimg.quantize(nb_levels, keep_range)
        return self

    def threshold(self, value, soft_threshold=False, strict_threshold=False):
        """ Threshold pixel values.
            
            Args:
                value: Threshold value.
                soft_threshold: Tells if soft thresholding must be 
                                applied (instead of hard one). 
                strict_threshold: Tells if threshold value is strict.
        """
        self._cimg.threshold(value, soft_threshold, strict_threshold)
        return self

    def histogram(self, nb_levels, min_value, max_value):
        """ Compute the histogram of pixel values.

            Args:
                nb_levels: Number of desired histogram levels.
                min_value: Minimum pixel value considered for the 
                           histogram computation. All pixel values 
                           lower than min_value will not be counted. 
                max_value: Maximum pixel value considered for the 
                           histogram computation. All pixel values 
                           higher than max_value will not be counted. 
        """
        self._cimg.histogram(nb_levels, min_value, max_value)
        return self

    def equalize(self, nb_levels, min_value, max_value):
        """ Equalize histogram of pixel values.

            Args:
                nb_levels: Number of desired histogram levels.
                min_value: Minimum pixel value considered for the 
                           histogram computation. All pixel values 
                           lower than min_value will not be counted. 
                max_value: Maximum pixel value considered for the 
                           histogram computation. All pixel values 
                           higher than max_value will not be counted. 
        """
        self._cimg.equalize(nb_levels, min_value, max_value)
        return self

    # TODO: index, map

    def label(self, is_high_connectivity=False, tolerance=0.0):
        """ Label connected components.

            Args:
                is_high_connectivity: Boolean that choose between 4(false)
                - or 8(true)-connectivity in 2d case, and between 6(false)
                - or 26(true)-connectivity in 3d case. 
                tolerance: Tolerance used to determine if two neighboring 
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
                size_x: Number of columns (new size along the X-axis).
                size_y: Number of rows (new size along the Y-axis).
                size_z: Number of slices (new size along the Z-axis).
                size_c: Number of vector-channels (new size along the C-axis).
                interpolation_type:  Method of interpolation:
                    NONE_RAW = no interpolation: raw memory resizing.
                    NONE = no interpolation: additional space is filled 
                                          according to boundary_conditions.
                    NEAREST = nearest-neighbor interpolation.
                    MOVING_AVERAGE = moving average interpolation.
                    LINEAR = linear interpolation.
                    GRID = grid interpolation.
                    CUBIC = cubic interpolation.
                    LANCZOS = lanczos interpolation.
                boundary_conditions: Type of boundary conditions used if 
                                     necessary.
                    DIRICHLET | NEUMANN | PERIODIC | MIRROR
                centering_x: Set centering type (only if interpolation_type=NONE).
                centering_y: Set centering type (only if interpolation_type=NONE).
                centering_z: Set centering type (only if interpolation_type=NONE).
                centering_c: Set centering type (only if interpolation_type=NONE). 
        """
        self._cimg.resize(size_x, size_y, size_z, size_c, 
                          interpolation_type, boundary_conditions,
                          centering_x,
                          centering_y,
                          centering_z,
                          centering_c)
        return self



    ###########################################################################
    # Drawing functions
    ###########################################################################

    def _check_color(self, color):
        """ Raises a RuntimeError if color does not have the correct 
            number of entries."""
        n = self._cimg.spectrum()
        if not len(color) == n: 
            raise RuntimeError('Color should have {} entries'.format(n))

    def draw_rectangle(self, x0, y0, x1, y1, color, opacity=1):
        """ Draw a filled 2d rectangle. 

            Args:
                x0: X-coordinate of the upper-left rectangle corner. 
                y0: Y-coordinate of the upper-left rectangle corner. 
                x1: X-coordinate of the lower-right rectangle corner. 
                y1: Y-coordinate of the lower-right rectangle corner. 
                color: List of color value with spectrum() entries.
                opacity: Drawing opacity.

            Raises:
                RuntimeError: If list of color values does not have spectrum()
                entries.
        """
        self._check_color(color)
        self._cimg.draw_rectangle(x0, y0, x1, y1, color, opacity)
        return self

    # ...
    def draw_polygon(self, points, color, opacity=1):
        self._check_color(color)
        self._cimg.draw_polygon( points, color, opacity)
        return self

    def draw_circle(self, x0, y0, radius, color, opacity=1):
       self._check_color(color)
       self._cimg.draw_circle(x0, y0, radius, color, opacity)
       return self
    

    def display(self):
        """ Display image into a CImgDisplay window."""
        self._cimg.display()


