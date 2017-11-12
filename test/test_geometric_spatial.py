import unittest
import os
from datetime import datetime
from context import CImg

class TestGeometricSpatial(unittest.TestCase):

    def test_resize(self):
        im = CImg()
        im.load('test.jpg')
        im.resize(100, 50)
        self.assertEqual(im.width(), 100)
        self.assertEqual(im.height(), 50)
        self.assertEqual(im.depth(), 1)
        self.assertEqual(im.spectrum(), 3)

if __name__ == '__main__':
    unittest.main() 
            
