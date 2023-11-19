from PyQt5.QtWidgets import QWidget, QMessageBox
from layout import layoutCreator
from dataBase.dataBaseAPI import loginAttempt


class LoginWindow(QWidget):
    def __init__(self, switchToRegisterCallback, switchToPredictionCallback):
        super().__init__()
        self.switchToRegisterCallback = switchToRegisterCallback
        self.switchToPredictionCallback = switchToPredictionCallback
        self.layoutCreator = layoutCreator()
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

        userID = loginAttempt(username, password)
        if userID is not None:
            self.userID = userID
            self.switchToPredictionCallback()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password.')
