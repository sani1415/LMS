#!/usr/bin/env python3
"""
Database Schema Fix Script for cPanel Deployment
This script will update the database schema to match the current models.
Run this on cPanel to fix schema mismatches.
"""

import os
import sys
from sqlalchemy import text, inspect

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from backend.models import db, LibraryLog, Member, Book, Category, Publisher, IssueHistory, User
from backend.extensions import bcrypt

def check_table_exists(table_name):
    """Check if a table exists in the database"""
    with app.app_context():
        inspector = inspect(db.engine)
        return table_name in inspector.get_table_names()

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    with app.app_context():
        inspector = inspect(db.engine)
        columns = inspector.get_columns(table_name)
        return any(col['name'] == column_name for col in columns)

def fix_library_log_table():
    """Fix the library_log table schema"""
    with app.app_context():
        try:
            # Check if table exists
            if not check_table_exists('library_log'):
                print("Creating library_log table...")
                LibraryLog.__table__.create(db.engine, checkfirst=True)
                print("✅ library_log table created")
            else:
                print("✅ library_log table exists")
                
            # Check if id column exists
            if not check_column_exists('library_log', 'id'):
                print("Adding id column to library_log table...")
                db.engine.execute(text("ALTER TABLE library_log ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST"))
                print("✅ id column added to library_log table")
            else:
                print("✅ id column exists in library_log table")
                
        except Exception as e:
            print(f"❌ Error fixing library_log table: {e}")

def fix_members_table():
    """Fix the members table schema"""
    with app.app_context():
        try:
            if not check_table_exists('member'):
                print("Creating member table...")
                Member.__table__.create(db.engine, checkfirst=True)
                print("✅ member table created")
            else:
                print("✅ member table exists")
                
        except Exception as e:
            print(f"❌ Error fixing member table: {e}")

def fix_all_tables():
    """Create all tables if they don't exist"""
    with app.app_context():
        try:
            print("Creating all tables...")
            
            # Drop existing alembic_version table if it exists (we don't need Flask-Migrate)
            try:
                db.engine.execute(text("DROP TABLE IF EXISTS alembic_version"))
                print("✅ Removed alembic_version table")
            except:
                pass
                
            # Drop initialization_marker table if it exists
            try:
                db.engine.execute(text("DROP TABLE IF EXISTS initialization_marker"))
                print("✅ Removed initialization_marker table")
            except:
                pass
            
            # Create all application tables
            db.create_all()
            print("✅ All application tables created/updated")
            
            # Verify tables were created
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            expected_tables = ['user', 'book', 'member', 'category', 'publisher', 'issue_history', 'library_log']
            
            print("\n📋 Created tables:")
            for table in expected_tables:
                if table in tables:
                    print(f"  ✅ {table}")
                else:
                    print(f"  ❌ {table} - MISSING!")
                    
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            import traceback
            traceback.print_exc()

def create_admin_user():
    """Create admin user if it doesn't exist"""
    with app.app_context():
        try:
            admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
            existing_admin = User.query.filter_by(username=admin_username).first()
            
            if not existing_admin:
                admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
                admin = User(username=admin_username, password=admin_password)
                db.session.add(admin)
                db.session.commit()
                print(f"✅ Admin user created: {admin_username}")
            else:
                print(f"✅ Admin user already exists: {admin_username}")
                
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")

def main():
    """Main function to fix database schema"""
    print("🔧 Starting cPanel Database Schema Fix...")
    print("=" * 50)
    
    try:
        # Fix specific tables
        fix_library_log_table()
        fix_members_table()
        
        # Create all tables to ensure they exist
        fix_all_tables()
        
        # Create admin user
        create_admin_user()
        
        print("=" * 50)
        print("✅ Database schema fix completed successfully!")
        print("🚀 Your application should now work on cPanel!")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
