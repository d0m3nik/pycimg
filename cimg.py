import numpy as np
import os.path
from pycimg import CImg_int8, CImg_int16, CImg_int32, CImg_uint8, CImg_uint16, CImg_uint32, CImg_float32, CImg_float64 

class CImg:
    """ CImg is a wrapper class for the CImg library: """

    def __init__(self, dtype=np.float32):
        """ Create CImg with given data type.

            Supported datatypes are np.int8, np.int16, np.int32,
            np.uint8, np.uint16, np.uint32, np.float32, and np.float64.

            Args:
                dtype: Data type of CImg.

            Raises:
                RuntimeError: For unsupported data types.
        """
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

    # Operators
    def __call__(self, x):
        self._cimg(x)

    # Instance characteristics
    def width(self):
        """ Return width of image. """
        return self._cimg.width()

    def height(self):
        """ Return height of image. """
        return self._cimg.height()

    def depth(self):
        """ Return depth of image. """
        return self._cimg.depth()

    def spectrum(self):
        """ Return spectrum (number of channels) of image. """
        return self._cimg.spectrum()

    def size(self):
        """ Return the total number of pixel values in the image. """
        return self._cimg.size()

    def asarray(self):
        """ Convert image to a numpy array. """
        return self._cimg.asarray()

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


    def display(self):
        """ Display image into a CImgDisplay window."""
        self._cimg.display()


