import sqlite3

# Connect to the database file (it will be created if it doesn't exist)
conn = sqlite3.connect('diabetesPredictionApp.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,
    PasswordHash TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    Age INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Predictions (
    PredictionID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER,
    PredictionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    DataInput TEXT, -- JSON string or separate columns for each input feature
    PredictionResult TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
)
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()
