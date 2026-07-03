import os


class Package_Helper:
    def __init__(self, cls):
        self.__cls = cls
        self.__generate_package()

    def __generate_package(self):
        self.build_path = os.path.join(
            self.__cls.build_path,
            self.__cls.profile_selected
        )

        if not os.path.exists(self.build_path):
            os.makedirs(self.build_path)
            print(f"Created build directory: {self.build_path}")
