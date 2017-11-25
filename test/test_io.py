import unittest
import os
import numpy as np
from datetime import datetime
from context import cimg, CImg, get_test_image

class TestIO(unittest.TestCase):

    def _get_testfilename(self):
        return datetime.now().isoformat().replace(':','_')

    def test_load(self):
        im = CImg()
        self.assertRaises(RuntimeError, im.load, 'notexistent.jpg')
        im.load(get_test_image())
        self.assertEqual(im.width, 640)
        self.assertEqual(im.height, 426)
        self.assertEqual(im.depth, 1)
        self.assertEqual(im.spectrum, 3)

    def test_save(self):
        im = CImg()
        im.load(get_test_image())
        for ext in ['.jpg', '.png', '.cimg']:
            filename = self._get_testfilename() + ext  
            im.save(filename)
            self.assertTrue( os.path.isfile(filename) )
            os.remove(filename)

    def test_save_load(self):
        im = CImg()
        arr = np.random.randn(3, 2, 500, 300)
        im.fromarray(arr)
        self.assertTrue( np.allclose(arr, im.asarray()) )
        filename = self._get_testfilename() + '.cimg'  
        im.save(filename)
        im2 = CImg()
        im2.load(filename)
        self.assertTrue( np.allclose(im2.asarray(), im.asarray()) )
        # save/load half float
        filename = self._get_testfilename() + '.cimg'  
        im.save_cimg_float16(filename)
        im3 = CImg()
        im3.load_cimg_float16(filename)
        self.assertTrue( np.allclose(im2.asarray(), im.asarray()) )

if __name__ == '__main__':
    unittest.main() 
            
