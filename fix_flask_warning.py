#!/usr/bin/env python3
"""
Fix Flask Environment Warning Script
This script helps address the FLASK_ENV deprecation warning
"""

import os

def fix_flask_warning():
    """Add APP_ENV environment variable to avoid FLASK_ENV deprecation warning"""
    print("🔧 Fixing Flask Environment Warning...")
    
    # Check current environment variables
    flask_env = os.environ.get('FLASK_ENV')
    app_env = os.environ.get('APP_ENV')
    
    print(f"Current FLASK_ENV: {flask_env}")
    print(f"Current APP_ENV: {app_env}")
    
    if flask_env and not app_env:
        print("⚠️  FLASK_ENV is set but APP_ENV is not")
        print("📋 RECOMMENDATION:")
        print("In your cPanel environment variables, add:")
        print(f"APP_ENV={flask_env}")
        print("You can keep FLASK_ENV for now (it still works)")
        print("But adding APP_ENV will eliminate the deprecation warning")
    elif app_env:
        print("✅ APP_ENV is already set - no action needed")
    else:
        print("❌ Neither FLASK_ENV nor APP_ENV is set")
        print("📋 RECOMMENDATION:")
        print("In your cPanel environment variables, add:")
        print("APP_ENV=production")
    
    print("\n🎯 The warning doesn't affect functionality - it's just a deprecation notice")

if __name__ == '__main__':
    fix_flask_warning()
