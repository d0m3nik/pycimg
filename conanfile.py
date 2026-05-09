from conan import ConanFile

class PyCimgConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain", "VirtualBuildEnv"

    def requirements(self):
        self.requires('libtiff/4.7.1')
        self.requires('libpng/1.6.58')
        self.requires('libjpeg/9f')
        self.requires('zlib/1.3.1')
