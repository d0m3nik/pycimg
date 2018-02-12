import unittest
import numpy as np
from context import cimg, CImg, get_test_image

class TestConstructors(unittest.TestCase):

    def test_noarg(self):
        """ Test construction of empty image. """
        im = CImg()
        self.assertEqual(im.shape, (0, 0, 0, 0))

    def test_from_file(self):
        """ Test construction from file. """
        im = CImg(get_test_image())
        self.assertEqual(im.shape, (3, 1, 797, 1200))

    def test_from_numpy(self):
        """ Test construction from numpy array. """
        arr = np.ones((100, 50))
        im = CImg(arr)
        self.assertTrue( np.allclose( arr, im.asarray().squeeze() ))
    
    def test_fromarray(self):
        """ Test construction from array. """
        arr = np.ones((100, 50))
        im = CImg()
        im.fromarray(arr)
        self.assertTrue( np.allclose( arr, im.asarray().squeeze() ))
        invalid_arr = np.ones((2,3,4,5,6))
        self.assertRaises(RuntimeError, im.fromarray, invalid_arr)

    def test_size(self):
        """ Test construction with size tuple. """
        im = CImg((100, 50))
        self.assertEqual(im.shape, (1, 1, 50, 100))
        im = CImg((100))
        self.assertEqual(im.shape, (1, 1, 1, 100))

    def test_dtypes(self):
        """ Test construction for different data types. """
        dtypes = [cimg.uint8, cimg.uint16, cimg.uint32,
                  cimg.int8, cimg.int16, cimg.int32,
                  cimg.float32, cimg.float64
                ]
        for dtype in dtypes:
            im = CImg((2,3), dtype=dtype)
            self.assertEqual(im.size, 6)

        self.assertRaises(RuntimeError, CImg, dtype=1)
        self.assertRaises(RuntimeError, CImg, dict())

    def test_from_cimg(self):
        """ Test construction from other CImg. """
        img_a = CImg(np.array([[1, 2, 3], [4, 5, 6]]))
        img_b = CImg(img_a)
        self.assertEqual(img_a, img_b)
        img_a[0,0] = 5
        self.assertNotEqual(img_a, img_b)

if __name__ == '__main__':
    unittest.main() 
            
