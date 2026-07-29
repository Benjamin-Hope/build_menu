@echo off

REM ---------- CONFIGURATION ----------
set "ENV_FOLDER=.environment"
set "ENV_NAME=conda_env"
set "YAML_FILE=%ENV_FOLDER%\conda_env.yaml"
set "CHECKSUM_FILE=%ENV_FOLDER%\.env_checksum"
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

REM ----------------------------------------------------
REM Determine whether the environment already exists
REM ----------------------------------------------------
set "ENV_EXISTS=0"

call "%CONDA_BAT%" env list | findstr /R /C:"^[ *]*%ENV_NAME% " >nul
if not errorlevel 1 (
    set "ENV_EXISTS=1"
)

REM ----------------------------------------------------
REM Decide whether recreation is needed
REM ----------------------------------------------------
set "RECREATE=0"

if "%ENV_EXISTS%"=="0" (
    echo Environment "%ENV_NAME%" does not exist.
    set "RECREATE=1"
)

if /I not "%CURRENT_CHECKSUM%"=="%LAST_CHECKSUM%" (
    echo Detected changes in "%YAML_FILE%".
    set "RECREATE=1"
)

REM ----------------------------------------------------
REM Recreate environment if required
REM ----------------------------------------------------
if "%RECREATE%"=="1" (

    if "%ENV_EXISTS%"=="1" (
        echo Removing existing environment "%ENV_NAME%"...
        call "%CONDA_BAT%" remove -n "%ENV_NAME%" --all -y
        if errorlevel 1 (
            echo Error removing environment.
            exit /b 1
        )
    )

    echo Creating environment "%ENV_NAME%"...
    call "%CONDA_BAT%" env create -f "%YAML_FILE%"
    if errorlevel 1 (
        echo Error creating environment.
        exit /b 1
    )

    REM Save checksum
    > "%CHECKSUM_FILE%" echo %CURRENT_CHECKSUM%

) else (
    echo Environment "%ENV_NAME%" is already up to date.
)

REM ----------------------------------------------------
REM Activate environment
REM ----------------------------------------------------
echo Activating environment "%ENV_NAME%"...
call "%CONDA_BAT%" activate "%ENV_NAME%"
if errorlevel 1 (
    echo Failed to activate "%ENV_NAME%".
    exit /b 1
)

REM ----------------------------------------------------
REM Query active environment information
REM ----------------------------------------------------
set "ACTIVE_ENV="
set "ACTIVE_ENV_PATH="

for /f "delims=" %%I in ('
    call "%CONDA_BAT%" info --json ^
    ^| powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$j=$input|Out-String|ConvertFrom-Json; $j.active_prefix_name"
') do set "ACTIVE_ENV=%%I"

for /f "delims=" %%I in ('
    call "%CONDA_BAT%" info --json ^
    ^| powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$j=$input|Out-String|ConvertFrom-Json; $j.active_prefix"
') do set "ACTIVE_ENV_PATH=%%I"

if /I "%ACTIVE_ENV%"=="%ENV_NAME%" (
    echo.
    echo ==========================================
    echo Environment "%ENV_NAME%" is active.
    echo Path: %ACTIVE_ENV_PATH%
    echo ==========================================
) else (
    echo Failed to activate "%ENV_NAME%".
    exit /b 1
)

exit /b 0