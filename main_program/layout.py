from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton, QFrame, QSpacerItem, QSizePolicy, QVBoxLayout
from dataBase.dataBaseAPI import getUserData


class layoutCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.titleLabel = QLabel("DiabetesPredictor")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setFont(QFont('Arial', 24))  # You can adjust the size as needed

    def createLoginLayout(self):
        # Main layout
        mainLayout = QVBoxLayout()

        # Create a horizontal layout with spacers to center the widgets horizontally
        hLayout = QHBoxLayout()
        leftSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        rightSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Add your widgets here
        widgetContainer = QVBoxLayout()

        widgetContainer.addWidget(self.titleLabel)

        topSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        widgetContainer.addItem(topSpacer)

        usernameEdit = QLineEdit(self)
        usernameEdit.setPlaceholderText('Login')
        widgetContainer.addWidget(usernameEdit)

        passwordEdit = QLineEdit(self)
        passwordEdit.setEchoMode(QLineEdit.Password)
        passwordEdit.setPlaceholderText('Password')
        widgetContainer.addWidget(passwordEdit)

        loginButton = QPushButton('Log In', self)
        loginButton.setStyleSheet("background-color: blue; color: white;")
        loginButton.setFont(QFont('Arial', 11))
        widgetContainer.addWidget(loginButton)

        forgotPasswordLabel = QLabel('Forgot password?')
        forgotPasswordLabel.setAlignment(Qt.AlignCenter)
        widgetContainer.addWidget(forgotPasswordLabel)

        # Horizontal line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        widgetContainer.addWidget(line)

        registerButton = QPushButton('Create new account', self)
        registerButton.setStyleSheet("background-color: green; color: white;")
        registerButton.setFont(QFont('Arial', 11))
        widgetContainer.addWidget(registerButton)

        # Add the spacers and the widget container to the horizontal layout
        hLayout.addItem(leftSpacer)
        hLayout.addLayout(widgetContainer)
        hLayout.addItem(rightSpacer)

        # Create a vertical layout with spacers to center the widgets vertically
        topSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Add the spacers and the horizontal layout to the main layout
        mainLayout.addItem(topSpacer)
        mainLayout.addLayout(hLayout)
        mainLayout.addItem(bottomSpacer)

        return {
                'layout': mainLayout,
                'loginButton': loginButton,
                'registerButton': registerButton,
                'usernameEdit': usernameEdit,
                'passwordEdit': passwordEdit
        }

    def createRegisterLayout(self):
        # Main layout
        mainLayout = QVBoxLayout()

        # Create a horizontal layout with spacers to center the widgets horizontally
        hLayout = QHBoxLayout()
        leftSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        rightSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Add your widgets here
        widgetContainer = QVBoxLayout()

        widgetContainer.addWidget(self.titleLabel)

        topSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        widgetContainer.addItem(topSpacer)

        emailEdit = QLineEdit(self)
        emailEdit.setPlaceholderText("Email")
        widgetContainer.addWidget(emailEdit)

        usernameEdit = QLineEdit(self)
        usernameEdit.setPlaceholderText("Login")
        widgetContainer.addWidget(usernameEdit)

        passwordEdit = QLineEdit(self)
        passwordEdit.setEchoMode(QLineEdit.Password)
        passwordEdit.setPlaceholderText("Password")
        widgetContainer.addWidget(passwordEdit)

        passwordRepeatEdit = QLineEdit(self)
        passwordRepeatEdit.setEchoMode(QLineEdit.Password)
        passwordRepeatEdit.setPlaceholderText("Repeat Password")
        widgetContainer.addWidget(passwordRepeatEdit)

        registerButton = QPushButton("Register", self)
        registerButton.setStyleSheet("background-color: green; color: white;")
        registerButton.setFont(QFont("Arial", 11))
        widgetContainer.addWidget(registerButton)

        # Horizontal line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        widgetContainer.addWidget(line)

        loginButton = QPushButton('Click if you hava an account', self)
        loginButton.setStyleSheet("background-color: green; color: white;")
        loginButton.setFont(QFont('Arial', 11))
        widgetContainer.addWidget(loginButton)

        # Add the spacers and the widget container to the horizontal layout
        hLayout.addItem(leftSpacer)
        hLayout.addLayout(widgetContainer)
        hLayout.addItem(rightSpacer)

        # Create a vertical layout with spacers to center the widgets vertically
        topSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Add the spacers and the horizontal layout to the main layout
        mainLayout.addItem(topSpacer)
        mainLayout.addLayout(hLayout)
        mainLayout.addItem(bottomSpacer)

        return {
                'layout': mainLayout,
                'emailEdit': emailEdit,
                'usernameEdit': usernameEdit,
                'passwordEdit': passwordEdit,
                'passwordRepeatEdit': passwordRepeatEdit,
                'registerButton': registerButton,
                'loginButton': loginButton
        }

    def createPreditionLayout(self):
        # Main layout
        mainLayout = QVBoxLayout()

        # Create a horizontal layout with spacers to center the widgets horizontally
        hLayout = QHBoxLayout()
        leftSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        rightSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Add your widgets here
        widgetContainer = QVBoxLayout()

        widgetContainer.addWidget(self.titleLabel)

        topSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        widgetContainer.addItem(topSpacer)

        # Title label
        predictionTitleLabel = QLabel("Insert your data below")
        predictionTitleLabel.setAlignment(Qt.AlignCenter)
        predictionTitleLabel.setFont(QFont('Arial', 16))
        widgetContainer.addWidget(predictionTitleLabel)

        # Input fields
        inputFieldsName = ['gender', 'age', 'hypertension', 'heart disease,smoking history', 'bmi', 'HbA1c level', 'blood glucose level']
        inputFields = []
        for i in range(len(inputFieldsName)):
            inputName = QLabel(inputFieldsName[i])
            widgetContainer.addWidget(inputName)
            lineEdit = QLineEdit(self)
            inputFields.append(lineEdit)
            widgetContainer.addWidget(lineEdit)

        # Predict button
        predictButton = QPushButton('Predict', self)
        widgetContainer.addWidget(predictButton)

        # Top right buttons
        accountButton = QPushButton('Your Account', self)
        logoutButton = QPushButton('Logout', self)

        accountButton.setFont(QFont('Arial', 9))
        logoutButton.setFont(QFont('Arial', 9))

        accountButton.setFixedSize(100, 30)  # width, height
        logoutButton.setFixedSize(100, 30)

        # Horizontal layout buttons layout
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(accountButton)
        buttonsLayout.addWidget(logoutButton)

        buttonSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        buttonsLayout.addItem(buttonSpacer)
        buttonsLayout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        # Add the spacers and the widget container to the horizontal layout
        hLayout.addItem(leftSpacer)
        hLayout.addLayout(widgetContainer)
        hLayout.addItem(rightSpacer)

        # Create a vertical layout with spacers to center the widgets vertically
        topSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Add the spacers and the horizontal layout to the main layout
        mainLayout.addItem(topSpacer)
        mainLayout.addLayout(buttonsLayout)
        mainLayout.addLayout(hLayout)
        mainLayout.addItem(bottomSpacer)

        return {
                'layout': mainLayout,
                'inputFields': inputFields,
                'predictButton': predictButton,
                'accountButton': accountButton,
                'logoutButton': logoutButton
        }

    def createAccountLayout(self, userId):
        userData = getUserData(userId)
        loginText = userData[1]
        emailText = userData[3]
        # Main layout
        mainLayout = QVBoxLayout()

        # Create a horizontal layout with spacers to center the widgets horizontally
        hLayout = QHBoxLayout()
        leftSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        rightSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Add your widgets here
        widgetContainer = QVBoxLayout()

        widgetContainer.addWidget(self.titleLabel)

        topSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        widgetContainer.addItem(topSpacer)

        # Add widgets for user information
        loginLabel = QLabel('Login: ' + loginText)
        emailLabel = QLabel('Email: ' + emailText)

        # Add widgets to layout
        widgetContainer.addWidget(loginLabel)
        widgetContainer.addWidget(emailLabel)

        # Change password button
        changePasswordButton = QPushButton('Change Password')
        widgetContainer.addWidget(changePasswordButton)

        # Placeholder for previous prediction tests
        previousPredictionsLabel = QLabel('All previous prediction tests will be listed here')
        widgetContainer.addWidget(previousPredictionsLabel)

        # Top right buttons
        predictonWindowButton = QPushButton('Diabetes Predictor', self)
        logoutButton = QPushButton('Logout', self)

        predictonWindowButton.setFont(QFont('Arial', 9))
        logoutButton.setFont(QFont('Arial', 9))

        predictonWindowButton.setFixedSize(100, 30)  # width, height
        logoutButton.setFixedSize(100, 30)

        # Horizontal layout buttons layout
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(predictonWindowButton)
        buttonsLayout.addWidget(logoutButton)

        buttonSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        buttonsLayout.addItem(buttonSpacer)
        buttonsLayout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        # Add the spacers and the widget container to the horizontal layout
        hLayout.addItem(leftSpacer)
        hLayout.addLayout(widgetContainer)
        hLayout.addItem(rightSpacer)

        # Create a vertical layout with spacers to center the widgets vertically
        topSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        bottomSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Add the spacers and the horizontal layout to the main layout
        mainLayout.addItem(topSpacer)
        mainLayout.addLayout(buttonsLayout)
        mainLayout.addLayout(hLayout)
        mainLayout.addItem(bottomSpacer)

        return {
                'layout': mainLayout,
                'predictionWindowButton': predictonWindowButton,
                'logoutButton': logoutButton
        }
