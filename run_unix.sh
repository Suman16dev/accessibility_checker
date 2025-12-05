#!/bin/bash
echo "Installing Python requirements..."

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed. Install from python.org or package manager."
    read -p "Press Enter to exit..."
    exit 1
fi

# Install requirements if file exists
if [ -f "requirements.txt" ]; then
    echo "Found requirements.txt, installing packages..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install requirements."
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo "Requirements installed successfully!"
else
    echo "Warning: requirements.txt not found."
fi

echo "Starting accessibility checker web app..."
python3 app.py
