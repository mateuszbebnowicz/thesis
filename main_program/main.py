import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from login import LoginWindow
from register import RegistrationWindow
from prediction import PredictionWindow
from account import AccountWindow


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
        self.loginWindow = LoginWindow(self.createRegistrationForm, self.createPredictionForm)
        self.stackedWidget.addWidget(self.loginWindow)
        self.stackedWidget.setCurrentWidget(self.loginWindow)

    def createLoginForm(self):
        loginWindow = LoginWindow(self.createRegistrationForm, self.createPredictionForm)
        self.stackedWidget.addWidget(loginWindow)
        self.stackedWidget.setCurrentWidget(loginWindow)
        self.removeAllExcept(loginWindow)

    def createRegistrationForm(self):
        registrationWindow = RegistrationWindow(self.createLoginForm)
        self.stackedWidget.addWidget(registrationWindow)
        self.stackedWidget.setCurrentWidget(registrationWindow)
        self.removeAllExcept(registrationWindow)

    def createPredictionForm(self):
        predictionWindow = PredictionWindow(self.showAccountForm, self.createLoginForm)
        self.stackedWidget.addWidget(predictionWindow)
        self.stackedWidget.setCurrentWidget(predictionWindow)
        self.removeAllExcept(predictionWindow)

    def showAccountForm(self):
        accountWindow = AccountWindow(self.createLoginForm, self.createPredictionForm)
        self.stackedWidget.addWidget(accountWindow)
        self.stackedWidget.setCurrentWidget(accountWindow)
        self.removeAllExcept(accountWindow)

    def removeAllExcept(self, form):
        # Loop through all widgets in the stacked widget
        for i in range(self.stackedWidget.count()):
            widget = self.stackedWidget.widget(i)

            # Check if the widget is not the loginWindow
            if widget != form:
                # Remove the widget
                self.stackedWidget.removeWidget(widget)


def main():
    app = QApplication(sys.argv)
    mainApp = MainApp()
    mainApp.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
