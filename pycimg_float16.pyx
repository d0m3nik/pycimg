cdef class CImg_float16(CImg_float32):

    def __cinit__(self, filename):
        byte_string = filename.encode('UTF-8')
        cdef char* fn = byte_string
        # Loads single precision image from half
        # precision one.
        self._cimg = from_float16(fn)
