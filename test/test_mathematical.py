import unittest
from context import cimg, CImg, get_test_image
import numpy as np

class TestMathematical(unittest.TestCase):

    def test_sqr(self):
        arr = np.random.randn(10, 5)
        img = CImg(arr)
        self.assertTrue( np.allclose( arr*arr, img.sqr().asarray() ) )

    def test_sqrt(self):
        arr = np.ones((10, 5))
        img = CImg(arr)
        self.assertTrue( np.allclose( arr, img.sqrt().asarray() ) )

    def test_exp(self):
        arr = np.random.randn(10, 5)
        img = CImg(arr)
        self.assertTrue( np.allclose( np.exp(arr), img.exp().asarray() ) )

    def test_log(self):
        exponents = np.linspace(-10, 10, 11)
        arr = (np.e * np.ones((1,11)))**exponents
        img = CImg(arr)
        self.assertTrue( np.allclose( exponents, 10, 11), img.log().asarray() )

    def test_log2(self):
        exponents = np.linspace(-10, 10, 11)
        arr = (2* np.ones((1,11)))**exponents
        img = CImg(arr)
        self.assertTrue( np.allclose( exponents, img.log2().asarray() ) )

    def test_log10(self):
        exponents = np.linspace(-10, 10, 11)
        arr = (10* np.ones((1,11)))**exponents
        img = CImg(arr)
        self.assertTrue( np.allclose( exponents, img.log10().asarray() ) )

    def test_abs(self):
        arr = np.random.randn(10, 5)
        img = CImg(arr)
        self.assertTrue( np.allclose( np.abs(arr), img.abs().asarray() ) )

    def test_sign(self):
        arr = np.random.randn(10, 5)
        img = CImg(arr)
        self.assertTrue( np.allclose( np.sign(arr), img.sign().asarray() ) )

    def test_cos(self):
        arr = np.ones((10, 5))
        img = CImg(arr)
        self.assertTrue( np.allclose( np.cos(arr), img.cos().asarray() ) )

    def test_sin(self):
        arr = np.random.randn(10, 5)
        img = CImg(arr)
        self.assertTrue( np.allclose( np.sin(arr), img.sin().asarray() ) )

    def test_sinc(self):
        arr  = np.linspace(-10, 10, 100)
        img = CImg(arr)
        self.assertTrue( np.allclose( np.sinc(arr/np.pi), img.sinc().asarray() ) )

    def test_tan(self):
        arr = np.linspace(-0.5, 0.5, 100)
        img = CImg(arr)
        self.assertTrue( np.allclose( np.tan(arr), img.tan().asarray() ) )

    def test_sinh(self):
        arr = np.random.randn(10, 5)
        img = CImg(arr)
        self.assertTrue( np.allclose( np.sinh(arr), img.sinh().asarray() ) )

    def test_tanh(self):
        arr = np.random.randn(10, 5)
        img = CImg(arr)
        self.assertTrue( np.allclose( np.tanh(arr), img.tanh().asarray() ) )

    def test_acos(self):
        arr = -np.ones((10, 5))
        img = CImg(arr)
        self.assertTrue( np.allclose( np.arccos(arr), img.acos().asarray() ) )

#    def test_asin(self):
#        arr = np.random.randn(10, 5)
#        img = CImg(arr)
#        self.assertTrue( np.allclose( np.arcsin(arr), img.asin().asarray() ) )
    
    def test_atan(self):
        arr = np.random.randn(10, 5)
        img = CImg(arr)
        self.assertTrue( np.allclose( np.arctan(arr), img.atan().asarray() ) )

    def test_atan2(self):
        """ Test atan2. """
        x = np.random.rand(5, 2)
        y = np.random.rand(5, 2)
        img1 = CImg(y, dtype=cimg.float64)
        img2 = CImg(x, dtype=cimg.float64)
        delta = np.abs(img1.atan2(img2).asarray() - np.arctan2(y, x))
        self.assertTrue(np.allclose(delta, np.zeros((5, 2))))

    def test_mul(self):
        """ Test mul. """
        x = np.ones((5, 4))*2
        y = np.ones((5, 4))*3
        img_x = CImg(x)
        img_y = CImg(y)
        img_x.mul(img_y)
        img_expected = CImg(x*y)
        self.assertEqual(img_x, img_expected)

    def test_div(self):
        """ Test div. """
        x = np.ones((5, 4))*2
        y = np.ones((5, 4))*3
        img_x = CImg(x)
        img_y = CImg(y)
        img_x.div(img_y)
        img_expected = CImg(x/y)
        self.assertEqual(img_x, img_expected)

    def test_pow(self):
        """ Test pow. """
        x = np.ones((7, 3))*2
        img = CImg(x)
        img.pow(3)
        img_expected = CImg(x**3)
        self.assertEqual(img, img_expected)

    def test_min_max(self):
        """ Test min_max. """
        img = CImg(np.array([[2, -1],[0, 4]]))
        self.assertEqual(img.min_max(), (-1, 4))

    def test_max_min(self):
        """ Test max_min. """
        img = CImg(np.array([[2, -1],[0, 4]]))
        self.assertEqual(img.max_min(), (4, -1))

    def test_kth_smallest(self):
        """ Test kth smallest. """
        img = CImg(np.array([[2, -1], [0, 4]]))
        self.assertEqual(img.kth_smallest(0), -1)
        self.assertEqual(img.kth_smallest(1), 0)
        self.assertEqual(img.kth_smallest(2), 2)
        self.assertEqual(img.kth_smallest(3), 4)

    def test_variance(self):
        """ Test variance. """
        img = CImg(np.array([[2, -5], [0, 3]]))
        self.assertEqual(img.variance(), 38.0/3.0)

    def test_variance_mean(self):
        """ Test variance + mean. """
        img = CImg(np.array([[2, -5], [0, 3]]))
        self.assertEqual(img.variance_mean(), (38.0/3.0, 0))

    def test_variance_noise(self):
        """ Test variance noise. """
        pass

    def test_mse(self):
        """ Test MSE. """
        img1 = CImg(np.array([[2, -5], [0, 3]]))
        img2 = CImg(np.array([[2, -3], [0, 3]]))
        self.assertEqual(img1.mse(img2), 1.0)

    def test_psnr(self):
        """ Test PSNR. """
        pass

    def test_magnitude(self):
        """ Test magnitude. """
        img = CImg(np.array([[2, -5], [0, 3]]))
        self.assertEqual(img.magnitude(cimg.L1_NORM), 10)

    def test_dot(self):
        """ Test dot. """
        img1 = CImg(np.array([[2, -5], [0, 3]]))
        img2 = CImg(np.array([[2, -3], [0, 3]]))
        self.assertEqual(img1.dot(img2), 28)

if __name__ == '__main__':
    unittest.main()
