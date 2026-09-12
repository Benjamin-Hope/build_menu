# Project Goals and High level Documentation

## Description

This tool aims to centralize the multiple runner configurations, such as debug and unit test, into one interface. The script runs within a conda environment to ensure reproducibility and repeatability on any device. The script is constructed so that the project can be forked or downloaded separately and serve as a starting point for any project. In this **Guide** you will find instructions on how to activate the environment, add project dependent packages, add, configure and run new configuration. The following section [Initial Project Requirements](#initial-project-requirements) will describe the goals and requirements set when developing this script.

## Initial Project Requirements

- [x] Graphical control interface used to control target configurations
- [x] Graphical interface integrated and compatible with the conanfile.py structure requirements
- [x] Configurations defined in yaml structure and accessed by the graphical interface
- [x] Addition of new Configuration need to be intuitive and easy
- [x] Possibility of adding custom configurations and actions
- [x] Different OS compatibility
- [x] Build Paths based on configuration naming
- [x] Fetch packaging configuration with specified file destination
- [x] Different builds threaded runs
- [x] Unit test runner configured
- [x] Coverage test runner configured
- [ ] Runners use previous build resources to accelerate target build
- [ ] Packaging configuration available
- [ ] Docstring configuration available
- [ ] Script Unit Testing
- [ ] Setup Pipeline for Code maintainability

## Developer Notes

_"Please consider this project as a Beta version, testing is still required along with a code cleanup and better structuring.
Feel free to announce any bugs or if you feel like contributing, open a pull request."_ :smile:
