import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass  # The constructor is empty, but it can be used to initialize any attributes or configurations needed for the prediction pipeline in the future.

    def predict(self, features):
        try:
            model_path = "artifacts/model.pkl"  # Route to the model file
            preprocessor_path = "artifacts/preprocessor.pkl"  # Route to the preprocessor file

            # Load the model using the load_object function from utils.py
            model = load_object(file_path=model_path)
            # Load the preprocessor using the load_object function from utils.py
            preprocessor = load_object(file_path=preprocessor_path)

            # Scale the input features using the loaded preprocessor
            data_scaled = preprocessor.transform(features)
            # Make predictions using the loaded model on the scaled features
            preds = model.predict(data_scaled)

            return preds
        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(self,
                 gender: str,
                 race_ethnicity: str,
                 parental_level_of_education: str,
                 lunch: str,
                 test_preparation_course: str):  # We list all the features that we want to use for prediction
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course

    def get_data_as_dataframe(self):
        try:
            data_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course]
            }
            return pd.DataFrame(data_dict)
        except Exception as e:
            raise CustomException(e, sys)
