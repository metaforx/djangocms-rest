#!/bin/bash

# Live documentation server script for django CMS REST
# Run this from the project root directory

echo "Starting django CMS REST documentation live server..."
echo "Server will be available at http://localhost:8000"
echo "Press Ctrl+C to stop"

# Change to docs directory and start the server
cd docs
poetry run sphinx-autobuild . _build/html --port 8000 --host 0.0.0.0 --open-browser 