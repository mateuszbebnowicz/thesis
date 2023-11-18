from PyQt5.QtWidgets import QWidget, QMessageBox
from layout import Layout


class LoginWindow(QWidget):
    def __init__(self, switchToRegisterCallback, switchToPredictionCallback):
        super().__init__()
        self.switchToRegisterCallback = switchToRegisterCallback
        self.switchToPredictionCallback = switchToPredictionCallback
        self.layoutCreator = Layout()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        layoutDict = self.layoutCreator.createLoginLayout()

        self.layout = layoutDict['layout']
        self.loginButton = layoutDict['loginButton']
        self.registerButton = layoutDict['registerButton']
        self.usernameEdit = layoutDict['usernameEdit']
        self.passwordEdit = layoutDict['passwordEdit']

        self.setLayout(self.layout)

        # Connect buttons to their functions
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.switchToRegisterCallback)

    def login(self):
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        if self.credentialsAreValid(username, password):  # Replace with your actual validation logic
            self.switchToPredictionCallback()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password.')
        # You should add the logic to verify credentials here

    def credentialsAreValid(self, username, password):
        return True
