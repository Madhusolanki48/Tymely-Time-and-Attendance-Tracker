#!/usr/bin/env python3
"""
Database Connection Test Script
This script tests the connection to your Render PostgreSQL database
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')

try:
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

# Test database connection
from django.db import connection
from django.core.management.color import make_style

style = make_style()

def test_database_connection():
    """Test the database connection"""
    print("\n" + "="*50)
    print("🔍 TESTING DATABASE CONNECTION")
    print("="*50)
    
    try:
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        print(f"✅ Database connection successful!")
        print(f"✅ Test query result: {result}")
        
        # Get database info
        db_settings = connection.settings_dict
        print(f"\n📊 DATABASE INFORMATION:")
        print(f"   Engine: {db_settings['ENGINE']}")
        print(f"   Name: {db_settings['NAME']}")
        print(f"   Host: {db_settings['HOST']}")
        print(f"   Port: {db_settings['PORT']}")
        print(f"   User: {db_settings['USER']}")
        
        # Test if we can check tables
        db_engine = connection.settings_dict['ENGINE']
        
        with connection.cursor() as cursor:
            if 'postgresql' in db_engine:
                # PostgreSQL query
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
            elif 'sqlite' in db_engine:
                # SQLite query
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                    ORDER BY name;
                """)
            else:
                # Generic fallback
                cursor.execute("SELECT 'Unknown database type' as table_name;")
                
            tables = cursor.fetchall()
            
        print(f"\n📋 EXISTING TABLES ({len(tables)} found):")
        if tables:
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("   No tables found (database is empty)")
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed!")
        print(f"❌ Error: {e}")
        print(f"\n🔧 TROUBLESHOOTING TIPS:")
        print(f"   1. Check your DATABASE_URL in .env file")
        print(f"   2. Ensure your Render database is running")
        print(f"   3. Verify your database credentials")
        print(f"   4. Check if your IP is whitelisted (if applicable)")
        return False

def test_migrations_status():
    """Check migration status"""
    print("\n" + "="*50)
    print("🔍 CHECKING MIGRATIONS STATUS")
    print("="*50)
    
    try:
        from django.core.management import execute_from_command_line
        from io import StringIO
        import contextlib
        
        # Capture the output of showmigrations
        output = StringIO()
        with contextlib.redirect_stdout(output):
            execute_from_command_line(['manage.py', 'showmigrations', '--verbosity=0'])
        
        migrations_output = output.getvalue()
        print("📊 MIGRATIONS STATUS:")
        print(migrations_output)
        
        return True
        
    except Exception as e:
        print(f"❌ Could not check migrations: {e}")
        return False

if __name__ == "__main__":
    print("🚀 STARTING DATABASE CONNECTION TEST")
    print("="*50)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print(f"✅ DATABASE_URL found in environment")
        if database_url.startswith('postgresql'):
            print(f"✅ PostgreSQL URL detected")
        else:
            print(f"⚠️  Warning: DATABASE_URL doesn't look like PostgreSQL")
    else:
        print(f"❌ DATABASE_URL not found in environment variables")
        sys.exit(1)
    
    # Run tests
    db_success = test_database_connection()
    migration_success = test_migrations_status()
    
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    print(f"Database Connection: {'✅ PASS' if db_success else '❌ FAIL'}")
    print(f"Migrations Check: {'✅ PASS' if migration_success else '❌ FAIL'}")
    
    if db_success:
        print(f"\n🎉 Your database connection is working!")
        print(f"💡 Next steps:")
        print(f"   1. Run migrations: python manage.py migrate")
        print(f"   2. Create superuser: python manage.py createsuperuser")
        print(f"   3. Test your Django app locally")
    else:
        print(f"\n💥 Database connection failed. Please check your configuration.")
        
    print("="*50)
