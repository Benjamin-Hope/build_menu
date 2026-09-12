# Update Setup

Depending on your project you might consider changing the default setup to better match your needs.

## Packages

You can add required conan packages by changing the _.environment\conda_env.yaml_ file. You can check the available packages from the mini-forge package page in [Conda Forge Packages List](https://conda-forge.org/packages/).

Once you have updated your configuration run the environment activation script again to update the installed packages in your environment by `source activate_conda_env.sh` or `.\activate_conda_env.bat`.

## C and C++ Packages Installation

As mentioned before the conan is meant to facilitate C and C++ development by providing already compiled and packaged libraries. You can add the required C and C++ libraries by changing the `requirements()` function in the `conanfile.py`. The example below demonstrates how to add the **fmt** library.

```py
    def requirements(self):
        # TODO: Add any additional dependencies your project requires
        # Find the available versions in conan by writing "conan search <package_name> -r conan-center" in the terminal.
        self.requires("fmt/11.1.4")
```

You can check the available packages in the conan center by running `conan search <package_name> -r conan-center` in the activated environment terminal.

Note, that this `requirements()` section is meant to define packages needed in your code, not requirements needed for the build or packaging.

## In Depth Conan

If you would like to have a better understanding of how conan works please refer to their official page and documentation available in [Conan Home Page](https://conan.io).

## Add and setup build configuration files

You can add a new and customize your own build profile according to your needs. Lets take one as example:

```yaml
[settings]
arch=x86_64
build_type=Debug
compiler=gcc
compiler.cppstd=gnu20
compiler.libcxx=libstdc++11
compiler.version=16
os=Windows

[execution]
action=build
depends_on=Get_Dependencies,Unit_Tests
```

The initial section **settings** you define your compile configurations. You might need to change some of the current code logic in `build_helper.py` if you want to change the compile configurations.

The most configurable section is the **execution** section at the bottom. 

- `action` defines the flag that indicates which function is called in the **build_helper\build_helper.py** file.
- `depends_on` defines which profiles should have already ran before the execution of this one, if one is missing, it will be triggered first.

These configurations are processes by the `conanfile.py` and based on the defined **action** call the respective function in **build_helper\build_helper.py**.

### Custom actions

To add your own action definition you need to follow the steps:

- Define a new **action** in the profile yaml **execution** section
- Describe which helper function will be called in `conanfile.py` file at the `def execute(self, profile: str = None):` method logic
- Add the helper build function in the `build_helper.py`
- Run and Test it

## Build Output

Every build configuration will generate its output in the **build** path within a folder matching the configuration name. Hence the builds are isolated from other build outputs.