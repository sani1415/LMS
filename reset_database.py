#!/usr/bin/env python3
"""
UNIFIED DATABASE RESET SCRIPT
Works for both development and cPanel
"""

import os
import sys
from app import app, db, create_admin_user, create_sample_data
from backend.models import Book, User, Category, Publisher, Member, IssueHistory, LibraryLog

def reset_database():
    """Reset database completely - works everywhere"""
    print("🔄 Resetting database...")
    
    with app.app_context():
        try:
            # Drop all tables
            print("🗑️  Dropping all existing tables...")
            db.drop_all()
            print("✅ All tables dropped successfully")
            
        except Exception as e:
            print(f"⚠️  Warning during table drop: {e}")
            # Continue anyway - tables might not exist
            
        try:
            # Create all tables
            print("🏗️  Creating all tables...")
            db.create_all()
            print("✅ All tables created successfully")
            
            # Create admin user
            print("👤 Creating admin user...")
            create_admin_user()
            print("✅ Admin user created")
            
            # Add sample data
            print("📚 Adding sample data...")
            create_sample_data()
            print("✅ Sample data added")
            
            print("\n🎉 Database reset completed successfully!")
            print("🔑 Admin login: admin / admin123")
            print("📊 Sample data has been added")
            
        except Exception as e:
            print(f"❌ Error during database setup: {e}")
            sys.exit(1)

if __name__ == '__main__':
    reset_database()
