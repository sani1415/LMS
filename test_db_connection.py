#!/usr/bin/env python3
"""
Simple Database Connection Test
Run this to test your database connection directly
"""

import os
import pymysql

def test_connection():
    """Test database connection with detailed error reporting"""
    print("🔍 Testing Database Connection...")
    
    # Get connection parameters
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    
    print(f"Host: {db_host}")
    print(f"User: {db_user}")
    print(f"Database: {db_name}")
    print(f"Password: {'*' * len(db_password) if db_password else 'NOT SET'}")
    
    if not all([db_user, db_password, db_host, db_name]):
        print("❌ Missing environment variables!")
        return False
    
    try:
        print("\n🔌 Attempting connection...")
        
        # Try connection with detailed error handling
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            charset='utf8mb4',
            connect_timeout=30,
            read_timeout=30,
            write_timeout=30
        )
        
        print("✅ Connection successful!")
        
        # Test a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        print(f"✅ Query test successful: {result}")
        
        # Check if tables exist
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ Found {len(tables)} tables in database")
        
        cursor.close()
        connection.close()
        
        print("🎉 Database connection test PASSED!")
        return True
        
    except pymysql.Error as e:
        print(f"❌ MySQL Error: {e}")
        print(f"Error Code: {e.args[0] if e.args else 'Unknown'}")
        
        if "Access denied" in str(e):
            print("🔧 FIX: Check username and password")
        elif "Unknown database" in str(e):
            print("🔧 FIX: Database doesn't exist - create it in cPanel")
        elif "Can't connect" in str(e):
            print("🔧 FIX: Check host address and network connectivity")
        
        return False
        
    except Exception as e:
        print(f"❌ General Error: {e}")
        return False

if __name__ == '__main__':
    test_connection()
