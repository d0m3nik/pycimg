import unittest
from datetime import datetime
import os

import numpy as np
import pytest
from context import *

def _check_image_dimensions(im):
    assert im.width == 1200
    assert im.height == 797
    assert im.depth == 1
    assert im.spectrum == 3

def _get_testfilename():
        return datetime.now().isoformat().replace(':','_')

def test_load():
    """ Test load. """
    img = CImg()
    with pytest.raises(RuntimeError):
        img.load('notexistent.jpg')
    img.load(get_test_image())
    _check_image_dimensions(img)


def test_load_bmp():
    """ Test loading a BMP file. """
    img = CImg()
    img.load_bmp(get_test_image('bmp'))
    _check_image_dimensions(img)

def test_load_jpeg():
    """ Test loading a JPEG file. """
    img = CImg()
    img.load_jpeg(get_test_image('jpg'))
    _check_image_dimensions(img)

def test_load_png():
    """ Test loading a PNG file. """
    img = CImg()
    img.load_png(get_test_image('png'))
    _check_image_dimensions(img)

def test_load_tiff():
    """ Test loading a TIFF file. """
    img = CImg()
    img.load_tiff(get_test_image('tiff'))
    _check_image_dimensions(img)

def test_save():
    """ Test save. """
    img = CImg()
    img.load(get_test_image())
    for ext in ['.bmp', '.jpg', '.png', '.cimg', '.tiff']:
        filename = _get_testfilename() + ext  
        img.save(filename)
        assert os.path.isfile(filename) 
        os.remove(filename)

def test_save_bmp():
    """ Test save bmp. """
    img = CImg((100, 100), dtype=pycimg.uint8)
    img.rand(0, 255)
    filename = _get_testfilename() + '.bmp'
    img.save_bmp(filename)
    assert os.path.isfile(filename)
    os.remove(filename)

def test_save_jpeg():
    """ Test save jpeg. """
    img = CImg((100, 100), dtype=pycimg.uint8)
    img.rand(0, 255)
    filename = _get_testfilename() + '.jpeg'
    img.save_jpeg(filename, quality=80)
    assert os.path.isfile(filename)
    os.remove(filename)

def test_save_png():
    """ Test save png. """
    img = CImg((100, 100), dtype=uint8)
    img.rand(0, 255)
    filename = _get_testfilename() + '.png'
    img.save_png(filename)
    assert os.path.isfile(filename)
    os.remove(filename)

def test_save_tiff():
    """ Test save tiff. """
    img = CImg((100, 100), dtype=uint8)
    img.rand(0, 255)
    filename = _get_testfilename() + '.tiff'
    img.save_tiff(filename)
    assert os.path.isfile(filename)
    os.remove(filename)

def test_save_load():
    """ Test save/load half float. """
    im = CImg()
    arr = np.random.randn(3, 2, 500, 300)
    im.fromarray(arr)
    assert np.allclose(arr, im.asarray())
    filename = _get_testfilename() + '.cimg'  
    im.save(filename)
    im2 = CImg()
    im2.load(filename)
    assert np.allclose(im2.asarray(), im.asarray())
    os.remove(filename)
#        # save/load half float
#       # filename = self._get_testfilename() + '.cimg'  
#       # im.save_cimg_float16(filename)
#       # im3 = CImg()
#       # im3.load_cimg_float16(filename)
#       # self.assertTrue( np.allclose(im2.asarray(), im.asarray()) )
#       # os.remove(filename)
