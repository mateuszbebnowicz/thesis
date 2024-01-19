import sqlite3
import datetime


def dbConnection():
    return sqlite3.connect("diabetesPredictionApp.db")


def getUserByToken(token):
    with dbConnection() as conn:
        cursor = conn.cursor()

        # Checking if the token exists in the database and is not expired
        cursor.execute(
            "SELECT userID FROM Users WHERE resetToken = ? AND tokenExpiry > ?",
            (token, datetime.datetime.now()),
        )
        result = cursor.fetchone()

        return result is not None


def getUserIDPasswordByUsername(username):
    with dbConnection() as conn:
        cursor = conn.cursor()

        # Retrieve the hashed password from the database
        cursor.execute(
            "SELECT userID, passwordHash FROM Users WHERE username = ?", (username,)
        )

        return cursor.fetchone()


def getToken(userID):
    with dbConnection() as conn:
        cursor = conn.cursor()
        # Check if user exists
        cursor.execute("SELECT resetToken FROM Users WHERE userID = ?", (userID,))
        token = cursor.fetchone()
        if not token:
            return "Token not found"

        return token


def getUserData(userID):
    with dbConnection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE userID = ?", (userID,))
        userData = cursor.fetchone()

        return userData


def getEmailByUserID(userID):
    with dbConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM Users WHERE userID = ?", (userID,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the email
        else:
            return None


def getPreditions(userID):
    with dbConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT
            predictionDate,
            age,
            Bmi,
            hba1cLevel,
            bloodGlucoseLevel,
            predictionResult
            FROM Predictions
            WHERE userID = ?""",
            (userID,),
        )
        predictions = cursor.fetchall()

        predictionDates = []
        ages = []
        bmis = []
        hba1c_levels = []
        blood_glucose_levels = []
        predictionResults = []

        for prediction in predictions:
            (
                predictionDate,
                age,
                bmi,
                hba1c_level,
                blood_glucose_level,
                predictionResult,
            ) = prediction

            predictionDates.append(predictionDate)
            ages.append(age)
            bmis.append(bmi)
            hba1c_levels.append(hba1c_level)
            blood_glucose_levels.append(blood_glucose_level)
            predictionResults.append(predictionResult)

        return (
            predictionDates,
            ages,
            bmis,
            hba1c_levels,
            blood_glucose_levels,
            predictionResults,
        )


def getUserByUsernameOrEmail(username, email):
    with dbConnection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM Users WHERE username = ? OR email = ?", (username, email)
        )
        user = cursor.fetchone()

        return user is not None


def getUserIDByEmail(email):
    with dbConnection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT userID FROM Users WHERE email = ?", (email,))
        user = cursor.fetchone()

        return user is not None


def setResetToken(userID, token, expirationTime):
    with dbConnection() as conn:
        cursor = conn.cursor()
        # Store the token and expiration time in the database
        cursor.execute(
            "UPDATE Users SET resetToken = ?, tokenExpiry = ? WHERE userID = ?",
            (token, expirationTime, userID),
        )
        conn.commit()


def setNewPassword(token, newPassword):
    with dbConnection() as conn:
        cursor = conn.cursor()

        # Update the user's password and clear the reset token and expiry
        cursor.execute(
            "UPDATE Users SET passwordHash = ?, resetToken = NULL, tokenExpiry = NULL WHERE resetToken = ?",
            (newPassword, token),
        )
        affected_rows = cursor.rowcount

        conn.commit()

        return affected_rows > 0  # Returns True if the password was successfully reset


def createUser(username, password, email):
    with dbConnection() as conn:
        cursor = conn.cursor()

        print(f"User created username: {username}, email: {email}")
        cursor.execute(
            "INSERT INTO Users (username, passwordHash, email) VALUES (?, ?, ?)",
            (username, password, email),
        )

        conn.commit()
        return True


def insertPredictions(
    userId, age, bmi, hba1c_level, blood_glucose_level, predictionResult
):
    with dbConnection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Predictions (userID, age, Bmi, hba1cLevel, bloodGlucoseLevel, predictionResult) VALUES (?, ?, ?, ?, ?, ?)",
            (userId, age, bmi, hba1c_level, blood_glucose_level, predictionResult),
        )

        conn.commit()
