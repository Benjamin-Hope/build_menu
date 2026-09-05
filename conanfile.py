'''
You can run the following commands to build and package your project using Conan:
conan create . project/1.0.0@ -s build_type=Release
'''
import os

import configparser
import sys
import subprocess

from pathlib import Path
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps, cmake_layout, CMake
from conan.tools.files import copy


class ProjectConan(ConanFile):
    name = "project"  # TODO: Insert Project Name Here
    version = "1.0.0"  # TODO: Insert Project Version Here

    package_type = "application"

    # TODO: Add any additional settings, options, or requirements as needed
    # Conan builds different binaries for different settings, so you need to specify which settings your project supports. (Windows, Linux, MacOS, etc.)
    settings = "os", "compiler", "build_type", "arch"

    def requirements(self):
        # TODO: Add any additional dependencies your project requires
        # Find the available versions in conan by writing "conan search <package_name> -r conan-center" in the terminal.
        self.requires("fmt/11.1.4")

    def build_requirements(self):
        if self.conf.get("user.project:unit_test", default=False):
            self.test_requires("gtest/1.15.0")
        # Ensure CMake is available for the build process.
        # self.tool_requires("cmake/3.15.0") # NOTE: If you use the env activations this is already included

    def layout(self):
        conf_name = self.conf.get(
            "user.project:build_target_path", default="fallback", check_type=str)

        cmake_layout(self, build_folder=f"build/{conf_name}")

    def generate(self):
        toolchain = CMakeToolchain(self)

        unit_test = self.conf.get(
            "user.project:unit_test",
            False
        )
        toolchain.variables["UNIT_TEST"] = 1 if unit_test else 0
        toolchain.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def configure(self):
        # This method can be used to configure settings or options before the build process.
        # For example, you can set options for dependencies here.
        pass

    def build(self):
        ''' Equivalent as running:
          cmake -S . -B build
          cmake --build build
        '''
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

        if self.conf.get("user.project:unit_test", False):
            cmake.test()

    def package(self):
        # Packages the build artifacts into Conan's package directory.
        # Assuming install rules are defined in CMakeLists.txt, this will copy the necessary files to the package folder.
        cmake = CMake(self)
        cmake.install()


class BuildMenu:
    """Convenience wrapper around the Conan CLI."""

    def __init__(self):
        self.project_dir = Path(__file__).resolve().parent
        # TODO: Change to the directory where your build profiles are located
        self.profile_dir = Path(self.project_dir) / "build_profiles"
        # Below are the allowed config options for the build profiles

        self.sections = ["execution", "settings"]
        self.execution_keys = ["action", "depends_on"]
        self.settings_keys = ["arch", "build_type", "compiler", "compiler.cppstd",
                              "compiler.libcxx", "compiler.version", "os"]

    def generate_user_interface(self):
        # Import the GUI module here to avoid circular imports
        features_path = os.path.join(os.path.dirname(__file__))
        sys.path.append(features_path)

        from build_helper.gui.interface import BuildGUI
        self.app = BuildGUI(features_path)
        self.app.fill_menu_items("EXECUTE", self.execute)
        self.app.mainloop()

    def execute(self):
        self.profile_selected = self.app.get_selected_profile()

        if self.profile_selected is None:
            return

        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(
            __file__), "build_profiles", f"{self.profile_selected}.ini"))

        print(f"Building...{self.profile_selected}")

        from build_helper.build_helper import BuildHelper
        self.BuildHelper = BuildHelper(self)

        self.BuildHelper._validate_config_information()
        self.BuildHelper._load_options_from_config()

        self.options = self.BuildHelper.options

        if self.options.action == "build":
            print(
                f"Executing build for profile: {self.profile_selected}")
            self.BuildHelper.build(self.profile_selected)

        if self.options.action == "unit_test":
            print(
                f"Executing build for profile: {self.profile_selected}")
            self.BuildHelper.build_test(self.profile_selected)

        if self.options.action == "get_dependencies":
            print(
                f"Getting dependencies for profile: {self.profile_selected}")

        self.build_path = os.path.join(os.path.dirname(__file__), "build")
        from build_helper.package_helper import Package_Helper
        Package_Helper(self)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build Menu")
    parser.add_argument("--gui", action="store_true", help="Launch the GUI")
    args = parser.parse_args()

    build_menu = BuildMenu()

    if args.gui:
        build_menu.generate_user_interface()
