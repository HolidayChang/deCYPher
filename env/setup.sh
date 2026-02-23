#!/bin/bash

# 1. Setup Path Anchors
# This gets the absolute path of the directory where setup.sh is located (the env folder)
ENV_SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
# This gets the project root (one level up from env)
ROOT_DIR=$(dirname "$ENV_SCRIPT_DIR")

# Move to the project root so all relative paths work correctly
cd "$ROOT_DIR"

# 2. Create Conda environment
echo "Creating Conda environment from environment.yml..."
# Points specifically to the yml in the env folder
conda env create -f "$ENV_SCRIPT_DIR/environment.yml"

# 3. Activate environment and install the package
# This ensures the 'decypher' command is linked to the project root
source $(conda info --base)/etc/profile.d/conda.sh
conda activate deCYPher_env

echo "Installing deCYPher package in editable mode..."
pip install -e .

# 4. Install k8 v0.2.4
echo "Downloading and installing k8 v0.2.4..."
curl -L https://github.com/attractivechaos/k8/releases/download/v0.2.4/k8-0.2.4.tar.bz2 | tar -jxf -
cp k8-0.2.4/k8-Linux $CONDA_PREFIX/bin/k8
chmod +x $CONDA_PREFIX/bin/k8
rm -rf k8-0.2.4

# 5. Install paftools.js
echo "Downloading paftools.js..."
curl -L https://raw.githubusercontent.com/lh3/minimap2/master/misc/paftools.js > $CONDA_PREFIX/bin/paftools.js
chmod +x $CONDA_PREFIX/bin/paftools.js

# 6. Prepare reference data (ref.tar.gz)
echo "Checking reference data in $ROOT_DIR..."
if [ -d "ref" ]; then
    echo "Reference folder 'ref' already exists. Skipping download."
else
    echo "Downloading reference data from GitHub..."
    wget https://github.com/HolidayChang/deCYPher/releases/download/v0.1.0/ref.tar.gz

    if [ -f "ref.tar.gz" ]; then
        echo "Extracting ref.tar.gz..."
        tar -zxvf ref.tar.gz
        rm ref.tar.gz
        echo "Reference data is ready."
    else
        echo "[Error] Download failed! Please check your network connection or the release link."
    fi
fi

echo "------------------------------------------------"
echo "Installation complete!"
echo "To start, run: conda activate deCYPher_env"
echo "------------------------------------------------"
