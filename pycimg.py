__version__ = "0.0.6"

from cimg_bindings import CImg_float

class CImg:

    def __init__(self):
        self._cimg = CImg_float()

    def __getattr__(self, name):
        return getattr(self._cimg, name)