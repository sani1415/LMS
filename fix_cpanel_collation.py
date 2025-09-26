#!/usr/bin/env python3
"""
CPANEL DATABASE COLLATION FIX SCRIPT
Fixes the collation mismatch issue on cPanel
"""

import os
import pymysql
from app import app, db
from backend.models import Book, User, Category, Publisher, Member, IssueHistory, LibraryLog

def fix_cpanel_collation():
    """Fix collation issues on cPanel database"""
    print("🔧 Fixing cPanel database collation issues...")
    
    # Get database connection details
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    
    if not all([db_user, db_password, db_host, db_name]):
        print("❌ Missing database environment variables")
        return False
    
    try:
        # Connect to database
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        
        print("✅ Connected to database")
        
        # Fix database collation
        print("🔧 Setting database collation to utf8mb4_unicode_ci...")
        cursor.execute(f"ALTER DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"🔧 Fixing collation for {len(tables)} tables...")
        
        for table in tables:
            table_name = table[0]
            print(f"  📝 Fixing table: {table_name}")
            
            # Fix table collation
            cursor.execute(f"ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            
            # Get all text columns and fix their collation
            cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE, COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = %s 
                AND DATA_TYPE IN ('varchar', 'char', 'text', 'mediumtext', 'longtext')
            """, (db_name, table_name))
            
            columns = cursor.fetchall()
            for column_name, data_type, max_length, is_nullable, default_value in columns:
                # Build the column definition properly
                if data_type == 'varchar':
                    column_def = f"VARCHAR({max_length})"
                elif data_type == 'char':
                    column_def = f"CHAR({max_length})"
                else:
                    column_def = data_type.upper()
                
                # Add NULL/NOT NULL
                null_clause = "NULL" if is_nullable == 'YES' else "NOT NULL"
                
                # Add default value if exists
                default_clause = ""
                if default_value is not None:
                    if isinstance(default_value, str):
                        default_clause = f" DEFAULT '{default_value}'"
                    else:
                        default_clause = f" DEFAULT {default_value}"
                
                # Execute the ALTER TABLE command
                alter_sql = f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} {column_def} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci {null_clause}{default_clause}"
                cursor.execute(alter_sql)
        
        connection.commit()
        print("✅ Database collation fixed successfully!")
        
        # Test the fix
        print("🧪 Testing collation fix...")
        with app.app_context():
            # Try a simple query that was failing
            test_book = Book.query.first()
            if test_book:
                print("✅ Database queries working correctly")
            else:
                print("ℹ️  No books found (database is empty)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing collation: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == '__main__':
    success = fix_cpanel_collation()
    if success:
        print("\n🎉 Collation fix completed successfully!")
        print("📚 You can now import CSV files without collation errors!")
    else:
        print("\n❌ Collation fix failed. Please check the error messages above.")
