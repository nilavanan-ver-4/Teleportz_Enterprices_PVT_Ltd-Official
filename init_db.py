#!/usr/bin/env python3
"""
Database initialization script for Teleportz Admin Portal
Creates all necessary tables in site.db
"""

import os
import sys
from app import create_app, db, User

def init_database():
    """Initialize the database with all tables"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully")
        
        # Check if admin user exists, if not create one
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin')
            admin_user.set_password('admin123')  # Change this in production
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created (username: admin, password: admin123)")
        else:
            print("Admin user already exists")
        
        print("\nDatabase initialization completed!")
        print("You can now run the admin portal with: python admin/app.py")

if __name__ == '__main__':
    init_database()