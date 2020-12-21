import os
import numpy as np
import pytest
from context import * 

#def test_getitem():
#    """ Test __getitem__. """
#    img = CImg(np.array([[1, 2, 3, 4],
#                         [5, 6, 7, 8], 
#                         [9, 10, 11, 12]]))
#
#    # 1. All slices
#    img2 = img[1:,:]
#    img_expected = CImg(np.array([[2, 3, 4],
#                                  [6, 7, 8],
#                                  [10, 11, 12]]))
#    self.assertEqual(type(img2).__name__, 'CImg')
#    self.assertEqual(img2, img_expected)
#
#    # 2. All integers
#    self.assertEqual(img[0,1], 5)
#    self.assertEqual(img[3,1], 8)
#    # Out of bounds
#    with self.assertRaises(IndexError):
#        value = img[0,3]
#
#    # 3. Mixed integers / slices
#    img2 = img[0,:2]
#    img_expected = CImg(np.array([[1],
#                                  [5]]))
#    self.assertEqual(img2, img_expected)
#    img2 = img[0:2,1]
#    img_expected = CImg(np.array([[5, 6]]))
#    self.assertEqual(img2, img_expected)
#
#    # Invalid index types
#    with self.assertRaises(IndexError):
#        v = img[0.1]
#    with self.assertRaises(IndexError):
#        v = img[:,0.1]
#
#def test_setitem(self):
#    """ Test __setitem__. """
#    # 1. All slices
#    img = CImg(np.array([[1, 2, 3, 4],
#                         [5, 6, 7, 8], 
#                         [9, 10, 11, 12]]))
#    img[2:4,1:3] = np.array([[1,2],[3,4]])
#    img_expected = CImg(np.array([[1, 2, 3, 4],
#                                  [5, 6, 1, 2], 
#                                  [9, 10, 3, 4]]))
#    self.assertEqual(img, img_expected)
#
#    # 2. All Integers
#    img = CImg(np.array([[1, 2, 3, 4],
#                         [5, 6, 7, 8], 
#                         [9, 10, 11, 12]]))
#    img[2,1] = 0
#    img_expected = CImg(np.array([[1, 2, 3, 4],
#                                  [5, 6, 0, 8], 
#                                  [9, 10, 11, 12]]))
#    self.assertEqual(img, img_expected)
#
#    # 3. Mixed integers / slices 
#    img = CImg(np.array([[1, 2, 3, 4],
#                         [5, 6, 7, 8], 
#                         [9, 10, 11, 12]]))
#    img[:,1] = 0
#    img_expected = CImg(np.array([[1, 2, 3, 4],
#                         [0, 0, 0, 0], 
#                         [9, 10, 11, 12]]))
#    self.assertEqual(img, img_expected)

def test_add():
    """ Test __add__. """

    # 1. CImg + CImg 
    a = CImg(np.array([[1, 2, 3],
                       [4, 5, 6]]))
    b = CImg(np.array([[1, 1, 1],
                       [2, 3, 2]]))
    img_expected = CImg(np.array([[2, 3, 4],
                                  [6, 8, 8]]))
    img = a + b    
    assert img == img_expected

    # 2. CImg + scalar
    a = CImg(np.array([[1, 2, 3],
                       [4, 5, 6]]))
    img_expected = CImg(np.array([[3, 4, 5],
                                  [6, 7, 8]]))
    img = a + 2
    assert img == img_expected

def test_sub():
    """ Test __sub__. """

    # 1. CImg - CImg 
    a = CImg(np.array([[1, 2, 3],
                       [4, 5, 6]]))
    b = CImg(np.array([[1, 1, 1],
                       [2, 3, 2]]))
    img_expected = CImg(np.array([[0, 1, 2],
                                  [2, 2, 4]]))
    img = a - b    
    assert img == img_expected

    # 2. CImg - scalar
    a = CImg(np.array([[1, 2, 3],
                       [4, 5, 6]]))
    img_expected = CImg(np.array([[-1, 0, 1],
                                  [2, 3, 4]]))
    img = a - 2
    assert img == img_expected

def test_mul():
    """ Test __mul__. """

    # 1. CImg * CImg 
    a = CImg(np.array([[1, 2, 3],
                       [4, 5, 6]]))
    b = CImg(np.array([[1, 1, 1],
                       [2, 3, 2]]))
    img_expected = CImg(np.array([[1, 2, 3],
                                  [8, 15, 12]]))
    img = a * b    
    assert img == img_expected

    # 2. CImg * scalar
    a = CImg(np.array([[1, 2, 3],
                       [4, 5, 6]]))
    img_expected = CImg(np.array([[2, 4, 6],
                                  [8, 10, 12]]))
    img = a * 2
    assert img == img_expected

def test_truediv():
    """ Test __truediv__. """

    # 1. CImg / CImg 
    a = CImg(np.array([[1.0, 2.0, 3.0],
                       [4.0, 5.0, 6.0]]))
    b = CImg(np.array([[2, 2, 2],
                       [4, 2, 3]]))
    img_expected = CImg(np.array([[0.5, 1.0, 1.5],
                                  [1.0, 2.5, 2.0]]))
    img = a / b    
    assert img == img_expected

    # 2. CImg / scalar
    a = CImg(np.array([[1.0, 2.0, 3.0],
                       [4.0, 5.0, 6.0]]))
    img_expected = CImg(np.array([[0.5, 1.0, 1.5],
                                  [2.0, 2.5, 3.0]]))
    img = a / 2
    assert img == img_expected

def test_floordiv():
    """ Test __floordiv__. """

    # 1. CImg // CImg 
    a = CImg(np.array([[1.0, 2.0, 3.0],
                       [4.0, 5.0, 6.0]]))
    b = CImg(np.array([[2, 2, 2],
                       [4, 2, 3]]))
    img_expected = CImg(np.array([[0, 1, 1],
                                  [1, 2, 2]]))
    img = a // b    
    assert img == img_expected

    # 2. CImg // scalar
    a = CImg(np.array([[1.0, 2.0, 3.0],
                       [4.0, 5.0, 6.0]]))
    img_expected = CImg(np.array([[0, 1, 1],
                                  [2, 2, 3]]))
    img = a // 2
    assert img == img_expected

def test_iadd():
    """ Test __iadd__. """

    # 1. CImg += CImg 
    img = CImg(np.array([[1, 7, 3],
                       [4, 5, 6]]))
    b = CImg(np.array([[1, 1, 0],
                       [2, 0, 3]]))
    img_expected = CImg(np.array([[2, 8, 3],
                                  [6, 5, 9]]))
    img += b    
    assert img == img_expected

    # 2. CImg += scalar
    img = CImg(np.array([[1, 7, 3],
                       [4, 5, 6]]))
    img_expected = CImg(np.array([[3, 9, 5],
                                  [6, 7, 8]]))
    img += 2    
    assert img == img_expected

def test_isub():
    """ Test __isub__. """

    # 1. CImg -= CImg 
    img = CImg(np.array([[1, 2, 3],
                       [4, 5, 6]]))
    b = CImg(np.array([[1, 1, 1],
                       [2, 3, 2]]))
    img_expected = CImg(np.array([[0, 1, 2],
                                  [2, 2, 4]]))
    img -= b    
    assert img == img_expected

    # 2. CImg -= scalar
    img = CImg(np.array([[1, 2, 3],
                       [4, 5, 6]]))
    img_expected = CImg(np.array([[-1, 0, 1],
                                  [2, 3, 4]]))
    img -= 2
    assert img == img_expected

def test_imul():
    """ Test __imul__. """

    # 1. CImg *= CImg 
    img = CImg(np.array([[1, 2, 3],
                       [4, 5, 6]]))
    b = CImg(np.array([[1, 1, 1],
                       [2, 3, 2]]))
    img_expected = CImg(np.array([[1, 2, 3],
                                  [8, 15, 12]]))
    img *= b    
    assert img == img_expected

    # 2. CImg *= scalar
    img = CImg(np.array([[1, 2, 3],
                       [4, 5, 6]]))
    img_expected = CImg(np.array([[2, 4, 6],
                                  [8, 10, 12]]))
    img *= 2
    assert img == img_expected

def test_itruediv():
    """ Test __itruediv__. """

    # 1. CImg /= CImg 
    img = CImg(np.array([[1.0, 2.0, 3.0],
                       [4.0, 5.0, 6.0]]))
    b = CImg(np.array([[2, 2, 2],
                       [4, 2, 3]]))
    img_expected = CImg(np.array([[0.5, 1.0, 1.5],
                                  [1.0, 2.5, 2.0]]))
    img /= b    
    assert img == img_expected

    # 2. CImg /= scalar
    img = CImg(np.array([[1.0, 2.0, 3.0],
                       [4.0, 5.0, 6.0]]))
    img_expected = CImg(np.array([[0.5, 1.0, 1.5],
                                  [2.0, 2.5, 3.0]]))
    img /= 2
    assert img == img_expected

def test_ifloordiv():
    """ Test __ifloordiv__. """

    # 1. CImg //= CImg 
    img = CImg(np.array([[1.0, 2.0, 3.0],
                       [4.0, 5.0, 6.0]]))
    b = CImg(np.array([[2, 2, 2],
                       [4, 2, 3]]))
    img_expected = CImg(np.array([[0, 1, 1],
                                  [1, 2, 2]]))
    img //= b    
    assert img == img_expected

    # 2. CImg //= scalar
    img = CImg(np.array([[1.0, 2.0, 3.0],
                       [4.0, 5.0, 6.0]]))
    img_expected = CImg(np.array([[0, 1, 1],
                                  [2, 2, 3]]))
    img //= 2
    assert img == img_expected
