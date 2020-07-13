import unittest
import os
import numpy as np
from datetime import datetime
from context import cimg, CImg, get_test_image

class TestIO(unittest.TestCase):

    def _get_testfilename(self):
        return datetime.now().isoformat().replace(':','_')

    def _check_image_dimensions(self, im):
        self.assertEqual(im.width, 1200)
        self.assertEqual(im.height, 797)
        self.assertEqual(im.depth, 1)
        self.assertEqual(im.spectrum, 3)

    def test_load(self):
        """ Test load. """
        img = CImg()
        self.assertRaises(RuntimeError, img.load, 'notexistent.jpg')
        img.load(get_test_image())
        self._check_image_dimensions(img)

    def test_load_bmp(self):
        """ Test loading a BMP file. """
        img = CImg()
        img.load_bmp(get_test_image('bmp'))
        self._check_image_dimensions(img)

    def test_load_jpeg(self):
        """ Test loading a JPEG file. """
        img = CImg()
        img.load_jpeg(get_test_image('jpg'))
        self._check_image_dimensions(img)

    def test_load_png(self):
        """ Test loading a PNG file. """
        img = CImg()
        img.load_png(get_test_image('png'))
        self._check_image_dimensions(img)

    def test_load_tiff(self):
        """ Test loading a TIFF file. """
        img = CImg()
        img.load_tiff(get_test_image('tiff'))
        self._check_image_dimensions(img)

    def test_save(self):
        """ Test save. """
        img = CImg()
        img.load(get_test_image())
        for ext in ['.bmp', '.jpg', '.png', '.cimg', '.tiff']:
            filename = self._get_testfilename() + ext  
            img.save(filename)
            self.assertTrue( os.path.isfile(filename) )
            os.remove(filename)

    def test_save_bmp(self):
        """ Test save bmp. """
        img = CImg((100, 100), dtype=cimg.uint8)
        img.rand(0, 255)
        filename = self._get_testfilename() + '.bmp'
        img.save_bmp(filename)
        self.assertTrue(os.path.isfile(filename))
        os.remove(filename)

    def test_save_jpeg(self):
        """ Test save jpeg. """
        img = CImg((100, 100), dtype=cimg.uint8)
        img.rand(0, 255)
        filename = self._get_testfilename() + '.jpeg'
        img.save_jpeg(filename, quality=80)
        self.assertTrue(os.path.isfile(filename))
        os.remove(filename)

    def test_save_png(self):
        """ Test save png. """
        img = CImg((100, 100), dtype=cimg.uint8)
        img.rand(0, 255)
        filename = self._get_testfilename() + '.png'
        img.save_png(filename)
        self.assertTrue(os.path.isfile(filename))
        os.remove(filename)

    def test_save_tiff(self):
        """ Test save tiff. """
        img = CImg((100, 100), dtype=cimg.uint8)
        img.rand(0, 255)
        filename = self._get_testfilename() + '.tiff'
        img.save_tiff(filename, compression_type=cimg.C_LZW, voxel_size=0, description="Test tiff")
        self.assertTrue(os.path.isfile(filename))
        os.remove(filename)


    def test_save_load(self):
        """ Test save/load half float. """
        im = CImg()
        arr = np.random.randn(3, 2, 500, 300)
        im.fromarray(arr)
        self.assertTrue( np.allclose(arr, im.asarray()) )
        filename = self._get_testfilename() + '.cimg'  
        im.save(filename)
        im2 = CImg()
        im2.load(filename)
        self.assertTrue( np.allclose(im2.asarray(), im.asarray()) )
        os.remove(filename)
        # save/load half float
        #filename = self._get_testfilename() + '.cimg'  
        #im.save_cimg_float16(filename)
        #im3 = CImg()
        #im3.load_cimg_float16(filename)
        #self.assertTrue( np.allclose(im2.asarray(), im.asarray()) )
        #os.remove(filename)

if __name__ == '__main__':
    unittest.main() 
            
