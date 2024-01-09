import bcrypt
import random
import string
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dataBase.dataBaseAPI import getUserIDPasswordByUsername


def check_password(hashedPassword, user_password):
    # Convert the user password to bytes
    user_passwordBytes = user_password.encode("utf-8")

    # Check if the password provided by the user matches the hashed password
    return bcrypt.checkpw(user_passwordBytes, hashedPassword)


def hashPassword(password):
    # Convert the password to bytes if it's not already
    passwordBytes = password.encode("utf-8")

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(passwordBytes, salt)

    return hashedPassword


def generateResetToken():
    # Generate a random token
    token = "".join(random.choices(string.ascii_letters + string.digits, k=20))

    # Set the token expiration time (e.g., 24 hours from now)
    expirationTime = datetime.datetime.now() + datetime.timedelta(hours=24)

    return token, expirationTime


def loginAttempt(username, password):
    userID, hashedPassword = getUserIDPasswordByUsername(username)
    if userID:
        # Ensure hashedPassword is in byte format for bcrypt comparison
        hashedPasswordBytes = hashedPassword.encode("utf-8")
        # Convert the provided password to bytes
        passwordBytes = password.encode("utf-8")
        # Use bcrypt to compare the provided password with the hashed password
        if bcrypt.checkpw(passwordBytes, hashedPasswordBytes):
            return userID


def sendResetEmail(email, token):
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
