import unittest
from context import cimg, CImg, get_test_image
import numpy as np

class TestMathematical(unittest.TestCase):

    def test_sqr(self):
        arr = np.random.randn(10,5)
        im = CImg(arr)
        self.assertTrue( np.allclose( arr*arr, im.sqr().asarray() ) )

    def test_sqrt(self):
        arr = np.ones((10,5))
        im = CImg(arr)
        self.assertTrue( np.allclose( arr, im.sqrt().asarray() ) )

    def test_exp(self):
        arr = np.random.randn(10,5)
        im = CImg(arr)
        self.assertTrue( np.allclose( np.exp(arr), im.exp().asarray() ) )

    def test_log(self):
        arr = np.random.randn(10,5)
        arr = np.maximum(1e-6, arr)
        im = CImg(arr)
        self.assertTrue( np.allclose( np.log(arr), im.log().asarray() ) )

    def test_log2(self):
        arr = np.random.randn(10,5)
        arr = np.maximum(1e-6, arr)
        im = CImg(arr)
        self.assertTrue( np.allclose( np.log2(arr), im.log2().asarray() ) )

    def test_log10(self):
        arr = np.random.randn(10,5)
        arr = np.maximum(1e-6, arr)
        im = CImg(arr)
        self.assertTrue( np.allclose( np.log10(arr), im.log10().asarray() ) )

    def test_abs(self):
        arr = np.random.randn(10,5)
        im = CImg(arr)
        self.assertTrue( np.allclose( np.abs(arr), im.abs().asarray() ) )

    def test_sign(self):
        arr = np.random.randn(10,5)
        im = CImg(arr)
        self.assertTrue( np.allclose( np.sign(arr), im.sign().asarray() ) )

    def test_cos(self):
        arr = np.ones((10,5))
        im = CImg(arr)
        self.assertTrue( np.allclose( np.cos(arr), im.cos().asarray() ) )

    def test_sin(self):
        arr = np.random.randn(10,5)
        im = CImg(arr)
        self.assertTrue( np.allclose( np.sin(arr), im.sin().asarray() ) )

#    def test_sinc(self):
#        arr = np.random.randn(10,5)
#        im = CImg(arr)
#        print(np.sinc(arr))
#        print(im.sinc().asarray())
#        self.assertTrue( np.allclose( np.sinc(arr), im.sinc().asarray() ) )

    def test_tan(self):
        arr = np.random.randn(10,5)
        im = CImg(arr)
        self.assertTrue( np.allclose( np.tan(arr), im.tan().asarray() ) )

    def test_sinh(self):
        arr = np.random.randn(10,5)
        im = CImg(arr)
        self.assertTrue( np.allclose( np.sinh(arr), im.sinh().asarray() ) )

    def test_tanh(self):
        arr = np.random.randn(10,5)
        im = CImg(arr)
        self.assertTrue( np.allclose( np.tanh(arr), im.tanh().asarray() ) )

    def test_acos(self):
        arr = -np.ones((10,5))
        im = CImg(arr)
        self.assertTrue( np.allclose( np.arccos(arr), im.acos().asarray() ) )

#    def test_asin(self):
#        arr = np.random.randn(10,5)
#        im = CImg(arr)
#        self.assertTrue( np.allclose( np.arcsin(arr), im.asin().asarray() ) )
    
    def test_atan(self):
        arr = np.random.randn(10,5)
        im = CImg(arr)
        self.assertTrue( np.allclose( np.arctan(arr), im.atan().asarray() ) )

    # def test_atan2(self, img):
    #     arr = np.random.randn(10,5)
    #     im = CImg(arr)
    #     self.assertTrue( np.allclose( np.math.atan2(arr), im.atan2().asarray() ) )
    #

if __name__ == '__main__':
    unittest.main() 
            
