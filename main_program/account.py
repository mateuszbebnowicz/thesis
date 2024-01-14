from PyQt5.QtWidgets import QWidget
from layout import layoutCreator
from security import resetPasswordProcedure


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
        self.resetPasswordButton.clicked.connect(lambda: resetPasswordProcedure(self, self.userID))
        self.logoutButton.clicked.connect(
            lambda: (self.clearCurrentUser(), self.switchToLoginCallback())
        )
        self.predictionWindowButton.clicked.connect(self.switchToPredictCallback)
