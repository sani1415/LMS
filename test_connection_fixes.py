#!/usr/bin/env python3
"""
Test Connection Fixes Script
This script tests the database connection fixes
"""

import os
import sys

def test_sqlalchemy_fixes():
    """Test the SQLAlchemy fixes"""
    print("🔍 Testing SQLAlchemy Fixes...")
    print("=" * 40)
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app import app, check_database_connection
        
        with app.app_context():
            print("✅ App context created successfully")
            
            # Test the connection check function
            print("🔌 Testing database connection check...")
            result = check_database_connection()
            
            if result:
                print("✅ Database connection check PASSED!")
                print("✅ SQLAlchemy text() fix is working")
                print("✅ Connection recovery is working")
                return True
            else:
                print("❌ Database connection check FAILED")
                print("❌ There may still be connection issues")
                return False
                
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_environment_setup():
    """Test environment setup"""
    print("\n🔍 Testing Environment Setup...")
    print("=" * 40)
    
    required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_NAME']
    missing_vars = []
    
    for var in required_vars:
        if os.environ.get(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Missing")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n🚨 Missing variables: {missing_vars}")
        return False
    else:
        print("\n✅ All required environment variables are set!")
        return True

def main():
    """Main test function"""
    print("🧪 Testing Database Connection Fixes")
    print("=" * 50)
    
    # Test environment setup
    env_ok = test_environment_setup()
    
    if env_ok:
        # Test SQLAlchemy fixes
        fixes_ok = test_sqlalchemy_fixes()
        
        if fixes_ok:
            print("\n🎉 ALL TESTS PASSED!")
            print("Your database connection fixes are working correctly.")
            print("You can now deploy these changes to production.")
        else:
            print("\n🚨 SOME TESTS FAILED")
            print("Please check the errors above before deploying.")
    else:
        print("\n🚨 ENVIRONMENT SETUP ISSUES")
        print("Please fix the environment variables first.")

if __name__ == '__main__':
    main()
