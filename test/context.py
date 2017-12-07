import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cimg as cimg
from cimg import CImg

def get_test_image(ext=None):
    if ext == None:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), './test.jpg'))
    return os.path.abspath(os.path.join(os.path.dirname(__file__), './test.' + ext))
