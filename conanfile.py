'''
You can run the following commands to build and package your project using Conan:
conan create . myproject/1.0.0@ -s build_type=Release
'''

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout


class ProjectConan(ConanFile):
    name = "myproject"  # TODO: Insert Project Name Here
    version = "1.0.0"  # TODO: Insert Project Version Here
    # TODO: Change to "application" if this is an executable project
    package_type = "library"

    # TODO: Add any additional settings, options, or requirements as needed
    # Conan builds different binaries for different settings, so you need to specify which settings your project supports. (Windows, Linux, MacOS, etc.)
    settings = "os", "compiler", "build_type", "arch"

    # These instruct Conan to generate helper files for CMake.
    generators = "CMakeDeps", "CMakeToolchain"

    exports_sources = (
        "CMakeLists.txt",
        "src/*",
        "include/*",
    )

    def requirements(self):
        # TODO: Add any additional dependencies your project requires
        # Find the available versions in conan by writing "conan search <package_name> -r conan-center" in the terminal.
        self.requires("fmt/11.1.3")
        # self.requires("spdlog/1.15.0")

    def layout(self):
        cmake_layout(self)  # Defines the folder structure.

    # This method is called to generate the build system files (CMake in this case).
    def generate(self):
      # This allows Cmake to find the dependencies automatically
        tc = CMakeToolchain(self)
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        ''' Equivalent as running:
          cmake -S . -B build
          cmake --build build
        '''
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # Packages the build artifacts into Conan's package directory.
        # Assuming install rules are difined in CMakeLists.txt, this will copy the necessary files to the package folder.
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        # This method defines the information about the package, such as libraries to link against.
        self.cpp_info.libs = ["myproject"]
