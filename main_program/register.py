from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
)
from layout import layoutCreator
from dataBase.dataBaseAPI import createUser, userExists


class RegistrationWindow(QWidget):
    def __init__(self, switchToLoginCallback):
        super().__init__()
        self.switchToLoginCallback = switchToLoginCallback
        self.layoutCreator = layoutCreator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Register")

        layoutDict = self.layoutCreator.createRegisterLayout()

        self.layout = layoutDict['layout']
        self.loginButton = layoutDict['loginButton']
        self.registerButton = layoutDict['registerButton']
        self.usernameEdit = layoutDict['usernameEdit']
        self.passwordEdit = layoutDict['passwordEdit']
        self.emailEdit = layoutDict['emailEdit']
        self.ageEdit = layoutDict['ageEdit']
        self.passwordRepeatEdit = layoutDict['passwordRepeatEdit']
        self.setLayout(self.layout)

        # Connect the register button to the register function
        self.loginButton.clicked.connect(self.switchToLoginCallback)
        self.registerButton.clicked.connect(self.register)

    def register(self):
        email = self.emailEdit.text()
        age = self.ageEdit.text()
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        passwordRepeat = self.passwordRepeatEdit.text()

        # Basic validation
        if not (email and age and username and password):
            QMessageBox.warning(self, "Register", "All fields are required.")
            return

        if password != passwordRepeat:
            QMessageBox.warning(self, "Register", "Passwords do not match.")
            return

        # Check if the user already exists
        if userExists(username, email):
            QMessageBox.warning(self, "Register", "User with the same username or email already registered.")
            return
        if (createUser(username, password, email, age)):
            QMessageBox.information(self, "Register", "Registration successful.")
            self.switchToLoginCallback()
