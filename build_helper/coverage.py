import os
import sys
import shutil
import subprocess
from pathlib import Path


def get_verified_gcov():
    gcov = 'gcov'
    if os.name == "nt":
        gcov = 'x86_64-w64-mingw32-gcov'
    else:
        gcov = 'x86_64-conda-linux-gnu-gcov'

    # Verify gcov installation
    if shutil.which(gcov) is None:
        print(f"Error: gcov not found: {gcov}")

    # Test version
    version = subprocess.check_output([gcov, "--version"]).decode("utf-8")
    print(f"Found gcov: {gcov}, version: {version}")

    return gcov


def coverage_command(build_dir: Path, output_dir: Path) -> list[str]:
    coverage_data = list(build_dir.rglob("*.gcda"))
    if not coverage_data:
        raise RuntimeError(
            f"No coverage data found in {build_dir}. "
            "Run the Unit_Tests profile first."
        )

    gcovr = shutil.which("gcovr")
    if gcovr is None:
        raise RuntimeError("gcovr is not installed in the active environment.")

    exclude_list = [
        ".*environment/.*",
        ".*/build/.*",
        ".*/test/.*",
        ".*/\\.conan2/.*",
    ]

    coverage_command = [
        gcovr,
        "--root", str(os.getcwd()),
        "--gcov-executable", get_verified_gcov(),
        "--html-details",
        f"--html={output_dir / 'coverage.html'}",
        "--xml-pretty",
        "--output", str(output_dir / "coverage.xml"),
        str(build_dir),
    ]

    for pattern in exclude_list:
        coverage_command.extend(["--exclude", pattern])

    return coverage_command
