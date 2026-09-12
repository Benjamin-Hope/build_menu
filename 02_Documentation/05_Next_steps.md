# Next planned steps

- [ ] Fix profile dependency naming and add validation for missing profiles.
- [ ] Add Python tests for profile loading, dependency resolution, command generation, and platform handling.
- [ ] Track successful build completion explicitly.
- [ ] Preserve incremental builds unless a clean build is requested.
- [ ] Separate the framework from the example project.
- [ ] Fix or remove the broken release workflow.
- [ ] Add contributor documentation, licensing, issue templates, and a small roadmap.

# According to AI

## Position It Clearly

Present it as:

> **Build Menu is a reusable Conan/CMake build orchestration template for C++ projects. It provides profile-based debug builds, unit tests, coverage, static analysis, reproducible Conda environments, and CLI/GUI execution.**

Avoid presenting it as a finished universal build system. Describe it as a **beta starter framework seeking contributors**.

## Prepare the Repository First

Before promoting it, add:

1. `LICENSE`
2. `CONTRIBUTING.md`
3. `CODE_OF_CONDUCT.md`
4. GitHub issue templates
5. A short roadmap
6. A tested quick-start section in `README.md`
7. A clear statement of supported platforms
8. A CI workflow that proves the example builds and tests successfully

Also fix the most visible rough edges:

- Broken profile dependency names containing `.ini`
- Missing `build.sh` referenced by release CI
- Lack of Python tests
- Incomplete packaging behavior

People are more likely to contribute when the first clone-and-build experience works.

## Give Contributors Small Entry Points

Create issues labelled:

- `good first issue`
- `help wanted`
- `documentation`
- `testing`
- `windows`
- `linux`
- `cmake`
- `conan`
- `python`

Good initial issues could be:

- Add profile-name validation
- Add tests for INI parsing
- Add a `--list-profiles` command
- Improve CLI error messages
- Add Linux CI
- Add Windows CI
- Add incremental-build support
- Implement real dependency-only setup
- Improve GUI process output
- Add install rules to the example project
- Fix release packaging
- Document how to add a new Conan dependency

Each issue should explain the expected behavior, relevant files, and acceptance criteria.

## Use a Contributor-Friendly README

Your README should answer these questions within the first few minutes:

- What problem does this solve?
- Who is it for?
- What tools are required?
- How do I run the example?
- How do I add a build profile?
- How can I contribute?
- What work is currently available?

Add a section such as:

```markdown
## Contributing

Build Menu is an early-stage open-source project and welcomes contributions.

Good places to start:

- Improve documentation
- Add tests for the Python orchestration code
- Improve Conan and CMake portability
- Add Windows and Linux CI coverage
- Improve the GUI
- Add build profiles and analysis actions

See CONTRIBUTING.md before opening a pull request.
```

## Introduce It Publicly

Use a short announcement rather than explaining every implementation detail:

> I am building an open-source Conan/CMake build orchestration tool for C++ projects. It centralizes debug builds, unit tests, coverage, static analysis, and reproducible Conda environments behind configurable profiles with both CLI and GUI support.
>
> The project is still in beta, and I am looking for contributors interested in CMake, Conan, Python tooling, cross-platform builds, testing, and documentation. Beginner-friendly issues are available in the repository.

Share it in:

- GitHub Discussions
- Reddit communities related to C++, CMake, Conan, and open source
- C++ Discord and Slack communities
- LinkedIn
- Dev.to or a short technical blog post
- Your personal or professional network

Focus each post on one contribution area instead of asking generally for “help.”

## Make the First Contribution Easy

A contributor should be able to:

1. Clone the repository.
2. Read the quick-start guide.
3. Activate the environment.
4. Run the example build.
5. Run the tests.
6. Pick a small issue.
7. Open a pull request.

Document the exact commands and expected output. A contributor guide should also explain formatting, testing, branch naming, and pull-request expectations.

The most important principle is this: **people contribute to a project when they understand its purpose, can run it quickly, and can see exactly where their contribution fits.**
