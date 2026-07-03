import os
import sys
import configparser
from types import SimpleNamespace


class BuildMenu:
    def __init__(self):
        # Below are the allowed config options for the build profiles
        self.__sections = ["execution", "settings"]
        self.__keys = ["action", "name", "depends_on"]

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
        elif self.options.action == "get_dependencies":
            print(
                f"Getting dependencies for profile: {self.profile_selected}")

        self.build_path = os.path.join(os.path.dirname(__file__), "build")

        from build_helper.package_helper import Package_Helper
        Package_Helper(self)

    def __validate_config_information(self):
        # Placeholder for config validation logic
        for section in self.config.sections():
            if section not in self.__sections:
                raise ValueError(f"Invalid section: {section}")
            for key in self.config[section]:
                if key not in self.__keys:
                    raise ValueError(
                        f"Invalid key: {key} in section: {section}")

    def __load_options_from_config(self):
        self.options = SimpleNamespace()

        for section in self.config.sections():
            for key, value in self.config.items(section):
                # avoid silent overwrite if same key appears in multiple sections
                if hasattr(self.options, key):
                    raise ValueError(f"Duplicate key across sections: {key}")
                setattr(self.options, key, value)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build Menu")
    parser.add_argument("--gui", action="store_true", help="Launch the GUI")
    args = parser.parse_args()

    build_menu = BuildMenu()

    if args.gui:
        build_menu.generate_user_interface()
