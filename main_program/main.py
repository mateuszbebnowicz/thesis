import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from login import LoginWindow
from register import RegistrationWindow
from prediction import PredictionWindow


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DiabetesPredictor')
        self.setFixedSize(int(QApplication.desktop().screenGeometry().width() * 0.5),
                          int(QApplication.desktop().screenGeometry().height() * 0.5))

        # Create the stacked widget
        self.stackedWidget = QStackedWidget(self)
        self.setCentralWidget(self.stackedWidget)

        # Create instances of the login and registration forms
        self.loginWindow = LoginWindow(self.showRegistrationForm, self.showPredictionForm)  # Pass the method, not the instance
        self.registrationWindow = RegistrationWindow(self.showLoginForm)
        self.predictionWindow = PredictionWindow()

        # Add the windows to the stacked widget
        self.stackedWidget.addWidget(self.loginWindow)
        self.stackedWidget.addWidget(self.registrationWindow)
        self.stackedWidget.addWidget(self.predictionWindow)

        # Show the login form first
        self.stackedWidget.setCurrentWidget(self.loginWindow)

    def showRegistrationForm(self):
        self.stackedWidget.setCurrentWidget(self.registrationWindow)

    def showLoginForm(self):
        self.stackedWidget.setCurrentWidget(self.loginWindow)

    def showPredictionForm(self):
        self.stackedWidget.setCurrentWidget(self.predictionWindow)


def main():
    app = QApplication(sys.argv)
    mainApp = MainApp()
    mainApp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()