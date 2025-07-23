#!/usr/bin/env python3
"""
Vercel Build Script for Django
This script handles the build process for Vercel deployment
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main build function"""
    print("🚀 Starting Vercel build process...")
    
    # Set environment variables
    os.environ['DJANGO_SETTINGS_MODULE'] = 'attendance_system.settings'
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent.absolute()
    sys.path.insert(0, str(current_dir))
    
    # Install dependencies (usually handled by Vercel automatically)
    print("📦 Dependencies should be installed by Vercel...")
    
    # Try to import Django to verify installation
    try:
        import django
        print(f"✅ Django {django.get_version()} is available")
    except ImportError:
        print("❌ Django not found. Dependencies may not be installed.")
        return False
    
    # Setup Django
    try:
        django.setup()
        print("✅ Django setup completed")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    # Collect static files
    success = run_command(
        "python manage.py collectstatic --noinput --clear",
        "Collecting static files"
    )
    
    if not success:
        print("⚠️ Static files collection failed, but continuing...")
    
    # Run migrations (optional for build, but good to check)
    print("🔍 Checking migrations...")
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate', '--check'])
        print("✅ Migrations are up to date")
    except Exception as e:
        print(f"⚠️ Migration check failed: {e}")
    
    print("🎉 Build process completed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
