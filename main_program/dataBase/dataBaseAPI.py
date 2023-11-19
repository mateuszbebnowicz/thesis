import sqlite3


def dbConnection():
    return sqlite3.connect('diabetesPredictionApp.db')


def createUser(username, passwordHash, email, age):
    conn = dbConnection()
    cursor = conn.cursor()
    print(f"User created Username: {username}, Email: {email}")
    cursor.execute("INSERT INTO Users (Username, PasswordHash, Email, Age) VALUES (?, ?, ?, ?)",
                   (username, passwordHash, email, age))

    conn.commit()
    conn.close()
    return True


def loginAttempt(username, passwordHash):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT UserID FROM Users WHERE Username = ? AND PasswordHash = ?", (username, passwordHash))
    result = cursor.fetchone()

    conn.close()
    if result:
        userID, = result
        return userID
    else:
        return None


def storePrediction(userId, dataInput, predictionResult):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Predictions (UserID, DataInput, PredictionResult) VALUES (?, ?, ?)",
                   (userId, dataInput, predictionResult))

    conn.commit()
    conn.close()


def getUserData(username):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE Username = ?", (username,))
    user_data = cursor.fetchone()

    conn.close()
    return user_data


def getPastResults(userId):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Predictions WHERE UserID = ?", (userId,))
    predictions = cursor.fetchall()

    conn.close()
    return predictions


def userExists(username, email):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE Username = ? OR Email = ?", (username, email))
    user = cursor.fetchone()

    conn.close()
    return user is not None
