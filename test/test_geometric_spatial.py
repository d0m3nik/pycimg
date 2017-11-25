import unittest
from context import cimg, CImg, get_test_image

class TestGeometricSpatial(unittest.TestCase):

    def test_resize(self):
        im = CImg()
        im.load(get_test_image())
        im.resize(100, 50)
        self.assertEqual(im.width, 100)
        self.assertEqual(im.height, 50)
        self.assertEqual(im.depth, 1)
        self.assertEqual(im.spectrum, 3)
        self.assertEqual(im.shape, (3, 1, 50, 100))

if __name__ == '__main__':
    unittest.main() 
            
