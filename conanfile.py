from conans import ConanFile

class PyCimgConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "json"

    def requirements(self):
        self.requires('libtiff/4.4.0')
        self.requires('libpng/1.6.38')
        self.requires('libjpeg/9e')
