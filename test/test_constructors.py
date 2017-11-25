import unittest
import numpy as np
from context import cimg, CImg, get_test_image

class TestConstructors(unittest.TestCase):

    def test_noarg(self):
        im = CImg()
        self.assertEqual(im.shape, (0, 0, 0, 0))

    def test_from_file(self):
        im = CImg(get_test_image())
        self.assertEqual(im.shape, (3, 1, 426, 640))

    def test_from_numpy(self):
        arr = np.ones((100, 50))
        im = CImg(arr)
        self.assertTrue( np.allclose( arr, im.asarray().squeeze() ))

    def test_size(self):
        im = CImg((100, 50))
        self.assertEqual(im.shape, (1, 1, 50, 100))
        im = CImg((100))
        self.assertEqual(im.shape, (1, 1, 1, 100))

if __name__ == '__main__':
    unittest.main() 
            
