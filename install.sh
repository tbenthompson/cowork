#!/bin/bash

set -e

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Please install it first."
    exit 1
fi

# Build the project
echo "Building the project..."
poetry build

# Install the package
echo "Installing the package..."
pip install --user dist/*.whl

# Create ~/bin if it doesn't exist
mkdir -p ~/bin

# Get the installation directory
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get the path to the cowork executable
COWORK_PATH=$(poetry run which cowork)

# Create wrapper script
echo "Creating wrapper script..."
cat > ~/bin/cowork-wrapper <<EOL
#!/bin/bash
nohup "${COWORK_PATH}" "\$@" >> "${INSTALL_DIR}/cowork.log" 2>&1 &
EOL

# Make wrapper script executable
chmod +x ~/bin/cowork-wrapper

# Update symlink to use wrapper script
echo "Updating symlink in ~/bin..."
ln -sf ~/bin/cowork-wrapper ~/bin/cowork

echo "Installation complete. You can now run 'cowork' from anywhere, and it will run in the background."
echo "Output will be logged to ${INSTALL_DIR}/cowork.log"
echo "Make sure ~/bin is in your PATH."