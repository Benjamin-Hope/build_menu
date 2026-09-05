@echo off

REM ---------- CONFIGURATION ----------
set "ENV_FOLDER=.environment"
set "YAML_FILE=%ENV_FOLDER%\conda_env.yaml"
set "LOCK_FILE=%ENV_FOLDER%\conda-lock.win-64.yml"
set "CHECKSUM_FILE=%ENV_FOLDER%\.env_checksum"
set "ENV_PREFIX=%~dp0.environment\envs\conda_env"
REM -----------------------------------

REM Locate conda.bat (prefer Miniforge default path)
set "CONDA_BAT=C:\conda\condabin\conda.bat"
if not exist "%CONDA_BAT%" (
    for /f "delims=" %%I in ('where conda.bat 2^>nul') do (
        set "CONDA_BAT=%%I"
        goto :conda_found
    )
)

:conda_found
if not exist "%CONDA_BAT%" (
    echo Error: Conda not found.
    exit /b 1
)

REM Ensure environment folder exists
if not exist "%ENV_FOLDER%" (
    echo Error: Directory "%ENV_FOLDER%" not found.
    exit /b 1
)

REM Ensure YAML exists
if not exist "%YAML_FILE%" (
    echo Error: YAML file "%YAML_FILE%" not found.
    exit /b 1
)

REM Compute current checksum of YAML
set "CURRENT_CHECKSUM="
for /f "delims=" %%I in ('
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "(Get-FileHash -Algorithm SHA256 -Path '%YAML_FILE%').Hash.ToLower()"
') do set "CURRENT_CHECKSUM=%%I"

if not defined CURRENT_CHECKSUM (
    echo Error: Failed to compute YAML checksum.
    exit /b 1
)

REM Read last checksum
set "LAST_CHECKSUM="
if exist "%CHECKSUM_FILE%" (
    set /p LAST_CHECKSUM=<"%CHECKSUM_FILE%"
)

REM Decide whether lock regeneration is needed
set "NEED_LOCK_REGEN=0"
if not exist "%LOCK_FILE%" (
    echo Lock file "%LOCK_FILE%" not found.
    set "NEED_LOCK_REGEN=1"
)

if /I not "%CURRENT_CHECKSUM%"=="%LAST_CHECKSUM%" (
    echo Detected changes in "%YAML_FILE%".
    set "NEED_LOCK_REGEN=1"
)

REM Generate lock file if needed
if "%NEED_LOCK_REGEN%"=="1" (
    echo Generating lock file "%LOCK_FILE%"...

    where conda-lock >nul 2>nul
    if errorlevel 1 (
        echo conda-lock not found. Installing into base environment...
        call "%CONDA_BAT%" install -n base -c conda-forge -y conda-lock
        if errorlevel 1 (
            echo Error installing conda-lock.
            exit /b 1
        )
    )

    call "%CONDA_BAT%" run -n base conda-lock -f "%YAML_FILE%" -p win-64 --lockfile "%LOCK_FILE%"
    if errorlevel 1 (
        echo Error generating lock file.
        exit /b 1
    )
)

REM Recreate environment when lock changed or env missing/corrupted
set "RECREATE=0"
if "%NEED_LOCK_REGEN%"=="1" (
    set "RECREATE=1"
)

if not exist "%ENV_PREFIX%\conda-meta\history" (
    set "RECREATE=1"
)

if "%RECREATE%"=="1" (
    if exist "%ENV_PREFIX%" (
        echo Removing existing environment prefix "%ENV_PREFIX%"...
        call "%CONDA_BAT%" env remove -p "%ENV_PREFIX%" -y >nul 2>nul
        if exist "%ENV_PREFIX%" (
            rmdir /s /q "%ENV_PREFIX%"
            if errorlevel 1 (
                echo Error removing stale folder "%ENV_PREFIX%".
                exit /b 1
            )
        )
    )

    for %%I in ("%ENV_PREFIX%") do set "ENV_PREFIX_PARENT=%%~dpI"
    if not exist "%ENV_PREFIX_PARENT%" mkdir "%ENV_PREFIX_PARENT%"

    echo Creating environment from lock file at "%ENV_PREFIX%"...
    call "%CONDA_BAT%" run -n base conda-lock install -p "%ENV_PREFIX%" "%LOCK_FILE%"
    if errorlevel 1 (
        echo Error creating environment from lock file.
        exit /b 1
    )

    > "%CHECKSUM_FILE%" echo %CURRENT_CHECKSUM%
) else (
    echo Environment at "%ENV_PREFIX%" is already up to date.
)

REM Activate environment by prefix
echo Activating environment at "%ENV_PREFIX%"...
call "%CONDA_BAT%" activate "%ENV_PREFIX%"
if errorlevel 1 (
    echo Failed to activate environment at "%ENV_PREFIX%".
    exit /b 1
)

if not defined CONDA_PREFIX (
    echo Activation failed: CONDA_PREFIX is not set.
    exit /b 1
)

echo.
echo ==========================================
echo Environment is active.
echo Prefix: %CONDA_PREFIX%
echo ==========================================

exit /b 0