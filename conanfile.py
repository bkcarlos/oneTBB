from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps

class OneTBBRecipe(ConanFile):
    name = "onetbb"
    version = "2025.1.5"

    # Optional metadata
    license = "Apache-2.0"
    author = "bkcarlos@outlook.com"
    url = "https://github.com/bkcarlos/onetbb"
    description = "OneTBB for c++"
    topics = ("onetbb", "thread", "threadpool")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "include/*", "src/*", "cmake/*", "test/*", "integration/*", "README.md"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.variables["CMAKE_CXX_STANDARD"] = "17"  # 设置 C++ 标准
        tc.variables["BUILD_TESTS"] = "OFF"         # 设置自定义选项
        tc.variables["TBB4PY_BUILD"] = "OFF"    # 不编译 python 库
        tc.variables["TBB_BUILD"] = "ON"
        tc.variables["TBB_INSTALL"] = "ON"
        tc.variables["BUILD_SHARED_LIBS"] = "ON"
        tc.variables["CMAKE_BUILD_TYPE"] = "Debug"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["onetbb"]
