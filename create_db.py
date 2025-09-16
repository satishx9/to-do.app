"""Utility script to initialize the database tables.

Run with: python create_db.py
"""

from api.app import app, db  # import Flask app and db from api/app.py

with app.app_context():
    db.create_all()
    print("Database and tables created successfully!")
