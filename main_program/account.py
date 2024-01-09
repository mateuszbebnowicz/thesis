from PyQt5.QtWidgets import QWidget, QLineEdit, QInputDialog, QMessageBox
from layout import layoutCreator
from dataBase.dataBaseAPI import (
    setResetToken,
    setNewPassword,
    getUserByToken,
    getUserEmail,
    getToken,
)
from security import sendResetEmail, hashPassword, generateResetToken


class AccountWindow(QWidget):
    def __init__(
        self, switchToLoginCallback, switchToPredictCallback, clearCurrentUser, userId
    ):
        super().__init__()
        self.switchToPredictCallback = switchToPredictCallback
        self.switchToLoginCallback = switchToLoginCallback
        self.clearCurrentUser = clearCurrentUser
        self.userID = userId
        self.layoutCreator = layoutCreator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Account")

        layoutDict = self.layoutCreator.createAccountLayout(self.userID)

        self.layout = layoutDict["layout"]
        self.resetPasswordButton = layoutDict["changePasswordButton"]
        self.predictionWindowButton = layoutDict["predictionWindowButton"]
        self.logoutButton = layoutDict["logoutButton"]
        self.setLayout(self.layout)

        self.resetPasswordButton.clicked.connect(self.onResetPasswordClicked)
        self.logoutButton.clicked.connect(
            lambda: (self.clearCurrentUser(), self.switchToLoginCallback())
        )
        self.predictionWindowButton.clicked.connect(self.switchToPredictCallback)

    def onResetPasswordClicked(self):
        if self.userID:
            if self.userID:
                token, expirationTime = generateResetToken()
                setResetToken(self.userID, token, expirationTime)
                email = getUserEmail(self.userID)
                token = getToken(self.userID)
                # Send the email with the token
                sendResetEmail(email, token)
                token, ok = QInputDialog.getText(
                    self,
                    "Password Reset",
                    "Password token was sent to your email \nEnter the reset token:",
                )
                if ok and token:
                    self.openChangePasswordDialog(token)
            else:
                QMessageBox.warning(self, "Error", "Email not found for the user.")
        else:
            QMessageBox.warning(self, "Error", "No user is currently logged in.")

    def verifyToken(self, token):
        # Verify if the token is valid
        # If valid, open the change password dialog
        if getUserByToken(token):
            return True
        else:
            QMessageBox.warning(self, "Error", "Invalid or expired token.")
            return False

    def openChangePasswordDialog(self, token):
        if self.verifyToken(token):
            # Open a dialog to change the password
            newPassword, ok = QInputDialog.getText(
                self, "Password Reset", "Enter your new password:", QLineEdit.Password
            )
            if ok and newPassword:
                confirmNewPassword, ok = QInputDialog.getText(
                    self,
                    "Password Reset",
                    "Confirm your new password:",
                    QLineEdit.Password,
                )
                if ok and newPassword == confirmNewPassword:
                    response = self.resetPassword(token, newPassword)
                    QMessageBox.information(self, "Password Reset", response)
                else:
                    QMessageBox.warning(self, "Error", "Passwords do not match.")

    def resetPassword(self, token, newPassword):
        hashedPassword = hashPassword(newPassword).decode("utf-8")
        if setNewPassword(token, hashedPassword):
            return "Password reset successfully."
        else:
            return "Failed to reset password. Please try again."
