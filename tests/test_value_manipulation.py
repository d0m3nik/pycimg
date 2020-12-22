import unittest
import numpy as np
from .context import * 


""" Unit test for CImg value manipulation methods. """

def test_fill():
    """ Test fill. """
    img = CImg((2, 2))
    img.fill(42)
    img_expected = CImg(np.ones((2, 2))*42)
    assert img == img_expected

def test_invert_endianness():
    """ Test invert endianness. """
    img = CImg((2, 2), dtype=uint16)
    img.fill(0xAAFF)
    img.invert_endianness()
    print(img.asarray())
    img_expected = CImg((2, 2), dtype=uint16)
    img_expected.fill(0xFFAA)
    assert img == img_expected

def test_rand():
    """ Test rand. """
    img = CImg((100,100))
    img.rand(-2, 2)
    val_min, val_max = img.min_max()
    assert val_min >= -2
    assert val_max <= +2

def test_round():
    """ Test round. """
    img = CImg(np.array([2.3, -1.7, 1.5, -0.1]))
    img.round()
    img_expected = CImg(np.array([2, -2, 2, 0]))
    assert img == img_expected

def test_noise():
    """ Test noise. """
    img = CImg(np.zeros((5, 5)))
    img.noise(2)
    img_not_expected = CImg(np.zeros((5, 5)))
    assert img != img_not_expected

def test_normalize():
    """ Test normalize. """
    img = CImg((10, 10))
    img.rand(-10, 10)
    img.normalize(-5, 5)
    min_val, max_val = img.min_max()
    assert min_val == -5
    assert max_val == 5

def test_norm():
    """ Test norm. """
    img = CImg((10, 10, 1, 3))
    arr = img.asarray()
    arr[0, :, :, :] = 0
    arr[1, :, :, :] = 1
    arr[2, :, :, :] = 2
    img.norm(LINF_NORM)
    img_expected = CImg((10, 10, 1, 1))
    img_expected.fill(2)
    assert img == img_expected

def test_cut():
    """ Test cut. """
    img = CImg((100, 100))
    img.rand(-10, 10)
    img.cut(0, 1)
    max_val, min_val = img.max_min()
    assert max_val == 1
    assert min_val == 0

def test_quantize():
    """ Test quantize. """
    img = CImg(np.array([0, 1, 2, 3, 4]))
    img.quantize(2, keep_range=True)
    img_expected = CImg(np.array([0, 0, 2, 2, 2]))
    assert img == img_expected

def test_threshold():
    """ Test threshold. """
    img = CImg(np.array([0, 1, 2, 3, 4]))
    img.threshold(2)
    img_expected = CImg(np.array([0, 0, 1, 1, 1]))
    assert img == img_expected

def test_histogram():
    """ Test histogram. """
    img = CImg(np.array([0, 1, 2, 3, 4]))
    img.histogram(2, 0, 4)
    img_expected = CImg(np.array([2, 3]))
    assert img == img_expected

def test_equalize():
    """ Test equalize. """
    img = CImg(np.array([1, 1, 2, 2]))
    img.equalize(2, 1, 2)
    img_expected = CImg(np.array([1.5, 1.5, 2, 2]))
    assert img == img_expected

def test_label():
    """ Test label. """
    img = CImg(np.array([[0, 1, 0, 0], 
                         [1, 1, 1, 0], 
                         [0, 0, 0, 0]]))
    img.label()
    img_expected = CImg(np.array([[ 0,  1,  2,  2],
                                  [ 1,  1,  1,  2],
                                  [ 2,  2,  2,  2]]))
    assert img == img_expected
