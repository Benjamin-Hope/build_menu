#!/usr/bin/env bash

set -u

# ---------- CONFIGURATION ----------
ENV_FOLDER=".environment"
ENV_NAME="conda_env"
YAML_FILE="$ENV_FOLDER/conda_env.yaml"
CHECKSUM_FILE="$ENV_FOLDER/.env_checksum"
# -----------------------------------

# Ensure conda is available
if ! command -v conda >/dev/null 2>&1; then
    echo "Error: Conda (Miniforge) not found in PATH."
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

# ----------------------------------------------------
# Determine whether the environment already exists
# ----------------------------------------------------
ENV_EXISTS=0

if conda env list | awk '{print $1}' | grep -Fxq "$ENV_NAME"; then
    ENV_EXISTS=1
fi

# ----------------------------------------------------
# Decide whether recreation is needed
# ----------------------------------------------------
RECREATE=0

if [ "$ENV_EXISTS" -eq 0 ]; then
    echo "Environment '$ENV_NAME' does not exist."
    RECREATE=1
fi

if [ "$CURRENT_CHECKSUM" != "$LAST_CHECKSUM" ]; then
    echo "Detected changes in '$YAML_FILE'."
    RECREATE=1
fi

# ----------------------------------------------------
# Recreate environment if required
# ----------------------------------------------------
if [ "$RECREATE" -eq 1 ]; then

    if [ "$ENV_EXISTS" -eq 1 ]; then
        echo "Removing existing environment '$ENV_NAME'..."
        conda env remove -n "$ENV_NAME" -y
    fi

    echo "Creating environment '$ENV_NAME'..."
    conda env create -f "$YAML_FILE"

    echo "$CURRENT_CHECKSUM" > "$CHECKSUM_FILE"

else
    echo "Environment '$ENV_NAME' is already up to date."
fi

# ----------------------------------------------------
# Activate environment
# ----------------------------------------------------
echo "Activating environment '$ENV_NAME'..."
conda activate "$ENV_NAME"

# ----------------------------------------------------
# Query active environment information
# ----------------------------------------------------
ACTIVE_ENV=$(conda info --json | jq -r '.active_prefix_name')
ACTIVE_ENV_PATH=$(conda info --json | jq -r '.active_prefix')

if [ "$ACTIVE_ENV" = "$ENV_NAME" ]; then
    echo
    echo "=========================================="
    echo "Environment '$ENV_NAME' is active."
    echo "Path: $ACTIVE_ENV_PATH"
    echo "=========================================="
else
    echo "Failed to activate '$ENV_NAME'."
    return 1
fi
