import unittest
import numpy as np
from context import * 


#def test_correlate():
#    """ Test correlate. """
#    img = CImg(np.array([[0, 0, 0, 0],
#                         [0, 1, 1, 0],
#                         [0, 1, 1, 0],
#                         [0, 0, 0, 0]]))
#    kernel = CImg(np.array([[1, 1],
#                            [1, 1]]))
#    img.correlate(kernel)
#    img_expected = CImg(np.array([[1, 2, 1, 0],
#                                  [2, 4, 2, 0],
#                                  [1, 2, 1, 0],
#                                  [0, 0, 0, 0]]))
#    assert img == img_expected
#
#def test_convolve():
#    """ Test convolve. """
#    img = CImg(np.array([[0, 0, 0, 0],
#                         [0, 1, 1, 0],
#                         [0, 1, 1, 0],
#                         [0, 0, 0, 0]]))
#    kernel = CImg(np.array([[1, 1],
#                            [1, 1]]))
#    img.convolve(kernel)
#    img_expected = CImg(np.array([[0, 0, 0, 0],
#                                  [0, 1, 2, 1],
#                                  [0, 2, 4, 2],
#                                  [0, 1, 2, 1]]))
#    assert img == img_expected
#
#def test_cumulate():
#    """ Test cumulate. """
#    img = CImg(np.array([[0, 0, 0, 0],
#                         [0, 1, 1, 0],
#                         [0, 1, 1, 0],
#                         [0, 0, 0, 0]]))
#    img.cumulate("x")
#    print(img)
#    img_expected = CImg(np.array([[0, 0, 0, 0],
#                                  [0, 1, 2, 2],
#                                  [0, 1, 2, 2],
#                                  [0, 0, 0, 0]]))
#    assert img == img_expected
#
#def test_erode():
#    """ Test erode. """
#    img = CImg(np.array([[0, 0, 0, 0],
#                         [0, 1, 1, 0],
#                         [0, 1, 1, 0],
#                         [0, 0, 0, 0]]))
#    kernel = CImg(np.array([[1, 1],
#                            [1, 1]]))
#    img.erode(kernel)
#    img_expected = CImg(np.array([[0, 0, 0, 0],
#                                  [0, 1, 0, 0],
#                                  [0, 0, 0, 0],
#                                  [0, 0, 0, 0]]))
#    assert img == img_expected
#
#def test_dilate():
#    """ Test dilate. """
#    img = CImg(np.array([[0, 0, 0, 0],
#                         [0, 1, 1, 0],
#                         [0, 1, 1, 0],
#                         [0, 0, 0, 0]]))
#    kernel = CImg(np.array([[1, 1],
#                            [1, 1]]))
#    img.dilate(kernel)
#    img_expected = CImg(np.array([[0, 0, 0, 0],
#                                  [0, 1, 1, 1],
#                                  [0, 1, 1, 1],
#                                  [0, 1, 1, 1]]))
#    assert img == img_expected
#
#def test_watershed():
#    """ Test watershed. """
#    img = CImg(np.array([[0, 0.5, 1, 0.5],
#                         [1, 1, 0.5, 0],
#                         [0.5, 1, 0.5, 0],
#                         [1, 0.5, 0, 0]]))
#    priority = CImg((4, 4))
#    priority.fill(1)
#    img.watershed(priority)
#    img_expected = CImg(np.array([[0.5, 0.5, 1, 0.5],
#                                  [1, 1, 0.5, 0.5],
#                                  [0.5, 1, 0.5, 0.5],
#                                  [1, 0.5, 0.5, 0.5]]))
#    assert img == img_expected
#
#def test_deriche():
#    """ Test deriche. """
#    img = CImg(np.array([[0, 0, 0, 0],
#                         [0, 1, 1, 0],
#                         [0, 1, 1, 0],
#                         [0, 0, 0, 0]]))
#    img.deriche(1)
#    img_expected = CImg(np.array([[0, 0, 0, 0],
#                                  [0.26966834, 0.62711906, 0.62711906, 0.26966834],
#                                  [0.26966834, 0.62711906, 0.62711906, 0.26966834],
#                                  [0, 0, 0, 0]]))
#    assert np.allclose(img.asarray(), img_expected.asarray())
#
#
#def test_vanvliet():
#    """ Test vanvliet. """
#    img = CImg(np.array([[0, 0, 0, 0],
#                         [0, 1, 1, 0],
#                         [0, 1, 1, 0],
#                         [0, 0, 0, 0]]))
#    img.vanvliet(1, FIRST_DERIV)
#    img_expected = CImg(np.array([[0, 0, 0, 0],
#                                  [0, 0.21424547, -0.09127644, -0.08401725],
#                                  [0, 0.21424547, -0.09127644, -0.08401725],
#                                  [0, 0, 0, 0]]))
#    assert np.allclose(img.asarray(), img_expected.asarray())
#
#def test_blur():
#    """ Test blur. """
#    img = CImg(np.array([[0, 0, 0, 0],
#                         [0, 1, 1, 0],
#                         [0, 1, 1, 0],
#                         [0, 0, 0, 0]]))
#    img.blur(0.5)
#    img_expected = CImg(np.array([[ 0.01423194,  0.10418227,  0.10418227,  0.01423194],
#                                  [ 0.10418227,  0.76264691,  0.76264691,  0.10418226],
#                                  [ 0.10418227,  0.76264691,  0.76264691,  0.10418226],
#                                  [ 0.01423194,  0.10418227,  0.10418227,  0.01423194]]))
#    assert np.allclose(img.asarray(), img_expected.asarray())
#
#def test_boxfilter():
#    """ Test boxfilter. """
#    img = CImg(np.array([[0, 0, 0, 0],
#                         [0, 1, 1, 0],
#                         [0, 1, 1, 0],
#                         [0, 0, 0, 0]]))
#    img.boxfilter(2, 0, axis="y")
#    img_expected = CImg(np.array([[0, 0.25, 0.25, 0],
#                                  [0, 0.75, 0.75, 0],
#                                  [0, 0.75, 0.75, 0],
#                                  [0, 0.25, 0.25, 0]]))
#    assert np.allclose(img.asarray(), img_expected.asarray())
#
#def test_blur_box():
#    """ Test blur_box. """
#    img = CImg(np.array([[0, 0, 0, 0],
#                         [0, 1, 1, 0],
#                         [0, 1, 1, 0],
#                         [0, 0, 0, 0]]))
#    img.blur_box(2)
#    img_expected = CImg(np.array([[0.0625, 0.1875, 0.1875, 0.0625],
#                                  [0.1875, 0.5625, 0.5625, 0.1875],
#                                  [0.1875, 0.5625, 0.5625, 0.1875],
#                                  [0.0625, 0.1875, 0.1875, 0.0625]]))
#    assert img == img_expected
#
#def test_blur_median():
#    """ Test blur median. """
#    img = CImg(np.array([[0, 0, 0, 0],
#                         [0, 1, 1, 0],
#                         [0, 1, 1, 0],
#                         [0, 0, 0, 0]]))
#    img.blur_median(2)
#    img_expected = CImg(np.array([[0, 0.5, 0, 0],
#                                  [0.5, 1, 0.5, 0],
#                                  [0, 0.5, 0, 0],
#                                  [0, 0, 0, 0]]))
#    assert img == img_expected
#
#def test_sharpen():
#    """ Test sharpen. """
#    img = CImg(np.array([[0, 0.5, 0.5, 0],
#                         [0, 1, 1, 0.5],
#                         [0.5, 1, 1, 0],
#                         [0, 0.5, 0.5, 0]]))
#    img.sharpen(1)
#    print(img)
#    img_expected = CImg(np.array([[0,  0.5, 0.5, 0],
#                                  [0,  1, 1, 0.83333337],
#                                  [0.83333337,  1, 1, 0],
#                                  [0,  0.5, 0.5, 0]]))
#    assert img == img_expected
#