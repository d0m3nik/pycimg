import unittest
import os
import numpy as np
from datetime import datetime
from context import cimg, CImg, get_test_image

class TestOps(unittest.TestCase):

    def test_getitem(self):
        """ Test __getitem__. """
        img = CImg(np.array([[1, 2, 3, 4],
                             [5, 6, 7, 8], 
                             [9, 10, 11, 12]]))

        # 1. All slices
        img2 = img[1:,:]
        img_expected = CImg(np.array([[2, 3, 4],
                                      [6, 7, 8],
                                      [10, 11, 12]]))
        self.assertEqual(type(img2).__name__, 'CImg')
        self.assertEqual(img2, img_expected)

        # 2. All integers
        self.assertEqual(img[0,1], 5)
        self.assertEqual(img[3,1], 8)
        # Out of bounds
        with self.assertRaises(IndexError):
            value = img[0,3]

        # 3. Mixed integers / slices
        img2 = img[0,:2]
        img_expected = CImg(np.array([[1],
                                      [5]]))
        self.assertEqual(img2, img_expected)
        img2 = img[0:2,1]
        img_expected = CImg(np.array([[5, 6]]))
        self.assertEqual(img2, img_expected)

        # Invalid index types
        with self.assertRaises(IndexError):
            v = img[0.1]
        with self.assertRaises(IndexError):
            v = img[:,0.1]

    def test_setitem(self):
        """ Test __setitem__. """
        # 1. All slices
        img = CImg(np.array([[1, 2, 3, 4],
                             [5, 6, 7, 8], 
                             [9, 10, 11, 12]]))
        img[2:4,1:3] = np.array([[1,2],[3,4]])
        img_expected = CImg(np.array([[1, 2, 3, 4],
                                      [5, 6, 1, 2], 
                                      [9, 10, 3, 4]]))

        # 2. All Integers
        img = CImg(np.array([[1, 2, 3, 4],
                             [5, 6, 7, 8], 
                             [9, 10, 11, 12]]))
        img[2,1] = 0
        img_expected = CImg(np.array([[1, 2, 3, 4],
                                      [5, 6, 0, 8], 
                                      [9, 10, 11, 12]]))

        # 3. Mixed integers / slices 
        img = CImg(np.array([[1, 2, 3, 4],
                             [5, 6, 7, 8], 
                             [9, 10, 11, 12]]))
        img[:,1] = 0
        img_expected = CImg(np.array([[1, 2, 3, 4],
                             [0, 0, 0, 0], 
                             [9, 10, 11, 12]]))


if __name__ == '__main__':
    unittest.main() 
            
