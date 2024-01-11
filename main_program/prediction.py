from PyQt5.QtWidgets import QWidget, QMessageBox
from layout import layoutCreator
import pandas as pd
import numpy as np
from joblib import load
from dataBase.dataBaseAPI import insertPredictions


class PredictionWindow(QWidget):
    def __init__(
        self, switchToAccountCallback, switchToLoginCallback, clearCurrentUser, userID
    ):
        super().__init__()
        self.switchToAccountCallback = switchToAccountCallback
        self.switchToLoginCallback = switchToLoginCallback
        self.clearCurrentUser = clearCurrentUser
        self.userID = userID
        self.layoutCreator = layoutCreator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")

        layoutDict = self.layoutCreator.createPreditionLayout()
        self.layout = layoutDict["layout"]
        self.inputFields = layoutDict["inputFields"]
        self.predictButton = layoutDict["predictButton"]
        self.accountButton = layoutDict["accountButton"]
        self.logoutButton = layoutDict["logoutButton"]

        self.setLayout(self.layout)

        self.accountButton.clicked.connect(self.switchToAccountCallback)
        self.logoutButton.clicked.connect(
            lambda: (self.clearCurrentUser(), self.switchToLoginCallback())
        )
        self.predictButton.clicked.connect(self.predictDiabetes)

        self.scaler = load("./model/scaler.joblib")  # Update with the correct path
        self.encoder = load("./model/encoder.joblib")  # Update with the correct path
        self.model = load(
            "./model/diabetes_prediction_model.joblib"
        )  # Update with the correct path

    def predictDiabetes(self):
        # Collecting and validating input data
        try:
            age = int(self.inputFields["Age"].text())
            bmi = float(self.inputFields["BMI"].text())
            hba1c_level = float(self.inputFields["HbA1c Level"].text())
            blood_glucose_level = float(self.inputFields["Blood Glucose Level"].text())
            hypertension = (
                1 if self.inputFields["Hypertension"].currentText() == "Have" else 0
            )
            heart_disease = (
                1 if self.inputFields["Heart Disease"].currentText() == "Have" else 0
            )
            gender = self.inputFields["Gender"].currentText()
            smoking_history = self.inputFields["Smoking History"].currentText()
        except ValueError:
            QMessageBox.warning(
                self, "Invalid Input", "Please enter valid values for all fields."
            )
            return

        # Preparing input data for prediction
        inputData = pd.DataFrame(
            {
                "age": [age],
                "bmi": [bmi],
                "HbA1c_level": [hba1c_level],
                "blood_glucose_level": [blood_glucose_level],
                "hypertension": [hypertension],
                "heart_disease": [heart_disease],
                "gender": [gender],
                "smoking_history": [smoking_history],
            }
        )
        print(inputData)
        # Apply preprocessing
        inputDataScaled = self.scaler.transform(
            inputData[
                [
                    "age",
                    "bmi",
                    "HbA1c_level",
                    "blood_glucose_level",
                    "hypertension",
                    "heart_disease",
                ]
            ]
        )
        inputData_encoded = self.encoder.transform(
            inputData[["gender", "smoking_history"]]
        ).toarray()

        # Combine scaled and encoded data
        finalInputData = np.hstack((inputDataScaled, inputData_encoded))

        # Make a prediction
        prediction = self.model.predict(finalInputData)
        probabilities = self.model.predict_proba(finalInputData)
        diabetes_probability = probabilities[0][1]  # Probability of the positive class (diabetes)

        # Convert probability to percentage
        diabetes_probability_percent = round((diabetes_probability * 100),2)
        predictionText = (
            "May have diabetes with " + str(diabetes_probability_percent) + '% propabiility' if prediction[0] == 1 else "Unlikely to have diabetes"
        )
        QMessageBox.information(
            self, "Prediction Result", f"Prediction: {predictionText}"
        )
        insertPredictions(self.userID, age, bmi, hba1c_level, blood_glucose_level, predictionText)
