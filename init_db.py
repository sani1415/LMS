#!/usr/bin/env python3
"""
Database initialization script for Library Management System
Run this script to create the database and populate it with sample data
"""

from app import app
from extensions import db
from models import Book, Member, Category, Publisher, LibraryLog

def create_sample_data():
    """Create sample data for testing"""
    # Create categories
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
    
    for category in categories:
        db.session.add(category)
    db.session.commit()
    
    # Create publishers
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
    
    for publisher in publishers:
        db.session.add(publisher)
    db.session.commit()
    
    # Create members
    members = [
        Member(name='John Doe', email='john.doe@example.com'),
        Member(name='Jane Smith', email='jane.smith@example.com'),
        Member(name='Mike Johnson', email='mike.johnson@example.com'),
        Member(name='Sarah Wilson', email='sarah.wilson@example.com'),
        Member(name='David Brown', email='david.brown@example.com')
    ]
    
    for member in members:
        db.session.add(member)
    db.session.commit()
    
    # Create books
    books = [
        Book(
            book_name='The Great Gatsby',
            author='F. Scott Fitzgerald',
            volumes=1,
            category_id=1,  # Fiction
            publisher_id=1,  # Penguin Books
            year=1925,
            note='Classic American novel',
            status='Available'
        ),
        Book(
            book_name='To Kill a Mockingbird',
            author='Harper Lee',
            volumes=1,
            category_id=1,  # Fiction
            publisher_id=2,  # Random House
            year=1960,
            note='Pulitzer Prize winner',
            status='Available'
        ),
        Book(
            book_name='1984',
            author='George Orwell',
            volumes=1,
            category_id=1,  # Fiction
            publisher_id=1,  # Penguin Books
            year=1949,
            note='Dystopian classic',
            status='Available'
        )
    ]
    
    for book in books:
        db.session.add(book)
    db.session.commit()
    
    # Create library log entries
    logs = [
        LibraryLog(content='Library opened for the day. New books arrived from Penguin Books.'),
        LibraryLog(content='Sample data initialized successfully.')
    ]
    
    for log in logs:
        db.session.add(log)
    db.session.commit()
    
    print("Sample data created successfully!")

def init_database():
    """Initialize the database and create sample data"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        print("Checking if sample data exists...")
        if not Book.query.first():
            print("Creating sample data...")
            create_sample_data()
            print("Sample data created successfully!")
        else:
            print("Sample data already exists, skipping...")
        
        print("Database initialization completed!")

if __name__ == '__main__':
    init_database()