#!/usr/bin/env python3
"""
Database setup script for the name lookup application.
This script creates the MySQL database and populates it with sample data.

Prerequisites:
- MySQL server must be running
- Update DB_CONFIG with your MySQL credentials
"""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySecurePass123',  # MySQL root password
}

# Sample names to insert
SAMPLE_NAMES = [
    'Alice',
    'Bob',
    'Charlie',
    'Diana',
    'Eve',
    'Frank',
    'Grace',
    'Henry',
    'Ivy',
    'Jack',
]

def create_database_and_table():
    """Create the database and names table."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create database
        print("Creating database 'name_db'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS name_db")
        print("✓ Database created or already exists")
        
        # Select the database
        cursor.execute("USE name_db")
        
        # Create table
        print("Creating 'names' table...")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS names (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        print("✓ Table created or already exists")
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"✗ Error: {e}")
        return False

def insert_sample_data():
    """Insert sample names into the database."""
    try:
        config = DB_CONFIG.copy()
        config['database'] = 'name_db'
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("Inserting sample names...")
        insert_query = "INSERT IGNORE INTO names (name) VALUES (%s)"
        
        cursor.executemany(insert_query, [(name,) for name in SAMPLE_NAMES])
        connection.commit()
        
        print(f"✓ Inserted {cursor.rowcount} names into database")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"✗ Error: {e}")
        return False

def show_database_contents():
    """Display all names in the database."""
    try:
        config = DB_CONFIG.copy()
        config['database'] = 'name_db'
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM names")
        rows = cursor.fetchall()
        
        print("\nNames in database:")
        for row in rows:
            print(f"  - {row[1]}")  # row[1] is the name column
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    print("=== Name Lookup Database Setup ===\n")
    
    if create_database_and_table():
        if insert_sample_data():
            show_database_contents()
            print("\n✓ Database setup complete!")
            print("\nNext steps:")
            print("1. Update DB_CONFIG in main.py with your MySQL credentials")
            print("2. Run: .venv/bin/python main.py")
            print("3. Open http://localhost:5000 in your browser")
        else:
            print("\n✗ Failed to insert sample data")
    else:
        print("\n✗ Failed to create database and table")
