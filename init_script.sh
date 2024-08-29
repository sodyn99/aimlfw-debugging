#!/bin/bash
set -e

echo "Installing dependencies..." > /tmp/progress_state
apt-get update && apt-get install -y curl git wget
echo "Dependencies installed." > /tmp/progress_state

echo "Installing Miniconda..." > /tmp/progress_state
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p /opt/conda
rm miniconda.sh
echo "Miniconda installed." > /tmp/progress_state

echo "Setting up Conda environment..." > /tmp/progress_state
export PATH="/opt/conda/bin:$PATH"
echo 'export PATH="/opt/conda/bin:$PATH"' >> /root/.bashrc
. /opt/conda/etc/profile.d/conda.sh
conda init bash
. /root/.bashrc
conda create -n aimlfw python=3.8 -y
echo 'conda activate aimlfw' >> /root/.bashrc
. /root/.bashrc
echo "Conda environment set up." > /tmp/progress_state

# Install ipykernel in the Conda environment
echo "Installing ipykernel..." > /tmp/progress_state
conda run -n aimlfw conda install -n aimlfw ipykernel -y
echo "ipykernel installed." > /tmp/progress_state

# Get the Python version
PYTHON_VERSION=$(python --version | awk '{print $2}')

# Register the kernel with Jupyter
echo "Registering ipykernel..." > /tmp/progress_state
conda run -n aimlfw python3 -m ipykernel install --user --name aimlfw --display-name "aimlfw (Python $PYTHON_VERSION)"
echo "ipykernel registered as 'aimlfw (Python $PYTHON_VERSION)'." > /tmp/progress_state

echo "Installing code-server..." > /tmp/progress_state
curl -fsSL https://code-server.dev/install.sh | sh
echo "code-server installed." > /tmp/progress_state

echo "Cloning SDK repositories..." > /tmp/progress_state
git clone -b g-release "https://gerrit.o-ran-sc.org/r/aiml-fw/athp/sdk/feature-store" /SDK/featurestoresdk_main
git clone -b g-release "https://gerrit.o-ran-sc.org/r/aiml-fw/athp/sdk/model-storage" /SDK/modelmetricssdk_main
echo "SDK Repositories cloned." > /tmp/progress_state

echo "Installing Python requirements..." > /tmp/progress_state
conda run -n aimlfw python3 /app_run/install_requirements.py
echo "Python requirements installed." > /tmp/progress_state

echo "Starting code-server..." > /tmp/progress_state
code-server --install-extension ms-python.python
code-server --install-extension ms-toolsai.jupyter
code-server --auth none --bind-addr 0.0.0.0:10000 /app_run/src --disable-telemetry > /dev/null 2>&1 &
echo "code-server started." > /tmp/progress_state

echo "Initialization complete" > /tmp/init_complete
