from conans import ConanFile

class PyCimgConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "json"

    def requirements(self):
        self.requires('libtiff/4.0.9@bincrafters/stable')
        self.requires('libpng/1.6.37@bincrafters/stable')
        if self.settings.os == "Linux" and self.settings.arch == "x86":
            self.requires('libjpeg/9c@bincrafters/stable')
        else:
            self.requires('libjpeg-turbo/2.0.2@bincrafters/stable')
