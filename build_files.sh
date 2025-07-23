#!/bin/bash

echo "Starting build process..."

# Install Python dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create output directory
echo "Preparing static files for deployment..."
mkdir -p staticfiles_build

# Copy all static files
if [ -d "staticfiles" ]; then
    cp -r staticfiles/* staticfiles_build/ 2>/dev/null || echo "No staticfiles to copy"
fi

# Also copy static directory if it exists
if [ -d "static" ]; then
    cp -r static/* staticfiles_build/ 2>/dev/null || echo "No static files to copy"
fi

echo "✅ Build completed successfully"
