#!/usr/bin/env bash

set -u

# ---------- CONFIGURATION ----------
ENV_FOLDER=".environment"
YAML_FILE="$ENV_FOLDER/conda_env.yaml"
LOCK_FILE="$ENV_FOLDER/conda-lock.linux-64.yml"
CHECKSUM_FILE="$ENV_FOLDER/.env_checksum"
ENV_PREFIX="$(pwd)/.environment/envs/conda_env"
# -----------------------------------

# Ensure conda is available
if ! command -v conda >/dev/null 2>&1; then
    echo "Error: Conda not found in PATH."
    return 1
fi

# Ensure environment folder exists
if [ ! -d "$ENV_FOLDER" ]; then
    echo "Error: Directory '$ENV_FOLDER' not found."
    return 1
fi

# Ensure YAML exists
if [ ! -f "$YAML_FILE" ]; then
    echo "Error: YAML file '$YAML_FILE' not found."
    return 1
fi

# Initialize Conda for this shell
source "$(conda info --base)/etc/profile.d/conda.sh"

# Compute current checksum
CURRENT_CHECKSUM=$(sha256sum "$YAML_FILE" | awk '{print $1}')

# Read previous checksum
if [ -f "$CHECKSUM_FILE" ]; then
    LAST_CHECKSUM=$(cat "$CHECKSUM_FILE")
else
    LAST_CHECKSUM=""
fi

# Decide whether lock regeneration is needed
NEED_LOCK_REGEN=0
if [ ! -f "$LOCK_FILE" ]; then
    echo "Lock file '$LOCK_FILE' not found."
    NEED_LOCK_REGEN=1
fi

if [ "$CURRENT_CHECKSUM" != "$LAST_CHECKSUM" ]; then
    echo "Detected changes in '$YAML_FILE'."
    NEED_LOCK_REGEN=1
fi

# Generate lock file if needed
if [ "$NEED_LOCK_REGEN" -eq 1 ]; then
    if ! command -v conda-lock >/dev/null 2>&1; then
        echo "conda-lock not found. Installing in base..."
        conda install -n base -c conda-forge -y conda-lock || return 1
    fi

    echo "Generating lock file '$LOCK_FILE'..."
    conda run -n base conda-lock -f "$YAML_FILE" -p linux-64 --lockfile "$LOCK_FILE" || return 1
fi

# Recreate environment if lock changed or env missing/corrupted
RECREATE=0
if [ "$NEED_LOCK_REGEN" -eq 1 ]; then
    RECREATE=1
fi

if [ ! -f "$ENV_PREFIX/conda-meta/history" ]; then
    RECREATE=1
fi

if [ "$RECREATE" -eq 1 ]; then
    if [ -d "$ENV_PREFIX" ]; then
        echo "Removing existing environment prefix '$ENV_PREFIX'..."
        conda env remove -p "$ENV_PREFIX" -y >/dev/null 2>&1 || true
        rm -rf "$ENV_PREFIX"
    fi

    mkdir -p "$(dirname "$ENV_PREFIX")"

    echo "Creating environment from lock file at '$ENV_PREFIX'..."
    conda run -n base conda-lock install -p "$ENV_PREFIX" "$LOCK_FILE" || return 1

    echo "$CURRENT_CHECKSUM" > "$CHECKSUM_FILE"
else
    echo "Environment at '$ENV_PREFIX' is already up to date."
fi

echo "Activating environment at '$ENV_PREFIX'..."
conda activate "$ENV_PREFIX" || return 1

echo
echo "=========================================="
echo "Environment is active."
echo "Prefix: $CONDA_PREFIX"
echo "=========================================="