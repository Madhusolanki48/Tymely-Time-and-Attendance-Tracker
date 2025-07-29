#!/bin/bash

# Build the project
echo "Building the project..."

python3 -m pip install -r requirements.txt

echo "Collect Static..."
python3 manage.py collectstatic --noinput --clear

echo "Creating staticfiles_build directory..."
cp -r staticfiles staticfiles_build
