#!/bin/bash

deactivate

# Create .venv inside the same project folder
poetry config virtualenvs.in-project true

# Remove the existing virtual environment
rm -rf .venv/

# Create virtual environment
poetry install

# Install libraries
poetry add -G dev -e ../s3
poetry add -G dev -e ../db