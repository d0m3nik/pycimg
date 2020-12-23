import numpy as np
import pytest
from context import * 

def test_draw_rectangle():
    """ Test draw rectangle."""
    img = CImg((5, 5))
    img.draw_rectangle(1, 1, 4, 4, 255)
    arr = np.array([[0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1],
                    [0, 1, 1, 1, 1],
                    [0, 1, 1, 1, 1],
                    [0, 1, 1, 1, 1]])*255
    img_expected = CImg(arr)
    arr = img.asarray().squeeze()
    assert img == img_expected

def test_draw_polygon():
    """ Test draw polygon. """
    img = CImg((5, 5), dtype=uint8)
    img.fill(0)
    points = np.array([(2, 0), (4, 2), (2, 4), (0, 2)]).transpose()
    img.draw_polygon(points, 255)
    arr = np.array([[0, 0, 1, 0, 0],
                    [0, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1],
                    [0, 1, 1, 1, 0],
                    [0, 0, 1, 0, 0]])*255
    img_expected = CImg(arr, dtype=uint8)
    print(img.asarray())
    assert img == img_expected

def test_draw_circle():
    """ Test draw circle. """
    img = CImg(np.zeros((10, 10)), dtype=uint8)
    img.draw_circle(4, 4, 2, [255])
    img.save('circle.png')
    arr = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    ])*255
    img_expected = CImg(arr, dtype=uint8)
    assert img == img_expected
    with  pytest.raises(RuntimeError):
        img.draw_circle(4, 4, 2, [255, 0, 0])

def test_draw_triangle():
    """ Test draw triangle. """
    img = CImg((5,5))
    img.fill(0)
    img.draw_triangle(0, 0, 0, 4, 2, 2, 255)
    img_expected = CImg(np.array([[1, 0, 0, 0, 0],
                                  [1, 1, 0, 0, 0],
                                  [1, 1, 1, 0, 0],
                                  [1, 1, 0, 0, 0],
                                  [1, 0, 0, 0, 0]])*255)
    assert img == img_expected

def test_draw_text():
    """ Test draw text. """
    img = CImg((10, 10))
    img.draw_text(0, 0, 'A', 1, 0)
    img_expected = CImg(np.array(
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
     [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 1, 0, 0, 0]]))
    assert img == img_expected
