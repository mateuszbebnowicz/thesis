from PyQt5.QtWidgets import QWidget, QLineEdit, QInputDialog, QMessageBox
from layout import layoutCreator
from dataBase.dataBaseAPI import generate_reset_token, reset_password_in_db, isTokenValid, getUserEmail


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
                generate_reset_token(email)
                token, ok = QInputDialog.getText(self, 'Password Reset', 'Password token was sent to your email \nEnter the reset token:')
                if ok and token:
                    self.verifyToken(token)
            else:
                QMessageBox.warning(self, 'Error', 'Email not found for the user.')
        else:
            QMessageBox.warning(self, 'Error', 'No user is currently logged in.')

    def verifyToken(self, token):
        # Verify if the token is valid
        # If valid, open the change password dialog
        if isTokenValid(token):
            self.openChangePasswordDialog(token)
        else:
            QMessageBox.warning(self, 'Error', 'Invalid or expired token.')

    def openChangePasswordDialog(self, token):
        # Open a dialog to change the password
        newPassword, ok = QInputDialog.getText(self, 'Password Reset', 'Enter your new password:', QLineEdit.Password)
        if ok and newPassword:
            confirmNewPassword, ok = QInputDialog.getText(self, 'Password Reset', 'Confirm your new password:', QLineEdit.Password)
            if ok and newPassword == confirmNewPassword:
                response = self.resetPassword(token, newPassword)
                QMessageBox.information(self, 'Password Reset', response)
            else:
                QMessageBox.warning(self, 'Error', 'Passwords do not match.')

    def resetPassword(self, token, new_password):
        if reset_password_in_db(token, new_password):
            return "Password reset successfully."
        else:
            return "Failed to reset password. Please try again."
