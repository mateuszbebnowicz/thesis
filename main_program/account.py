from PyQt5.QtWidgets import QWidget
from layout import Layout


class AccountWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = Layout()
        self.initUI()

    def initUI(self):
        self.setLayout(self.layout.createAccountLayout())
