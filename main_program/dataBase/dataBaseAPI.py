import sqlite3
import random
import string
import datetime
import bcrypt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def dbConnection():
    return sqlite3.connect("diabetesPredictionApp.db")


def hash_password(password):
    # Convert the password to bytes if it's not already
    password_bytes = password.encode("utf-8")

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password


def isTokenValid(token):
    with dbConnection() as conn:
        cursor = conn.cursor()

        # Checking if the token exists in the database and is not expired
        cursor.execute(
            "SELECT UserID FROM Users WHERE ResetToken = ? AND TokenExpiry > ?",
            (token, datetime.datetime.now()),
        )
        result = cursor.fetchone()

        return result is not None


def check_password(hashed_password, user_password):
    # Convert the user password to bytes
    user_password_bytes = user_password.encode("utf-8")

    # Check if the password provided by the user matches the hashed password
    return bcrypt.checkpw(user_password_bytes, hashed_password)


def generate_reset_token(email):
    # Generate a random token
    token = "".join(random.choices(string.ascii_letters + string.digits, k=20))

    # Set the token expiration time (e.g., 24 hours from now)
    expiration_time = datetime.datetime.now() + datetime.timedelta(hours=24)

    conn = dbConnection()
    cursor = conn.cursor()
    # Check if user exists
    cursor.execute("SELECT UserID FROM Users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if not user:
        return "User not found"
    # Store the token and expiration time in the database
    cursor.execute(
        "UPDATE Users SET ResetToken = ?, TokenExpiry = ? WHERE email = ?",
        (token, expiration_time, email),
    )
    conn.commit()

    # Send the email with the token
    send_reset_email(email, token)


def send_reset_email(email, token):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use 465 for SSL
    smtp_user = "diabetespredictorpassreset@gmail.com"  # Your Gmail address
    smtp_password = "eage krqg hmit juzg"  # Your Gmail password or App Password

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = email
    msg["Subject"] = "Password Reset Request"

    body = f"Your password reset token is: {token}\nPlease use this token to reset your password."
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return "Email sent successfully."
    except Exception as e:
        print(f"Failed to send email: {e}")  # Log or print the exception
        return f"Failed to send email: {e}"


def reset_password_in_db(token, new_password):
    hashed_password = hash_password(new_password).decode("utf-8")

    with dbConnection() as conn:
        cursor = conn.cursor()

        # Update the user's password and clear the reset token and expiry
        cursor.execute(
            "UPDATE Users SET PasswordHash = ?, ResetToken = NULL, TokenExpiry = NULL WHERE ResetToken = ?",
            (hashed_password, token),
        )
        affected_rows = cursor.rowcount

        conn.commit()

        return affected_rows > 0  # Returns True if the password was successfully reset


def createUser(username, password, email):
    conn = dbConnection()
    cursor = conn.cursor()

    # Hash the password before storing it
    hashed_password = hash_password(password)
    hashed_password_str = hashed_password.decode("utf-8")

    print(f"User created Username: {username}, Email: {email}")
    cursor.execute(
        "INSERT INTO Users (Username, PasswordHash, Email) VALUES (?, ?, ?)",
        (username, hashed_password_str, email),
    )

    conn.commit()
    conn.close()
    return True


def loginAttempt(username, password):
    with dbConnection() as conn:
        cursor = conn.cursor()

        # Retrieve the hashed password from the database
        cursor.execute(
            "SELECT UserID, PasswordHash FROM Users WHERE Username = ?", (username,)
        )
        result = cursor.fetchone()

        if result:
            userID, hashed_password = result

            # Ensure hashed_password is in byte format for bcrypt comparison
            hashed_password_bytes = hashed_password.encode("utf-8")

            # Convert the provided password to bytes
            password_bytes = password.encode("utf-8")

            # Use bcrypt to compare the provided password with the hashed password
            if bcrypt.checkpw(password_bytes, hashed_password_bytes):
                return userID

    return None


def storePrediction(userId, dataInput, predictionResult):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Predictions (UserID, DataInput, PredictionResult) VALUES (?, ?, ?)",
        (userId, dataInput, predictionResult),
    )

    conn.commit()
    conn.close()


def getUserData(userID):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE UserID = ?", (userID,))
    userData = cursor.fetchone()

    conn.close()
    return userData


def getUserEmail(userID):
    # Implement a function to fetch the email for the given user ID from the database
    with dbConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Email FROM Users WHERE UserID = ?", (userID,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the email
        else:
            return None


def getPastResults(userID):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Predictions WHERE UserID = ?", (userID,))
    predictions = cursor.fetchall()

    conn.close()
    return predictions


def userExists(username, email):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Users WHERE Username = ? OR Email = ?", (username, email)
    )
    user = cursor.fetchone()

    conn.close()
    return user is not None
