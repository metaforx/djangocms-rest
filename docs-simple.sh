#!/bin/bash

# Simple documentation server script for django CMS REST
# Run this from the project root directory to start the basic Furo theme

echo "Starting django CMS REST documentation with basic Furo theme..."
echo "Server will be available at http://localhost:8000"
echo "Press Ctrl+C to stop"

# Change to docs directory and start the server
cd docs
poetry run sphinx-autobuild . _build/html --port 8000 --host 0.0.0.0 --open-browser 