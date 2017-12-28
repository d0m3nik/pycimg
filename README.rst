.. image:: https://travis-ci.org/d0m3nik/pycimg.svg?branch=master
  :target: https://travis-ci.org/d0m3nik/pycimg
  :alt: Travis Status
.. image:: https://ci.appveyor.com/api/projects/status/github/d0m3nik/pycimg?branch=master&svg=true
  :target: https://ci.appveyor.com/project/d0m3nik/pycimg
  :alt: AppVeyor Status
.. image:: https://coveralls.io/repos/github/d0m3nik/pycimg/badge.svg?branch=HEAD
  :target: https://coveralls.io/github/d0m3nik/pycimg?branch=HEAD
  :alt: Coverage Status
.. image:: https://readthedocs.org/projects/pycimg/badge/?version=latest
  :target: http://pycimg.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

README
======
**pycimg** is a python extension for the CImg_ library.

The package contains a single class CImg that provides access to the
image processing methods of the CImg_ library. 

Pixel data of CImg objects can be accessed as a numpy_ array.

Vice versa new CImg objects can be created from pixel data in a numpy_ array 
or a image file. Supported file formats are png_, jpeg_, tiff_, bmp, and cimg.

.. code-block:: python

     from pycimg import CImg
     import numpy as np

     # Load image from file
     img = CImg('test/test.png')
     img.display()

     # Access pixel data as numpy array
     arr = img.asarray()
     # Set pixels in upper left 100 x 100 px rectangle
     arr[:,:,0:99,0:99] = 0
     # Pixel data is shared with the image instance
     img.display()

     # Create image from numpy array
     img = CImg(np.random.randn(100,100))

Features
--------
- Access pixel data as a numpy_ array.
- Builtin support for reading/writing png_, jpeg_, and tiff_ image formats.

Installation
------------
Install pycimg by running:

.. code-block:: bash

   pip install pycimg

Documentation
-------------
See readthedocs_.

License
-------
The project is licensed under the GPL3 license.

TODO
----
- [x] Setup PyPI distribution
- [x] Support numpy array interface
- [] Test package with tox
- [] Add more unit tests
- [] Operator overloads
- [] Colorspace methods
- [] Add tutorial
- [] Add support for different Mac OS X versions
- [] Support python2.7, 3.4, 3.5, 3.6

.. _CImg: http://www.cimg.eu
.. _numpy: http://www.numpy.org/
.. _jpeg: https://github.com/libjpeg-turbo/libjpeg-turbo
.. _png: https://github.com/glennrp/libpng/
.. _tiff: https://gitlab.com/libtiff/libtiff
.. _readthedocs: http://pycimg.readthedocs.io/en/latest/ 
