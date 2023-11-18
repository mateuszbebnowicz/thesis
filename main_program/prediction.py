from PyQt5.QtWidgets import QWidget, QMessageBox
from layout import Layout


class PredictionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.Layout = Layout()
        layoutDict = self.Layout.createPreditionLayout()

        self.layout = layoutDict['layout']
        self.inputFields = layoutDict['inputFields']
        self.predictButton = layoutDict['predictButton']
        self.accountButton = layoutDict['accountButton']

        self.setLayout(self.layout)

        self.accountButton.clicked.connect(self.openAccountPage)
        self.predictButton.clicked.connect(self.predictDiabetes)

    def predictDiabetes(self):
        # Logic to trigger the prediction using the AI model
        # This would involve collecting the data from input_fields and passing it to your model
        QMessageBox.information(self, 'Prediction', 'The prediction functionality will be implemented here.')

    def openAccountPage(self):
        # Logic to open the account page will be implemented here
        QMessageBox.information(self, 'Account', 'Open account page functionality will be implemented here.')
