import unittest
import numpy as np
from context import cimg, CImg, get_test_image


class TestInstanceCharacteristics(unittest.TestCase):

    def test_linear_atXY(self):
        ia = CImg((2,2))
        # Create simple 2x2 checkerboard
        arr = ia.asarray()
        arr[0,0,0,1] = 1
        arr[0,0,1,1] = 1
        ia.resize(4, 4, interpolation_type=cimg.LINEAR)

        ib = CImg((2,2))
        arr = ib.asarray()
        arr[0,0,0,1] = 1
        arr[0,0,1,1] = 1
        sc = (2-1)/(4-1)
        ic = CImg((4,4))
        arr = ic.asarray()
        for x in range(ic.width):
            for y in range(ic.height):
                arr[0,0,y,x] = ib.linear_atXY(sc*x, sc*y, 0, 0)

        self.assertTrue( np.allclose( ia.asarray(), ic.asarray() ))

if __name__ == '__main__':
    unittest.main() 
            
