from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import get, copy, collect_libs
from conan.tools.build import check_min_cppstd
import os


class TinySAKConan(ConanFile):
    name = "tinySAK"
    description = "Tiny SAK forked from doubango"
    license = "GNU Public License or the Artistic License"
    homepage = "https://github.com/DoubangoTelecom/doubango"
    url = "https://github.com/conan-io/conan-center-index"
    topics = ("im", "nim", "nertc", "netease im", "netease")
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True
    }
    short_paths = True

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CMAKE_BUILD_TYPE"] = "Release" if self.settings.build_type == "Release" else "Debug"
        tc.variables["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        src_lib_folder = os.path.join(self.source_folder)
        dst_lib_folder = os.path.join(self.package_folder, "lib")
        src_include_folder = os.path.join(self.source_folder, "src")
        dst_include_folder = os.path.join(self.package_folder, "include")
        if self.settings.os == "Windows":
            copy(self, "*.lib", dst=dst_lib_folder, src=src_lib_folder, keep_path=False)
        if self.settings.os in ["Linux", "Macos"]:
            copy(self, "*.a", dst=dst_lib_folder, src=src_lib_folder, keep_path=False)
        copy(self, "*.h", dst=dst_include_folder, src=src_include_folder)

    def package_info(self):
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = collect_libs(self)
