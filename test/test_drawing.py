import unittest
import numpy as np
from context import cimg, CImg, get_test_image

class TestDrawing(unittest.TestCase):

    def test_draw_rectangle(self):
        im = CImg((5,5))
        im.draw_rectangle(1, 1, 4, 4, [255])
        arr = im.asarray().squeeze()
        print(arr)

    def test_draw_polygon(self):
        im = CImg(get_test_image())
        points = np.array([(0,0),(100,0),(100,100)])
        im.draw_polygon(points, [255,255,255])
#        im.save('poly.png')
        self.assertEqual(im.shape, (3, 1, 426, 640))

    def test_draw_circle(self):
        im = CImg(np.zeros((10,10)), dtype=cimg.uint8)
        im.draw_circle(5, 5, 2, [255])
        im.save('circle.png')

if __name__ == '__main__':
    unittest.main() 
            
