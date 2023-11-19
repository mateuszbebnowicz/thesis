from PyQt5.QtWidgets import QWidget, QMessageBox
from layout import layoutCreator


class PredictionWindow(QWidget):
    def __init__(self, switchToAccountCallback, switchToLoginCallback, clearUser):
        super().__init__()
        self.switchToAccountCallback = switchToAccountCallback
        self.switchToLoginCallback = switchToLoginCallback
        self.clearUser = clearUser
        self.layoutCreator = layoutCreator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")

        layoutDict = self.layoutCreator.createPreditionLayout()
        self.layout = layoutDict['layout']
        self.inputFields = layoutDict['inputFields']
        self.predictButton = layoutDict['predictButton']
        self.accountButton = layoutDict['accountButton']
        self.logoutButton = layoutDict['logoutButton']

        self.setLayout(self.layout)

        self.accountButton.clicked.connect(self.switchToAccountCallback)
        self.logoutButton.clicked.connect(lambda: (self.clearUser(), self.switchToLoginCallback()))
        self.predictButton.clicked.connect(self.predictDiabetes)

    def predictDiabetes(self):
        # Logic to trigger the prediction using the AI model
        # This would involve collecting the data from input_fields and passing it to your model
        QMessageBox.information(self, 'Prediction', 'The prediction functionality will be implemented here.')
