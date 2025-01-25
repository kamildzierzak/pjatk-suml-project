import sqlite3

import hashlib
import time

DB_PATH = "db/database.db"

def init_db():
    dbConnection = sqlite3.connect(DB_PATH)
    dbCursor = dbConnection.cursor()

    dbCursor.execute("""
                     CREATE TABLE IF NOT EXISTS users (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT UNIQUE NOT NULL, 
                     password_hash TEXT NOT NULL
                     )
                     """)
    
    dbCursor.execute("""
                    CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL, 
                    timestamp TEXT NOT NULL,
                    image_name TEXT,
                    predicted_class TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                    )
                     """)
    
    dbConnection.commit()
    dbConnection.close()

def get_db_connection():
    dbConnection = sqlite3.connect(DB_PATH)
    return dbConnection


def create_user(username, password):
    dbConnection = get_db_connection()
    dbCursor = dbConnection.cursor()

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    dbCursor.execute("""
                     INSERT INTO users (username, password_hash) 
                     VALUES (?, ?)
                     """, (username, password_hash))

    dbConnection.commit()
    dbConnection.close()

def check_user(username, password):
    dbConnection = get_db_connection()
    dbCursor = dbConnection.cursor()

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    dbCursor.execute("""
                     SELECT id 
                     FROM users 
                     WHERE username = ? AND password_hash = ?
                     """, (username, password_hash))

    row = dbCursor.fetchone()
    dbConnection.close()

    if row:
        return row[0]
    else:
        return None
    
def save_prediction(user_id, image_name, predicted_class):
    dbConnection = get_db_connection()
    dbCursor = dbConnection.cursor()

    # Timestamp in format "YYYY-MM-DD HH:MM:SS"
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    dbCursor.execute("""
                     INSERT INTO predictions (user_id, timestamp, image_name, predicted_class) 
                     VALUES (?, ?, ?, ?)
                     """, (user_id, timestamp, image_name, predicted_class))

    dbConnection.commit()
    dbConnection.close()

def get_predictions(user_id):
    dbConnection = get_db_connection()
    dbCursor = dbConnection.cursor()

    dbCursor.execute("""
                    SELECT timestamp, image_name, predicted_class
                    FROM predictions
                    WHERE user_id = ?
                    ORDER BY id DESC
                    """, (user_id,))
    
    rows = dbCursor.fetchall()
    dbConnection.close()
    
    return rows