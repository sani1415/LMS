#!/usr/bin/env python3
"""
Complete Database Reset Script for cPanel
This script will completely reset the database and create all required tables.
"""

import os
import sys
from sqlalchemy import text, inspect

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from backend.models import db, LibraryLog, Member, Book, Category, Publisher, IssueHistory, User
from backend.extensions import bcrypt

def reset_database():
    """Complete database reset"""
    with app.app_context():
        try:
            print("🔄 Starting complete database reset...")
            print("=" * 50)
            
            # Get all existing tables
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print(f"📋 Found {len(existing_tables)} existing tables:")
            for table in existing_tables:
                print(f"  - {table}")
            
            # Drop all existing tables
            print("\n🗑️ Dropping all existing tables...")
            db.drop_all()
            print("✅ All tables dropped")
            
            # Create all application tables
            print("\n🏗️ Creating all application tables...")
            db.create_all()
            print("✅ All tables created")
            
            # Verify tables were created
            inspector = inspect(db.engine)
            new_tables = inspector.get_table_names()
            expected_tables = ['user', 'book', 'member', 'category', 'publisher', 'issue_history', 'library_log']
            
            print("\n📋 Created tables:")
            for table in expected_tables:
                if table in new_tables:
                    print(f"  ✅ {table}")
                else:
                    print(f"  ❌ {table} - MISSING!")
            
            # Create admin user
            print("\n👤 Creating admin user...")
            admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
            
            admin = User(username=admin_username, password=admin_password)
            db.session.add(admin)
            db.session.commit()
            print(f"✅ Admin user created: {admin_username}")
            
            print("\n" + "=" * 50)
            print("🎉 Database reset completed successfully!")
            print("🚀 Your application should now work on cPanel!")
            print(f"📝 Login credentials: {admin_username} / {admin_password}")
            
        except Exception as e:
            print(f"❌ Error during database reset: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    reset_database()
