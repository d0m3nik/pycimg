import unittest
import os
from datetime import datetime
from context import CImg

class TestIO(unittest.TestCase):

    def test_load(self):
        im = CImg()
        self.assertRaises(RuntimeError, im.load, 'notexistent.jpg')
        im.load('test.jpg')
        self.assertEqual(im.width(), 640)
        self.assertEqual(im.height(), 426)
        self.assertEqual(im.depth(), 1)
        self.assertEqual(im.spectrum(), 3)

    def test_save(self):
        im = CImg()
        im.load('test.jpg')
        for ext in ['.jpg', '.png', '.cimg']:
            filename = datetime.now().isoformat() + ext  
            print(filename)
            im.save(filename)
            self.assertTrue( os.path.isfile(filename) )
            os.remove(filename)

if __name__ == '__main__':
    unittest.main() 
            
