#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Copy static files to staticfiles_build
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/

echo "Build completed successfully"
