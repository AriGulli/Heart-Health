# static/database/database.py
import sqlite3
from flask import g

DATABASE = 'static/database/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = Database()
    return db

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL
            );
        ''')
        self.conn.commit()

    def insert_email(self, email):
        try:
            self.cursor.execute('INSERT INTO emails (email) VALUES (?)', (email,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print("Error:", e)
            return False  # Return False if the email already exists

    def fetch_all_emails(self):
        self.cursor.execute('SELECT email FROM emails')
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()
