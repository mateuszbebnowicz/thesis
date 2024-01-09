import sqlite3
import datetime


def dbConnection():
    return sqlite3.connect("diabetesPredictionApp.db")


def getUserByToken(token):
    with dbConnection() as conn:
        cursor = conn.cursor()

        # Checking if the token exists in the database and is not expired
        cursor.execute(
            "SELECT UserID FROM Users WHERE ResetToken = ? AND TokenExpiry > ?",
            (token, datetime.datetime.now()),
        )
        result = cursor.fetchone()

        return result is not None


def getUserIDPasswordByUsername(username):
    with dbConnection() as conn:

        cursor = conn.cursor()

        # Retrieve the hashed password from the database
        cursor.execute(
            "SELECT UserID, PasswordHash FROM Users WHERE Username = ?", (username,)
        )

        return cursor.fetchone()


def getToken(userID):
    with dbConnection() as conn:
        cursor = conn.cursor()
        # Check if user exists
        cursor.execute("SELECT ResetToken FROM Users WHERE UserID = ?", (userID,))
        token = cursor.fetchone()
        if not token:
            return "Token not found"

        return token


def getUserData(userID):
    with dbConnection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE UserID = ?", (userID,))
        userData = cursor.fetchone()

        return userData


def getUserEmail(userID):
    with dbConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Email FROM Users WHERE UserID = ?", (userID,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the email
        else:
            return None


def getPreditions(userID):
    with dbConnection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Predictions WHERE UserID = ?", (userID,))
        predictions = cursor.fetchall()

        return predictions


def getUserByEmail(username, email):
    with dbConnection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM Users WHERE Username = ? OR Email = ?", (username, email)
        )
        user = cursor.fetchone()

        return user is not None


def setResetToken(userID, token, expirationTime):
    with dbConnection() as conn:
        cursor = conn.cursor()
        # Store the token and expiration time in the database
        cursor.execute(
            "UPDATE Users SET ResetToken = ?, TokenExpiry = ? WHERE UserID = ?",
            (token, expirationTime, userID),
        )
        conn.commit()


def setNewPassword(token, newPassword):
    with dbConnection() as conn:
        cursor = conn.cursor()

        # Update the user's password and clear the reset token and expiry
        cursor.execute(
            "UPDATE Users SET PasswordHash = ?, ResetToken = NULL, TokenExpiry = NULL WHERE ResetToken = ?",
            (newPassword, token),
        )
        affected_rows = cursor.rowcount

        conn.commit()

        return affected_rows > 0  # Returns True if the password was successfully reset


def createUser(username, password, email):
    with dbConnection() as conn:
        cursor = conn.cursor()

        print(f"User created Username: {username}, Email: {email}")
        cursor.execute(
            "INSERT INTO Users (Username, PasswordHash, Email) VALUES (?, ?, ?)",
            (username, password, email),
        )

        conn.commit()
        return True


def insertPredictions(userId, dataInput, predictionResult):
    with dbConnection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Predictions (UserID, DataInput, PredictionResult) VALUES (?, ?, ?)",
            (userId, dataInput, predictionResult),
        )

        conn.commit()
