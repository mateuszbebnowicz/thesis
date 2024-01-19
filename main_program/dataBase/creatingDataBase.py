import sqlite3

# Connect to the database file (it will be created if it doesn't exist)
conn = sqlite3.connect("diabetesPredictionApp.db")

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create tables
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    passwordHash VARCHAR(128) NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER,
    resetToken TEXT,
    tokenExpiry TIMESTAMP
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Predictions (
    predictionID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER,
    predictionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    age TEXT,
    Bmi TEXT,
    hba1cLevel TEXT,
    bloodGlucoseLevel TEXT,
    predictionResult TEXT,
    FOREIGN KEY (userID) REFERENCES Users(userID)
)
"""
)


# Commit the changes
conn.commit()

# Close the connection
conn.close()
