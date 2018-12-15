import os
import sys
import pycimg as cimg
from pycimg import CImg

def get_test_image(ext=None):
    if ext == None:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), './test.jpg'))
    return os.path.abspath(os.path.join(os.path.dirname(__file__), './test.' + ext))
