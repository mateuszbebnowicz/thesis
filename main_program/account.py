from PyQt5.QtWidgets import QWidget
from layout import layoutCreator


class AccountWindow(QWidget):
    def __init__(self, switchToLoginCallback, switchToPredictCallback):
        super().__init__()
        self.switchToPredictCallback = switchToPredictCallback
        self.switchToLoginCallback = switchToLoginCallback
        self.layoutCreator = layoutCreator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Account")

        layoutDict = self.layoutCreator.createAccountLayout()

        self.layout = layoutDict['layout']
        self.predictionWindowButton = layoutDict['predictionWindowButton']
        self.logoutButton = layoutDict['logoutButton']
        self.setLayout(self.layout)

        self.logoutButton.clicked.connect(self.switchToLoginCallback)
        self.predictionWindowButton.clicked.connect(self.switchToPredictCallback)
