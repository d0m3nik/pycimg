import numpy as np
import pytest
from context import pycimg, CImg, get_test_image


def test_noarg():
    """ Test construction of empty image. """
    im = CImg()
    assert im.shape == (0, 0, 0, 0)

def test_from_file():
    """ Test construction from file. """
    im = CImg(get_test_image())
    assert im.shape ==  (3, 1, 797, 1200)

def test_from_numpy():
    """ Test construction from numpy array. """
    arr = np.ones((100, 50))
    im = CImg(arr)
    assert np.allclose( arr, im.asarray().squeeze() )
    
def test_fromarray():
    """ Test construction from array. """
    arr = np.ones((100, 50))
    im = CImg()
    im.fromarray(arr)
    assert np.allclose( arr, im.asarray().squeeze() )
    invalid_arr = np.ones((2,3,4,5,6))
    with pytest.raises(RuntimeError):
        im.fromarray(invalid_arr)

def test_size():
    """ Test construction with size tuple. """
    im = CImg((100, 50))
    assert im.shape == (1, 1, 50, 100)
    im = CImg((100))
    assert im.shape == (1, 1, 1, 100)

def test_dtypes():
    """ Test construction for different data types. """
    dtypes = [pycimg.uint8, pycimg.uint16, pycimg.uint32,
              pycimg.int8, pycimg.int16, pycimg.int32,
              pycimg.float32, pycimg.float64
            ]
    for dtype in dtypes:
        im = CImg((2,3), dtype=dtype)
        assert im.size() == 6

    with pytest.raises(RuntimeError):
        CImg(dtype=1)
        CImg(dict())

    def test_from_cimg():
        """ Test construction from other CImg. """
        img_a = CImg(np.array([[1, 2, 3], [4, 5, 6]]))
        img_b = CImg(img_a)
        self.assertEqual(img_a, img_b)
        img_a[0,0] = 5
        self.assertNotEqual(img_a, img_b)

            
