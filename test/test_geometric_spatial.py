import unittest
import numpy as np
from context import cimg, CImg, get_test_image


class TestGeometricSpatial(unittest.TestCase):

    def test_resize(self):
        """ Test resize. """
        img = CImg()
        img.load(get_test_image())
        img.resize(100, 50)
        self.assertEqual(img.width, 100)
        self.assertEqual(img.height, 50)
        self.assertEqual(img.depth, 1)
        self.assertEqual(img.spectrum, 3)
        self.assertEqual(img.shape, (3, 1, 50, 100))

    def test_resize_halfXY(self):
        """ Test resize half XY."""
        img = CImg(get_test_image())
        img.resize_halfXY()
        self.assertEqual(img.width, 320)
        self.assertEqual(img.height, 213)
        self.assertEqual(img.depth, 1)
        self.assertEqual(img.spectrum, 3)


    def test_resize_doubleXY(self):
        """ Test resize double XY."""
        img = CImg(get_test_image())
        img.resize_doubleXY()
        self.assertEqual(img.width, 2*640)
        self.assertEqual(img.height, 2*426)
        self.assertEqual(img.depth, 1)
        self.assertEqual(img.spectrum, 3)

    def test_resize_tripleXY(self):
        """ Test resize triple XY."""
        img = CImg(get_test_image())
        img.resize_tripleXY()
        self.assertEqual(img.width, 3*640)
        self.assertEqual(img.height, 3*426)
        self.assertEqual(img.depth, 1)
        self.assertEqual(img.spectrum, 3)

    def test_mirror(self):
        """ Test mirror. """
        img = CImg(np.array([
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 0, 0]
            ]))
        img.mirror('x')
        img_expected = CImg(np.array([
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 1]
            ]))
        self.assertEqual(img, img_expected)

    def test_shift(self):
        """ Test shift. """
        img = CImg(np.array([
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 0, 0]
            ]))
        img.shift(1)
        img_expected = CImg(np.array([
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0]
            ]))
        self.assertEqual(img, img_expected)

    def test_permute_axes(self):
        """ Test permute axes. """
        img = CImg(np.ones((2, 3, 4, 5)))
        img.permute_axes("yxzc")
        self.assertEqual(img.shape, (2, 3, 5, 4))
        with self.assertRaises(RuntimeError):
            img.permute_axes("abcd")

    def test_unroll(self):
        """ Test unroll. """
        img = CImg(np.zeros((2, 3))) 
        img.unroll('x')
        self.assertEqual(img.shape, (1, 1, 1, 6))
        with self.assertRaises(RuntimeError):
            img.unroll('g')

    def test_rotate(self):
        """ Test rotate. """
        img = CImg(np.array([
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0]
            ]))
        img.rotate(90)
        img_expected = CImg(np.array([
            [0, 0, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
            ]))
        self.assertEqual(img, img_expected)

    def test_crop(self):
        """ Test crop. """
        img = CImg(np.array([
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0]
            ]))
        img.crop(1, 0, 0, 0, 3, 3, 0, 0)
        img_expected = CImg(np.array([
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0]
            ]))
        self.assertEqual(img, img_expected)
 
    def test_autocrop(self):
        """ Test autocrop. """
        img = CImg(np.array([
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0]
            ]))
        img.autocrop()
        img_expected = CImg(np.array([
            [1, 1],
            [1, 1],
            [0, 1],
            [0, 1]
            ]))
        self.assertEqual(img, img_expected)

        img = CImg(np.array([
            [1, 1, 1, 1],
            [1, 2, 2, 1],
            [1, 2, 2, 1],
            [1, 1, 1, 1]
            ]))
        img.autocrop(1, "x")
        img_expected = CImg(np.array([
            [1, 1],
            [2, 2],
            [2, 2],
            [1, 1]
            ]))
        print(img.asarray())
        self.assertEqual(img, img_expected)

if __name__ == '__main__':
    unittest.main() 
            
