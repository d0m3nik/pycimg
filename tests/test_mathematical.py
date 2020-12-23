from context import * 
import numpy as np

def test_sqr():
    arr = np.random.randn(10, 5)
    img = CImg(arr)
    assert np.allclose( arr*arr, img.sqr().asarray() )

def test_sqrt():
    arr = np.ones((10, 5))
    img = CImg(arr)
    assert np.allclose( arr, img.sqrt().asarray() )

def test_exp():
    arr = np.random.randn(10, 5)
    img = CImg(arr)
    assert np.allclose( np.exp(arr), img.exp().asarray() )

def test_log():
    exponents = np.linspace(-10, 10, 11)
    arr = (np.e * np.ones((1,11)))**exponents
    img = CImg(arr)
    assert np.allclose( exponents, img.log().asarray() )

def test_log2():
    exponents = np.linspace(-10, 10, 11)
    arr = (2* np.ones((1,11)))**exponents
    img = CImg(arr)
    assert np.allclose( exponents, img.log2().asarray() ) 

def test_log10():
    exponents = np.linspace(-10, 10, 11)
    arr = (10* np.ones((1,11)))**exponents
    img = CImg(arr)
    assert np.allclose( exponents, img.log10().asarray() ) 

def test_abs():
    arr = np.random.randn(10, 5)
    img = CImg(arr)
    assert np.allclose( np.abs(arr), img.abs().asarray() ) 

def test_sign():
    arr = np.random.randn(10, 5)
    img = CImg(arr)
    assert np.allclose( np.sign(arr), img.sign().asarray() )

def test_cos():
    arr = np.ones((10, 5))
    img = CImg(arr)
    assert np.allclose( np.cos(arr), img.cos().asarray() )

def test_sin():
    arr = np.random.randn(10, 5)
    img = CImg(arr)
    assert np.allclose( np.sin(arr), img.sin().asarray() )

def test_sinc():
    arr  = np.linspace(-10, 10, 100)
    img = CImg(arr)
    assert np.allclose( np.sinc(arr/np.pi), img.sinc().asarray() )

def test_tan():
    arr = np.linspace(-0.5, 0.5, 100)
    img = CImg(arr)
    assert np.allclose( np.tan(arr), img.tan().asarray() )

def test_sinh():
    arr = np.random.randn(10, 5)
    img = CImg(arr)
    assert np.allclose( np.sinh(arr), img.sinh().asarray() )

def test_tanh():
    arr = np.random.randn(10, 5)
    img = CImg(arr)
    assert np.allclose( np.tanh(arr), img.tanh().asarray() )

def test_acos():
    arr = -np.ones((10, 5))
    img = CImg(arr)
    assert np.allclose( np.arccos(arr), img.acos().asarray() )

def test_asin():
    arr = [-0.99, -0.5, 0, 0.5, 0.99]
    img = CImg(arr)
    assert np.allclose( np.arcsin(arr), img.asin().asarray() )

def test_atan():
    arr = np.random.randn(10, 5)
    img = CImg(arr)
    assert np.allclose( np.arctan(arr), img.atan().asarray() )

def test_atan2():
    """ Test atan2. """
    x = np.random.rand(5, 2)
    y = np.random.rand(5, 2)
    img1 = CImg(y, dtype=float64)
    img2 = CImg(x, dtype=float64)
    delta = np.abs(img1.atan2(img2).asarray() - np.arctan2(y, x))
    assert np.allclose(delta, np.zeros((5, 2)))

def test_mul():
    """ Test mul. """
    x = np.ones((5, 4))*2
    y = np.ones((5, 4))*3
    img_x = CImg(x)
    img_y = CImg(y)
    img_x.mul(img_y)
    img_expected = CImg(x*y)
    assert img_x == img_expected

def test_div():
    """ Test div. """
    x = np.ones((5, 4))*2
    y = np.ones((5, 4))*3
    img_x = CImg(x)
    img_y = CImg(y)
    img_x.div(img_y)
    img_expected = CImg(x/y)
    assert img_x == img_expected

def test_pow():
    """ Test pow. """
    x = np.ones((7, 3))*2
    img = CImg(x)
    img.pow(3)
    img_expected = CImg(x**3)
    assert img == img_expected

def test_min_max():
    """ Test min_max. """
    img = CImg(np.array([[2, -1],[0, 4]]))
    assert img.min_max() == (-1, 4)

def test_max_min():
    """ Test max_min. """
    img = CImg(np.array([[2, -1],[0, 4]]))
    assert img.max_min() == (4, -1)

def test_kth_smallest():
    """ Test kth smallest. """
    img = CImg(np.array([[2, -1], [0, 4]]))
    assert img.kth_smallest(0) ==  -1
    assert img.kth_smallest(1) ==  0
    assert img.kth_smallest(2) ==  2
    assert img.kth_smallest(3) ==  4

def test_variance():
    """ Test variance. """
    img = CImg(np.array([[2, -5], [0, 3]]))
    assert img.variance() == 38.0/3.0

def test_variance_mean():
    """ Test variance + mean. """
    img = CImg(np.array([[2, -5], [0, 3]]))
    assert img.variance_mean() == (38.0/3.0, 0)

def test_variance_noise():
    """ Test variance noise. """
    pass

def test_mse():
    """ Test MSE. """
    img1 = CImg(np.array([[2, -5], [0, 3]]))
    img2 = CImg(np.array([[2, -3], [0, 3]]))
    assert img1.mse(img2) == 1.0

def test_psnr():
    """ Test PSNR. """
    pass

def test_magnitude():
    """ Test magnitude. """
    img = CImg(np.array([[2, -5], [0, 3]]))
    assert img.magnitude(L1_NORM) == 10

def test_dot():
    """ Test dot. """
    img1 = CImg(np.array([[2, -5], [0, 3]]))
    img2 = CImg(np.array([[2, -3], [0, 3]]))
    assert img1.dot(img2) == 28
