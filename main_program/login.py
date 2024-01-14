from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog
from layout import layoutCreator
from security import loginAttempt, resetPasswordProcedure
from dataBase.dataBaseAPI import getUserIDByEmail


class LoginWindow(QWidget):
    def __init__(
        self, switchToRegisterCallback, switchToPredictionCallback, setCurrentUser
    ):
        super().__init__()
        self.switchToRegisterCallback = switchToRegisterCallback
        self.switchToPredictionCallback = switchToPredictionCallback
        self.setCurrentUser = setCurrentUser
        self.layoutCreator = layoutCreator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        layoutDict = self.layoutCreator.createLoginLayout()

        self.layout = layoutDict["layout"]
        self.loginButton = layoutDict["loginButton"]
        self.registerButton = layoutDict["registerButton"]
        self.usernameEdit = layoutDict["usernameEdit"]
        self.passwordEdit = layoutDict["passwordEdit"]
        self.forgotPasswordLabel = layoutDict["forgotPasswordLabel"]

        self.setLayout(self.layout)

        # Connect buttons to their functions
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.switchToRegisterCallback)
        self.forgotPasswordLabel.clicked.connect(self.onForgetPasswordClicked)

    def onForgetPasswordClicked(self):
        userID = self.getUserIDFromImputedEmail()
        if userID:
            resetPasswordProcedure(self, userID)
        else:
            QMessageBox.warning(self, "Error", "Email not found.")

    def getUserIDFromImputedEmail(self):
        email, ok = QInputDialog.getText(
            self,
            "Password Reset",
            "Enter your email:",
        )
        if ok and email:
            userID = getUserIDByEmail(email)
            return userID
        return None

    def login(self):
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()

        userID = loginAttempt(username, password)
        if userID is not None:
            self.setCurrentUser(userID)
            self.switchToPredictionCallback()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
