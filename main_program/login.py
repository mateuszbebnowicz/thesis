from PyQt5.QtWidgets import QWidget, QMessageBox
from layout import layoutCreator
from security import loginAttempt


class LoginWindow(QWidget):
    def __init__(self, switchToRegisterCallback, switchToPredictionCallback, setCurrentUser):
        super().__init__()
        self.switchToRegisterCallback = switchToRegisterCallback
        self.switchToPredictionCallback = switchToPredictionCallback
        self.setCurrentUser = setCurrentUser
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
            self.setCurrentUser(userID)
            self.switchToPredictionCallback()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password.')
