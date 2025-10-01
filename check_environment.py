#!/usr/bin/env python3
"""
Environment Variables Check Script for cPanel
Run this to diagnose database configuration issues
"""

import os
import sys

def check_environment_variables():
    """Check if all required environment variables are set"""
    print("🔍 Checking Environment Variables...")
    print("=" * 50)
    
    required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_NAME']
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Mask password for security
            if var == 'DB_PASSWORD':
                display_value = '*' * len(value)
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET")
            missing_vars.append(var)
    
    print("=" * 50)
    
    if missing_vars:
        print(f"🚨 MISSING VARIABLES: {', '.join(missing_vars)}")
        print("\n📋 TO FIX THIS:")
        print("1. Login to cPanel")
        print("2. Go to 'Environment Variables' or 'Python App' settings")
        print("3. Add these variables:")
        for var in missing_vars:
            print(f"   - {var}=your_value_here")
        return False
    else:
        print("✅ All required environment variables are set!")
        return True

def test_database_connection():
    """Test database connection with current settings"""
    print("\n🔍 Testing Database Connection...")
    print("=" * 50)
    
    try:
        import pymysql
        
        db_user = os.environ.get('DB_USER')
        db_password = os.environ.get('DB_PASSWORD')
        db_host = os.environ.get('DB_HOST')
        db_name = os.environ.get('DB_NAME')
        
        if not all([db_user, db_password, db_host, db_name]):
            print("❌ Cannot test connection - missing environment variables")
            return False
        
        print(f"Attempting connection to: {db_user}@{db_host}/{db_name}")
        
        # Test connection
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            charset='utf8mb4',
            connect_timeout=10
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        print("✅ Database connection successful!")
        print(f"✅ Test query result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 POSSIBLE FIXES:")
        print("1. Check if database name is correct")
        print("2. Verify username and password")
        print("3. Confirm database exists in cPanel")
        print("4. Check if user has proper permissions")
        return False

def check_flask_config():
    """Check Flask configuration"""
    print("\n🔍 Checking Flask Configuration...")
    print("=" * 50)
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from backend.config import config
        
        # Check which config is being used
        config_name = os.environ.get('APP_ENV') or os.environ.get('FLASK_ENV', 'development')
        print(f"Config being used: {config_name}")
        
        if config_name == 'production':
            prod_config = config['production']
            db_uri = prod_config.SQLALCHEMY_DATABASE_URI
            
            if db_uri:
                # Mask password in URI for security
                masked_uri = db_uri.replace(os.environ.get('DB_PASSWORD', ''), '***')
                print(f"✅ Database URI: {masked_uri}")
            else:
                print("❌ Database URI is None - environment variables not set properly")
                
            engine_options = prod_config.SQLALCHEMY_ENGINE_OPTIONS
            print(f"✅ Engine options: {engine_options}")
        else:
            print(f"⚠️  Using {config_name} config - make sure APP_ENV=production for cPanel")
            
        return True
        
    except Exception as e:
        print(f"❌ Flask config check failed: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("🔧 cPanel Database Configuration Diagnostic Tool")
    print("=" * 60)
    
    # Check environment variables
    env_ok = check_environment_variables()
    
    if env_ok:
        # Test database connection
        db_ok = test_database_connection()
        
        # Check Flask config
        config_ok = check_flask_config()
        
        if db_ok and config_ok:
            print("\n🎉 ALL CHECKS PASSED!")
            print("Your database configuration looks good.")
            print("If you're still getting 503 errors, the issue might be:")
            print("1. Database server temporarily unavailable")
            print("2. Connection pool exhausted")
            print("3. Network connectivity issues")
        else:
            print("\n🚨 CONFIGURATION ISSUES FOUND")
            print("Please fix the issues above and run this script again.")
    else:
        print("\n🚨 ENVIRONMENT VARIABLES NOT SET")
        print("Please set the required environment variables in cPanel first.")

if __name__ == '__main__':
    main()
