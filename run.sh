#!/bin/bash

# Run the Sample Orders API

set -e

# Change to the script's directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run the server
echo "Starting Sample Orders API on http://localhost:8000"
echo "Swagger UI: http://localhost:8000/docs"
echo ""
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
