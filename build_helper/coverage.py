import os
import shutil
import subprocess
from pathlib import Path


def get_verified_ctidy():
    ctidy = shutil.which("clang-tidy")
    if ctidy is None:
        raise RuntimeError(
            "clang-tidy is not installed in the active environment.")
    return ctidy


def gcc_include_argument(compiler: Path) -> str:
    include_dir = subprocess.check_output(
        [str(compiler), "-print-file-name=include"],
        text=True,
    ).strip()

    return f"--extra-arg-before=-isystem{include_dir}"


def code_quality_analysis(build_dir: Path) -> list[str]:
    compile_database = build_dir / "compile_commands.json"
    if not compile_database.is_file():
        raise RuntimeError(
            f"No compile_commands.json found in {build_dir}. "
            "Run the Unit_Tests profile first."
        )
    import json
    commands = json.loads(compile_database.read_text(encoding="utf-8"))
    compiler = Path(commands[0]["command"].split()[0])

    if not compiler.is_file():
        raise RuntimeError(
            f"Compiler from compilation database does not exist: {compiler}"
        )

    source_files = [
        Path(entry["file"])
        for entry in commands
        if "/test/" not in entry["file"].replace("\\", "/")
    ]

    return [
        get_verified_ctidy(),
        "-p", str(build_dir),
        "--checks="
        "-*,"
        "clang-diagnostic-*,"
        "bugprone-*,"
        "performance-*,"
        "portability-*,"
        "clang-analyzer-*,"
        "cert-*,"
        "cppcoreguidelines-*,"
        "modernize-use-nullptr,"
        "readability-implicit-bool-conversion",
        gcc_include_argument(compiler),

        "--extra-arg=-Wall",
        "--extra-arg=-Wextra",
        "--extra-arg=-Wpedantic",
        "--extra-arg=-Wshadow",
        "--extra-arg=-Wconversion",
        "--extra-arg=-Wunused-variable",
        "--extra-arg=-Wformat=2",
        "--extra-arg=-Wnull-dereference",
        "--extra-arg=-Wdouble-promotion",

        "--warnings-as-errors="
        "clang-diagnostic-unused-variable,"
        "clang-diagnostic-unused-parameter,"
        "clang-diagnostic-shadow,"
        "clang-diagnostic-conversion,"
        "clang-diagnostic-format",

        *map(str, source_files),
    ]


def get_verified_gcov():
    gcov = 'gcov'
    if os.name == "nt":
        gcov = 'x86_64-w64-mingw32-gcov'
    else:
        gcov = 'x86_64-conda-linux-gnu-gcov'

    # Verify gcov installation
    if shutil.which(gcov) is None:
        raise RuntimeError(f"Error: gcov not found: {gcov}")

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
