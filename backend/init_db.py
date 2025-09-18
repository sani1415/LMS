#!/usr/bin/env python3
"""
Database initialization script for Library Management System
Uses environment variables for DB credentials
"""

import os
import sys

# Ensure parent folder (where app.py lives) is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from backend.extensions import db
from backend.models import Book, Member, Category, Publisher, LibraryLog


def create_sample_data():
    """Create sample data for testing"""
    categories = [
        Category(name='Fiction'),
        Category(name='Non-Fiction'),
        Category(name='Science'),
        Category(name='Technology'),
        Category(name='History'),
        Category(name='Philosophy'),
        Category(name='Literature'),
        Category(name='Art'),
        Category(name='Mathematics'),
        Category(name='Biography')
    ]
    db.session.add_all(categories)
    db.session.commit()

    publishers = [
        Publisher(name='Penguin Books'),
        Publisher(name='Random House'),
        Publisher(name='HarperCollins'),
        Publisher(name='Simon & Schuster'),
        Publisher(name='Macmillan'),
        Publisher(name='Hachette'),
        Publisher(name='Scholastic'),
        Publisher(name='Bloomsbury'),
        Publisher(name='Faber & Faber')
    ]
    db.session.add_all(publishers)
    db.session.commit()

    members = [
        Member(name='John Doe', email='john.doe@example.com'),
        Member(name='Jane Smith', email='jane.smith@example.com'),
        Member(name='Mike Johnson', email='mike.johnson@example.com'),
        Member(name='Sarah Wilson', email='sarah.wilson@example.com'),
        Member(name='David Brown', email='david.brown@example.com')
    ]
    db.session.add_all(members)
    db.session.commit()

    books = [
        Book(
            book_name='The Great Gatsby',
            author='F. Scott Fitzgerald',
            volumes=1,
            category_id=1,
            publisher_id=1,
            year=1925,
            note='Classic American novel',
            status='Available'
        ),
        Book(
            book_name='To Kill a Mockingbird',
            author='Harper Lee',
            volumes=1,
            category_id=1,
            publisher_id=2,
            year=1960,
            note='Pulitzer Prize winner',
            status='Available'
        ),
        Book(
            book_name='1984',
            author='George Orwell',
            volumes=1,
            category_id=1,
            publisher_id=1,
            year=1949,
            note='Dystopian classic',
            status='Available'
        )
    ]
    db.session.add_all(books)
    db.session.commit()

    logs = [
        LibraryLog(content='Library opened for the day. New books arrived from Penguin Books.'),
        LibraryLog(content='Sample data initialized successfully.')
    ]
    db.session.add_all(logs)
    db.session.commit()

    print("✅ Sample data created successfully!")


def init_database():
    """Initialize the database and create sample data"""
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME")

    if not all([db_user, db_pass, db_name]):
        print("❌ Database credentials not found in environment variables!")
        print("Set DB_USER, DB_PASSWORD, DB_HOST, and DB_NAME in cPanel.")
        sys.exit(1)

    print(f"🔗 Connecting to database {db_name} as {db_user}@{db_host}...")

    with app.app_context():
        print("🛠 Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")

        print("🔎 Checking if sample data exists...")
        if not Book.query.first():
            print("📚 Creating sample data...")
            create_sample_data()
        else:
            print("ℹ️ Sample data already exists, skipping...")

        print("🎉 Database initialization completed!")


if __name__ == '__main__':
    init_database()
