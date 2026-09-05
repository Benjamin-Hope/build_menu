import subprocess
import os
from pathlib import Path
from types import SimpleNamespace


class BuildHelper:
    def __init__(self, cls):
        self.__cls = cls
        self.timer_ms = 250

    def build(self, configuration: str):
        self.__clean()

        profile = self.__create_conan_profile(configuration)

        command = [
            "conan",
            "build",
            str(self.__cls.project_dir),
            f"--profile={profile}",
            *self.__conan_toolchain_conf(),
            "--build=missing",
            "-c", f"user.project:build_target_path={configuration}",
        ]

        print("Running:")
        print(" ".join(command))
        print()

        process = subprocess.Popen(
            command,
            cwd=self.__cls.project_dir,
            stdout=None,
            stderr=None,
            text=True
        )

        self.__monitor_process_output(configuration, process)

    def build_test(self, configuration: str):
        self.__clean()

        profile = self.__create_conan_profile(configuration)

        command = [
            "conan",
            "build",
            str(self.__cls.project_dir),
            f"--profile={profile}",
            *self.__conan_toolchain_conf(),
            "--build=missing",
            "-c", f"user.project:build_target_path={configuration}",
            "-c", "user.project:unit_test=True",
        ]

        print("Running:")
        print(" ".join(command))
        print()

        process = subprocess.Popen(
            command,
            cwd=self.__cls.project_dir,
            stdout=None,
            stderr=None,
            text=True
        )

        self.__monitor_process_output(configuration, process)

    def __monitor_process_output(self, configuration, process):
        # Check process output every x milliseconds
        self.__cls.app.register_process(configuration, process)
        self.__cls.app.after(
            self.timer_ms, self.__cls.app.check_process_output)

    def _validate_config_information(self):
        # Placeholder for config validation logic
        for section in self.__cls.config.sections():
            if section not in self.__cls.sections:
                raise ValueError(f"Invalid section: {section}")
            for key in self.__cls.config[section]:
                if key not in getattr(self.__cls, f"{section}_keys"):
                    raise ValueError(
                        f"Invalid key: {key} in section: {section}")

    def _load_options_from_config(self):
        '''
        Loads the configuration options from the selected build profile into a SimpleNamespace object.
        This allows for easy access to configuration values as attributes.
        '''
        self.options = SimpleNamespace()

        for section in self.__cls.config.sections():
            for key, value in self.__cls.config.items(section):
                import platform
                if (key == "os") and (value != platform.system()):
                    print(
                        f"Warning! OS COnfiguration '{value}' do not match the actual OS '{platform.system()}'")
                # avoid silent overwrite if same key appears in multiple sections
                if hasattr(self.options, key):
                    raise ValueError(f"Duplicate key across sections: {key}")
                setattr(self.options, key, value)

    def __conan_toolchain_conf(self) -> list[str]:
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

        compiler_executables = {"c": cc, "cpp": cxx}
        if is_windows:
            extra_variables = {
                "CMAKE_AR": {"value": ar, "cache": True, "type": "FILEPATH", "force": True},
                "CMAKE_RANLIB": {"value": ranlib, "cache": True, "type": "FILEPATH", "force": True},
            }

            return [
                "-c:h", "tools.cmake.cmaketoolchain:generator=Ninja",
                "-c:h", f"tools.build:compiler_executables={compiler_executables!r}",
                "-c:h", f"tools.cmake.cmaketoolchain:extra_variables={extra_variables!r}",
            ]
        else:
            return [
                "-c:h", "tools.cmake.cmaketoolchain:generator=Ninja",
                "-c:h", f"tools.build:compiler_executables={compiler_executables!r}",
            ]

    def __clean(self):
        import shutil
        build_dir = Path(self.__cls.project_dir) / "build"

        if build_dir.exists():
            print(f"Cleaning {build_dir}")
            shutil.rmtree(build_dir)

    def __create_conan_profile(self, configuration: str) -> Path:
        out_dir = self.__cls.project_dir / "build" / ".profiles"
        out_dir.mkdir(parents=True, exist_ok=True)
        profile_path = out_dir / f"{configuration.lower()}.conanprofile"

        lines = ["[settings]"]
        for key, value in self.__cls.config.items("settings"):
            import platform
            if (key == "os") and (value != platform.system()):
                print("Attempting to force os configuration fix")
                print(f'key {key}:{value} -> {key}:{platform.system()}')
                value = platform.system()
            lines.append(f"{key}={value}")

        profile_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return profile_path
