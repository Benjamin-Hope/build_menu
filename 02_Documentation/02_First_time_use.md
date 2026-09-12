# So its your "First Time"

## Initial Requirements

The code within a conda environment, hence this needs to be setup locally in your environment. If you have never used the conan or dont know what it is, refer to their documentation available in [Conda Website](https://docs.conda.io/projects/conda/en/latest/index.html). In this project we use the **Miniforge** since it is light weight and has better ARM and Packages support. It is configured around _conda-forge_, thus we are not forced or limited to the _anaconda_ environment. You can find the conda forge installation in the the [Conda Forge Installation](https://conda-forge.org/download/).

You can verify the current packages imported in the _.environment\conda_env.yaml_ file. The default packages included are required for the current version to work properly.

## Launch Environment

You can activate the conda environment by running one of the activations scripts based on your OS.

### Windows

To activate with a windows device, start by opening a cmd terminal and run the following in the root path of the project.

`.\activate_conda_end.bat` or `call activate_conda_end.bat`

This will install all the packages defined in the previously mentioned yaml file and activate the environment. Note that every time you change the yaml packages required, a new installation of the packages is triggered.

To deactivate the environment run the following command within the activated environment `conda deactivate`.

### Unix

The activation within the Unix is very similar to the windows. Start by opening a terminal and run the following command in the root path of the project.

`source activate_conda_env.sh`

This will install all the packages defined in the previously mentioned yaml file and activate the environment. Note that every time you change the yaml packages required, a new installation of the packages is triggered.

To deactivate the environment run the following command within the activated environment `conda deactivate`.

## Launch the Control Interface

Once you have activated your environment you can open the Control Graphical Interface by running the following command `python conanfile_python --gui`.

This interface opens a tkinter GUI with the different default configurations loaded. To run of the configurations select one and press the **EXECUTE** button on the top left corner.

## Run Configuration

As mentioned before, you can run your desired configuration by following the previous steps:

- Activate environment `.\activate_conda_end.bat` or `source activate_conda_env.sh`.
- Open the Control GUI with `python conanfile_python --gui`.
- Select the desired configuration
- Run it by pressing the **EXECUTE** button on the top left corner.

You can also just run the desired configuration by triggering them in the terminal directly, for example:

`python conanfile_python --Debug_Build`

You can check the available configuration in the _**build_profiles**_ path or by running the `python conanfile_python --help`.
