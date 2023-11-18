from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
)
from layout import Layout


class RegistrationWindow(QWidget):
    def __init__(self, switchToLoginCallback):
        super().__init__()
        self.switchToLoginCallback = switchToLoginCallback
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Register")
        self.Layout = Layout()
        layoutDict = self.Layout.createRegisterLayout()

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
        # Implement registration logic here
        # email = self.emailEdit.text()
        # age = self.ageEdit.text()
        # username = self.usernameEdit.text()
        # password = self.passwordEdit.text()
        # passwordRepeat = self.passwordRepeatEdit.text()

        # You should add validation logic here

        QMessageBox.information(self, "Register", "Registration Attempted")
