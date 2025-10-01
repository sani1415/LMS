#!/usr/bin/env python3
"""
Startup Optimization Script for cPanel
This script helps optimize the application startup process
"""

import os
import sys

def check_startup_issues():
    """Check for common startup issues"""
    print("🔍 Checking Startup Issues...")
    print("=" * 50)
    
    issues_found = []
    
    # Check for fileno issues
    try:
        sys.stdout.fileno()
        print("✅ stdout.fileno() works")
    except (OSError, io.UnsupportedOperation) as e:
        print(f"⚠️  stdout.fileno() issue: {e}")
        issues_found.append("fileno")
    
    # Check for environment variables
    required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_NAME']
    for var in required_vars:
        if not os.environ.get(var):
            print(f"❌ Missing: {var}")
            issues_found.append(f"missing_{var}")
        else:
            print(f"✅ {var}: Set")
    
    # Check for Flask environment
    flask_env = os.environ.get('FLASK_ENV')
    app_env = os.environ.get('APP_ENV')
    
    if flask_env:
        print(f"✅ FLASK_ENV: {flask_env}")
    if app_env:
        print(f"✅ APP_ENV: {app_env}")
    
    if not flask_env and not app_env:
        print("⚠️  No Flask environment set")
        issues_found.append("no_flask_env")
    
    return issues_found

def optimize_startup():
    """Provide startup optimization recommendations"""
    print("\n🚀 Startup Optimization Recommendations...")
    print("=" * 50)
    
    issues = check_startup_issues()
    
    if not issues:
        print("✅ No major startup issues found!")
        print("Your application should start smoothly.")
    else:
        print("🔧 Issues found and recommendations:")
        
        if "fileno" in issues:
            print("• Fix fileno issues: Use the updated app.py with SafeOutput")
        
        if any("missing_" in issue for issue in issues):
            print("• Set missing environment variables in cPanel")
        
        if "no_flask_env" in issues:
            print("• Set FLASK_ENV=production in cPanel environment variables")

def test_application_startup():
    """Test if the application can start properly"""
    print("\n🧪 Testing Application Startup...")
    print("=" * 50)
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app import app
        print("✅ App import successful")
        
        # Test database connection
        from app import check_database_connection
        with app.app_context():
            result = check_database_connection()
            if result:
                print("✅ Database connection test passed")
                return True
            else:
                print("❌ Database connection test failed")
                return False
                
    except Exception as e:
        print(f"❌ Application startup test failed: {e}")
        return False

def main():
    """Main optimization function"""
    print("🔧 cPanel Startup Optimization Tool")
    print("=" * 60)
    
    # Check for startup issues
    optimize_startup()
    
    # Test application startup
    startup_ok = test_application_startup()
    
    if startup_ok:
        print("\n🎉 STARTUP OPTIMIZATION COMPLETE!")
        print("Your application should now start more reliably.")
        print("The fileno errors should be resolved.")
    else:
        print("\n🚨 STARTUP ISSUES DETECTED")
        print("Please address the issues above before deploying.")

if __name__ == '__main__':
    main()
