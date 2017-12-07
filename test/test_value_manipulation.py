import unittest
import numpy as np
from context import cimg, CImg, get_test_image


class TestValueManipulation(unittest.TestCase):
    """ Unit test for CImg value manipulation methods. """

    def test_fill(self):
        """ Test fill. """
        img = CImg((2, 2))
        img.fill(42)
        img_expected = CImg(np.ones((2, 2))*42)
        self.assertEqual(img, img_expected)

    def test_invert_endianness(self):
        """ Test invert endianness. """
        img = CImg((2, 2), dtype=cimg.uint16)
        img.fill(0xAAFF)
        img.invert_endianness()
        print(img.asarray())
        img_expected = CImg((2, 2), dtype=cimg.uint16)
        img_expected.fill(0xFFAA)
        self.assertEqual(img, img_expected)

    def test_rand(self):
        """ Test rand. """
        img = CImg((100,100))
        img.rand(-2, 2)
        val_min, val_max = img.min_max()
        self.assertGreaterEqual(val_min, -2)
        self.assertLessEqual(val_max, +2)

    def test_round(self):
        """ Test round. """
        img = CImg(np.array([2.3, -1.7, 1.5, -0.1]))
        img.round()
        img_expected = CImg(np.array([2, -2, 2, 0]))
        self.assertEqual(img, img_expected)

    def test_noise(self):
        """ Test noise. """
        img = CImg(np.zeros((5, 5)))
        img.noise(2)
        img_not_expected = CImg(np.zeros((5, 5)))
        self.assertNotEqual(img, img_not_expected)

    def test_normalize(self):
        """ Test normalize. """
        img = CImg((10, 10))
        img.rand(-10, 10)
        img.normalize(-5, 5)
        min_val, max_val = img.min_max()
        self.assertEqual(min_val, -5)
        self.assertEqual(max_val, 5)

    def test_norm(self):
        """ Test norm. """
        img = CImg((10, 10, 1, 3))
        arr = img.asarray()
        arr[0, :, :, :] = 0
        arr[1, :, :, :] = 1
        arr[2, :, :, :] = 2
        img.norm(cimg.LINF_NORM)
        img_expected = CImg((10, 10, 1, 1))
        img_expected.fill(2)
        self.assertEqual(img, img_expected)

    def test_cut(self):
        """ Test cut. """
        img = CImg((100, 100))
        img.rand(-10, 10)
        img.cut(0, 1)
        max_val, min_val = img.max_min()
        self.assertEqual(max_val, 1)
        self.assertEqual(min_val, 0)

    def test_quantize(self):
        """ Test quantize. """
        img = CImg(np.array([0, 1, 2, 3, 4]))
        img.quantize(2, keep_range=True)
        img_expected = CImg(np.array([0, 0, 2, 2, 2]))
        self.assertEqual(img, img_expected)

if __name__ == '__main__':
    unittest.main()
