from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
)
from layout import LayoutCreator
from dataBase.dataBaseAPI import createUser, getUserByUsernameOrEmail
from security import hashPassword, sendRegistrationConfirmationEmail


class RegistrationWindow(QWidget):
    def __init__(self, switchToLoginCallback):
        super().__init__()
        self.switchToLoginCallback = switchToLoginCallback
        self.layoutCreator = LayoutCreator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Register")

        layoutDict = self.layoutCreator.createRegisterLayout()

        self.layout = layoutDict["layout"]
        self.loginButton = layoutDict["loginButton"]
        self.registerButton = layoutDict["registerButton"]
        self.usernameEdit = layoutDict["usernameEdit"]
        self.passwordEdit = layoutDict["passwordEdit"]
        self.emailEdit = layoutDict["emailEdit"]
        self.passwordRepeatEdit = layoutDict["passwordRepeatEdit"]
        self.setLayout(self.layout)

        # Connect the register button to the register function
        self.loginButton.clicked.connect(self.switchToLoginCallback)
        self.registerButton.clicked.connect(self.register)

    def passwordRequirements(self, password, passwordRepeat):
        if password != passwordRepeat:
            QMessageBox.warning(self, "Register", "Passwords do not match.")
            return False

        # Additional password complexity validation
        if len(password) < 8:
            QMessageBox.warning(
                self, "Register", "Password must be at least 8 characters long."
            )
            return False

        if (
            not any(char.isdigit() for char in password)
            or not any(char.isupper() for char in password)
            or not any(char.islower() for char in password)
            or not any(char in "!@#$%^&*()-_+=" for char in password)
        ):
            QMessageBox.warning(
                self,
                "Register",
                "Password must contain a mix of uppercase letters, lowercase letters, digits, and special characters.",
            )
            return False

        return True

    def requirements(self, email, username, password, passwordRepeat):
        if not (email and username and password):
            QMessageBox.warning(self, "Register", "All fields are required.")
            return False

        # Check if the user already exists
        if getUserByUsernameOrEmail(username, email):
            QMessageBox.warning(
                self,
                "Register",
                "User with the same username or email already registered.",
            )
            return False

        if not self.passwordRequirements(password, passwordRepeat):
            return False

        if sendRegistrationConfirmationEmail(email):
            QMessageBox.information(
                self, "Register", "Confiramtion email was sent to you."
            )
            return True
        else:
            QMessageBox.warning(self, "Register", "email is not valid")
            return False

    def register(self):
        email = self.emailEdit.text()
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        passwordRepeat = self.passwordRepeatEdit.text()

        # Password validation
        if self.requirements(email, username, password, passwordRepeat):
            # Hash the password before storing it
            hashedPassword = hashPassword(password)
            hashedPassword_str = hashedPassword.decode("utf-8")

            if createUser(username, hashedPassword_str, email):
                QMessageBox.information(self, "Register", "Registration successful.")
                self.switchToLoginCallback()
