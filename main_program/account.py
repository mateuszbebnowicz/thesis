from PyQt5.QtWidgets import QWidget, QMessageBox
from layout import layoutCreator
from dataBase.dataBaseAPI import generate_reset_token, getUserEmail


class AccountWindow(QWidget):
    def __init__(self, switchToLoginCallback, switchToPredictCallback, clearUser, userId):
        super().__init__()
        self.switchToPredictCallback = switchToPredictCallback
        self.switchToLoginCallback = switchToLoginCallback
        self.clearUser = clearUser
        self.userID = userId
        self.layoutCreator = layoutCreator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Account")

        layoutDict = self.layoutCreator.createAccountLayout(self.userID)

        self.layout = layoutDict['layout']
        self.resetPasswordButton = layoutDict['changePasswordButton']
        self.predictionWindowButton = layoutDict['predictionWindowButton']
        self.logoutButton = layoutDict['logoutButton']
        self.setLayout(self.layout)

        self.resetPasswordButton.clicked.connect(self.onResetPasswordClicked)
        self.logoutButton.clicked.connect(lambda: (self.clearUser(), self.switchToLoginCallback()))
        self.predictionWindowButton.clicked.connect(self.switchToPredictCallback)

    def onResetPasswordClicked(self):
        if self.userID:
            email = getUserEmail(self.userID)
            if email:
                response = generate_reset_token(email)
                QMessageBox.information(self, 'Password Reset', response)
            else:
                QMessageBox.warning(self, 'Error', 'Email not found for the user.')
        else:
            QMessageBox.warning(self, 'Error', 'No user is currently logged in.')
