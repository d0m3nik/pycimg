import unittest
import numpy as np
import pytest
from context import *


def test_linear_atX():
    """ Test linear_atX interpolation. """
    img = CImg(np.array([0, 1, 2]))
    assert img.linear_atX(0.5) == 0.5
    assert img.linear_atX(1.5) == 1.5


def test_linear_atXY():
    """ Test linear_atXY interpolation. """
    img = CImg(np.array([
        [0, 1, 2],
        [3, 4, 5]
    ]))
    assert img.linear_atXY(0.5, 0.5) == 2.0
    assert img.linear_atXY(1.5, 0.5) == 3.0


def test_linear_atXYZ():
    """ Test linear_atXYZ interpolation. """
    img = CImg(np.array([
       [
        [0, 1, 2],
        [3, 4, 5]
       ],
       [
        [6, 7, 8],
        [9, 10, 11]
       ]
    ]))
    assert img.linear_atXYZ(0.5, 0.5, 0.5) == 5.0
    assert img.linear_atXYZ(1.5, 0.5, 0.5) == 6.0


def test_linear_atXYZC():
    """ Test linear_atXYZC interpolation. """
    img = CImg(np.array([
       [
        [0, 1, 2],
        [3, 4, 5]
       ],
       [
        [0, 1, 2],
        [3, 4, 5]
       ]
    ]))
    assert img.linear_atXYZC(0.5, 0.5, 0.5, 0.5) == 2.0
    assert img.linear_atXYZC(1.5, 0.5, 0.5, 0.5) == 3.0


def test_resize():
   """ Test resize. """
   img = CImg()
   img.load(get_test_image())
   img.resize(100, 50)
   assert img.width == 100
   assert img.height == 50
   assert img.depth == 1
   assert img.spectrum == 3
   assert img.shape == (3, 1, 50, 100)


def test_resize_halfXY():
   """ Test resize half XY."""
   img = CImg(get_test_image())
   img.resize_halfXY()
   assert img.width == 600
   assert img.height == 398
   assert img.depth == 1
   assert img.spectrum == 3


def test_resize_doubleXY():
   """ Test resize double XY."""
   img = CImg(get_test_image())
   img.resize_doubleXY()
   assert img.width == 2*1200
   assert img.height == 2*797
   assert img.depth == 1
   assert img.spectrum == 3


def test_resize_tripleXY():
   """ Test resize triple XY."""
   img = CImg(get_test_image())
   img.resize_tripleXY()
   assert img.width == 3*1200
   assert img.height == 3*797
   assert img.depth == 1
   assert img.spectrum == 3


def test_mirror():
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
   assert img == img_expected


def test_shift():
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
   assert img == img_expected


def test_permute_axes():
   """ Test permute axes. """
   img = CImg(np.ones((2, 3, 4, 5)))
   img.permute_axes("yxzc")
   assert img.shape == (2, 3, 5, 4)
   with pytest.raises(RuntimeError):
       img.permute_axes("abcd")


def test_unroll():
   """ Test unroll. """
   img = CImg(np.zeros((2, 3)))
   img.unroll('x')
   assert img.shape == (1, 1, 1, 6)


def test_rotate():
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
   assert img == img_expected


def test_crop():
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
   assert img == img_expected


def test_autocrop():
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
   assert img == img_expected

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
   assert img == img_expected


def test_append():
   """ Test append. """
   img = CImg(np.array([
       [1, 1],
       [1, 1],
       [0, 1],
       [0, 1]
   ]))
   img_b = CImg(np.array([
       [0, 0],
       [0, 0],
       [0, 0],
       [0, 0]
   ]))
   img.append(img_b)
   img_expected = CImg(np.array([
       [1, 1, 0, 0],
       [1, 1, 0, 0],
       [0, 1, 0, 0],
       [0, 1, 0, 0]
   ]))
   assert img == img_expected

def test_apply_geometric_transform():
   """ Test apply_geometric_transform. """
   img = CImg(np.array([[ 
       [0, 1],
       [1, 1]
      ],
      [
       [0, 1],
       [1, 1]
      ]
   ])) 
   M  = CImg(np.array([
       [1, 0, 0],
       [0, 1, 0],
       [0, 0, 1]
   ]))
   t  = CImg(np.array([0, 0, 0]))

   img_expected = CImg(img)
   img.apply_geometric_transform(1.0 ,M, t)

   assert img == img_expected
   M  = CImg(np.array([
       [-1, 0, 0],
       [0, -1, 0],
       [0, 0, 1]
   ]))
   img_expected = CImg(np.array([[ 
       [0, 0],
       [1, 1]
      ],
      [
       [0, 0],
       [1, 1]
      ]
   ])) 
   img.apply_geometric_transform(1.0 ,M, t)
   assert img == img_expected
