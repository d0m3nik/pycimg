import unittest
from context import cimg, CImg, get_test_image
import numpy as np

class TestVectorMatrixOps(unittest.TestCase):

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
