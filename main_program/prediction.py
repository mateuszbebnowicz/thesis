from PyQt5.QtWidgets import QWidget, QMessageBox
from layout import layoutCreator
import pandas as pd
import numpy as np
from joblib import load


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

        self.scaler = load('./model/scaler.joblib')  # Update with the correct path
        self.encoder = load('./model/encoder.joblib')  # Update with the correct path
        self.model = load('./model/diabetes_prediction_model.joblib')  # Update with the correct path

    def get_validated_input(self, field_name, data_type, validator):
        input_text = self.inputFields[field_name].text()
        if input_text and validator(input_text):
            return data_type(input_text)
        else:
            QMessageBox.warning(self, 'Invalid Input', f'Please enter a valid value for {field_name}.')
            return None

    def predictDiabetes(self):
        # Function to check if input is a valid float
        def is_valid_float(input_str):
            try:
                float(input_str)
                return True
            except ValueError:
                return False

        # Collecting and validating input data
        try:
            age = int(self.inputFields['Age'].text())
            bmi = float(self.inputFields['BMI'].text())
            hba1c_level = float(self.inputFields['HbA1c Level'].text())
            blood_glucose_level = float(self.inputFields['Blood Glucose Level'].text())
            hypertension = 1 if self.inputFields['Hypertension'].currentText() == 'Have' else 0
            heart_disease = 1 if self.inputFields['Heart Disease'].currentText() == 'Have' else 0
            gender = self.inputFields['Gender'].currentText()
            smoking_history = self.inputFields['Smoking History'].currentText()
        except ValueError:
            QMessageBox.warning(self, 'Invalid Input', 'Please enter valid values for all fields.')
            return

        # Preparing input data for prediction
        input_data = pd.DataFrame({
            'age': [age],
            'bmi': [bmi],
            'HbA1c_level': [hba1c_level],
            'blood_glucose_level': [blood_glucose_level],
            'hypertension': [hypertension],
            'heart_disease': [heart_disease],
            'gender': [gender],
            'smoking_history': [smoking_history]
        })

        # def perform_one_hot_encoding(df, column_name):
        #     dummies = pd.get_dummies(df[column_name], prefix=column_name)
        #     return pd.concat([df.drop(column_name, axis=1), dummies], axis=1)

        # # Perform one-hot encoding on 'gender' and 'smoking_history'
        # input_data = perform_one_hot_encoding(input_data, 'gender')
        # input_data = perform_one_hot_encoding(input_data, 'smoking_history')
        print(input_data)
        # Apply preprocessing
        input_data_scaled = self.scaler.transform(input_data[['age', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'hypertension', 'heart_disease']])
        input_data_encoded = self.encoder.transform(input_data[['gender', 'smoking_history']]).toarray()

        # Combine scaled and encoded data
        final_input_data = np.hstack((input_data_scaled, input_data_encoded))

        # Make a prediction
        prediction = self.model.predict(final_input_data)
        prediction_text = 'May have diabetes' if prediction[0] == 1 else 'Unlikely to have diabetes'
        QMessageBox.information(self, 'Prediction Result', f'Prediction: {prediction_text}')
