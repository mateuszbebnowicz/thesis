import bcrypt
import random
import string
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dataBase.dataBaseAPI import (
    getUserIDPasswordByUsername,
    setResetToken,
    getUserByToken,
    getEmailByUserID,
    setNewPassword,
)
from PyQt5.QtWidgets import QLineEdit, QInputDialog, QMessageBox


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


def resetPasswordProcedure(parent, userID):
    if userID:
        token, expirationTime = generateResetToken()
        setResetToken(userID, token, expirationTime)
        email = getEmailByUserID(userID)
        # Send the email with the token
        if sendResetEmail(email, token):
            imputedToken, ok = QInputDialog.getText(
                parent,
                "Password Reset",
                "Password token was sent to your email \nEnter the reset token:",
            )
            if ok and imputedToken:
                openChangePasswordDialog(parent, imputedToken)
            else:
                QMessageBox.warning(parent, "Error", "Password reset was not succesful")
        else:
            QMessageBox.warning(parent, "Error", "Email was not send")
    else:
        QMessageBox.warning(parent, "Error", "No user is currently logged in.")


def verifyToken(parent, token):
    # Verify if the token is valid
    # If valid, open the change password dialog
    if getUserByToken(token):
        return True
    else:
        QMessageBox.warning(parent, "Error", "Invalid or expired token.")
        return False


def openChangePasswordDialog(parent, token):
    if verifyToken(parent, token):
        # Open a dialog to change the password
        newPassword, ok = QInputDialog.getText(
            parent, "Password Reset", "Enter your new password:", QLineEdit.Password
        )
        if ok and newPassword:
            confirmNewPassword, ok = QInputDialog.getText(
                parent,
                "Password Reset",
                "Confirm your new password:",
                QLineEdit.Password,
            )
            if ok and newPassword == confirmNewPassword:
                response = resetPassword(token, newPassword)
                QMessageBox.information(parent, "Password Reset", response)
            else:
                QMessageBox.warning(parent, "Error", "Passwords do not match.")


def resetPassword(token, newPassword):
    hashedPassword = hashPassword(newPassword).decode("utf-8")
    if setNewPassword(token, hashedPassword):
        return "Password reset successfully."
    else:
        return "Failed to reset password. Please try again."


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
    return False


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
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")  # Log or print the exception
        return False


def sendRegistrationConfirmationEmail(email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use 465 for SSL
    smtp_user = "diabetespredictorpassreset@gmail.com"  # Your Gmail address
    smtp_password = "eage krqg hmit juzg"  # Your Gmail password or App Password

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = email
    msg["Subject"] = "Registration Successful"

    body = "Congratulations! You have successfully registered with our application."
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return True  # email sent successfully
    except Exception as e:
        print(f"Failed to send email: {e}")  # Log or print the exception
        return False  # email failed to send
