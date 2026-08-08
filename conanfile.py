'''
You can run the following commands to build and package your project using Conan:
conan create . myproject/1.0.0@ -s build_type=Release
'''
import os
from types import SimpleNamespace
import configparser
import sys
import subprocess

from pathlib import Path
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps, cmake_layout, CMake


class ProjectConan(ConanFile):
    name = "myproject"  # TODO: Insert Project Name Here
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
        # Ensure CMake is available for the build process.
        # self.tool_requires("cmake/3.15.0") # NOTE: If you use the env activations this is already included
        pass

    def layout(self):
        conf_name = os.environ.get(
            "BM_CONFIGURATION", "default").replace(".ini", "")
        cmake_layout(self, build_folder=f"build/{conf_name}")

    def generate(self):
        toolchain = CMakeToolchain(self)
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

        self.__sections = ["execution", "settings"]
        self.__execution_keys = ["action", "depends_on"]
        self.__settings_keys = ["arch", "build_type", "compiler", "compiler.cppstd",
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
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(os.path.dirname(
            __file__), "build_profiles", f"{self.profile_selected}.ini"))

        print(f"Building...{self.profile_selected}")

        self.__validate_config_information()
        self.__load_options_from_config()

        if self.options.action == "build":
            print(
                f"Executing build for profile: {self.profile_selected}")
            self.build(self.profile_selected)
        elif self.options.action == "get_dependencies":
            print(
                f"Getting dependencies for profile: {self.profile_selected}")

        self.build_path = os.path.join(os.path.dirname(__file__), "build")
        from build_helper.package_helper import Package_Helper
        Package_Helper(self)

    def build(self, configuration: str):
        self.__clean()

        profile = self.__create_conan_profile(configuration)

        command = [
            "conan",
            "build",
            str(self.project_dir),
            f"--profile={profile}",
            *self.__conan_toolchain_conf(),
            "--build=missing",
        ]

        print("Running:")
        print(" ".join(command))
        print()

        env = os.environ.copy()
        env["BM_CONFIGURATION"] = configuration
        subprocess.run(command, check=True)

    def __validate_config_information(self):
        # Placeholder for config validation logic
        for section in self.config.sections():
            if section not in self.__sections:
                raise ValueError(f"Invalid section: {section}")
            for key in self.config[section]:
                if key not in getattr(self, f"_BuildMenu__{section}_keys"):
                    raise ValueError(
                        f"Invalid key: {key} in section: {section}")

    def __load_options_from_config(self):
        '''
        Loads the configuration options from the selected build profile into a SimpleNamespace object.
        This allows for easy access to configuration values as attributes.
        '''
        self.options = SimpleNamespace()

        for section in self.config.sections():
            for key, value in self.config.items(section):
                # avoid silent overwrite if same key appears in multiple sections
                if hasattr(self.options, key):
                    raise ValueError(f"Duplicate key across sections: {key}")
                setattr(self.options, key, value)

    def __conan_toolchain_conf(self) -> list[str]:
        import os
        import platform

        conda_prefix = os.environ.get("CONDA_PREFIX")
        if not conda_prefix:
            raise RuntimeError(
                "Activate the Conda environment before building.")

        is_windows = platform.system() == "Windows"
        bin_dir = Path(conda_prefix) / ("Library/bin" if is_windows else "bin")

        def p(name: str) -> str:
            return (bin_dir / name).as_posix()

        if is_windows:
            cc = p("x86_64-w64-mingw32-gcc.exe")
            cxx = p("x86_64-w64-mingw32-g++.exe")
            ar = p("x86_64-w64-mingw32-ar.exe")
            ranlib = p("x86_64-w64-mingw32-ranlib.exe")
        else:
            cc = p("gcc")
            cxx = p("g++")
            ar = p("ar")
            ranlib = p("ranlib")

        compiler_executables = {"c": cc, "cpp": cxx}
        extra_variables = {
            "CMAKE_AR": {"value": ar, "cache": True, "type": "FILEPATH", "force": True},
            "CMAKE_RANLIB": {"value": ranlib, "cache": True, "type": "FILEPATH", "force": True},
        }

        return [
            "-c:h", "tools.cmake.cmaketoolchain:generator=Ninja",
            "-c:h", f"tools.build:compiler_executables={compiler_executables!r}",
            "-c:h", f"tools.cmake.cmaketoolchain:extra_variables={extra_variables!r}",
        ]

    def __clean(self):
        import shutil
        build_dir = Path(self.project_dir) / "build"

        if build_dir.exists():
            print(f"Cleaning {build_dir}")
            shutil.rmtree(build_dir)

    def __create_conan_profile(self, configuration: str) -> Path:
        out_dir = self.project_dir / "build" / ".profiles"
        out_dir.mkdir(parents=True, exist_ok=True)
        profile_path = out_dir / f"{configuration.lower()}.conanprofile"

        lines = ["[settings]"]
        for key, value in self.config.items("settings"):
            lines.append(f"{key}={value}")

        profile_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return profile_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build Menu")
    parser.add_argument("--gui", action="store_true", help="Launch the GUI")
    args = parser.parse_args()

    build_menu = BuildMenu()

    if args.gui:
        build_menu.generate_user_interface()
