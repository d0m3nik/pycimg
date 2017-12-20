import unittest
import numpy as np
from context import cimg, CImg, get_test_image


class TestDrawing(unittest.TestCase):

    def test_draw_rectangle(self):
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
        self.assertEqual(img, img_expected)

    def test_draw_polygon(self):
        """ Test draw polygon. """
        img = CImg((5, 5), dtype=cimg.uint8)
        img.fill(0)
        points = np.array([(2, 0), (4, 2), (2, 4), (0, 2)])
        img.draw_polygon(points, 255)
#        img.save('poly.png')
        arr = np.array([[0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1],
                        [0, 1, 1, 1, 0],
                        [0, 0, 1, 0, 0]])*255
        img_expected = CImg(arr, dtype=cimg.uint8)
#        img_expected.save('poly2.png')
        self.assertEqual(img, img_expected)

    def test_draw_circle(self):
        """ Test draw circle. """
        img = CImg(np.zeros((10, 10)), dtype=cimg.uint8)
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
        img_expected = CImg(arr, dtype=cimg.uint8)
        self.assertEqual(img, img_expected)
        with self.assertRaises(RuntimeError):
            img.draw_circle(4, 4, 2, [255, 0, 0])

    def test_draw_triangle(self):
        """ Test draw triangle. """
        img = CImg((5,5))
        img.fill(0)
        img.draw_triangle(0, 0, 0, 4, 2, 2, 255)
        img_expected = CImg(np.array([[1, 0, 0, 0, 0],
                                      [1, 1, 0, 0, 0],
                                      [1, 1, 1, 0, 0],
                                      [1, 1, 0, 0, 0],
                                      [1, 0, 0, 0, 0]])*255)
        self.assertEqual(img, img_expected)

    def test_draw_text(self):
        """ Test draw text. """
        img = CImg((10, 10))
        img.draw_text(0, 0, 'A', 1, 0)
        img_expected = CImg(np.array(
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 1, 0, 0, 0, 0]]))
        self.assertEqual(img, img_expected)

if __name__ == '__main__':
    unittest.main() 
            
