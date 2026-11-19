from dataclasses import dataclass
import os
import sys

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join(
        "artifacts", "preprocessor.pkl"
    )


class DataTransformation:
    CATEGORICAL_COLUMNS = [
        "gender",
        "race_ethnicity",
        "parental_level_of_education",
        "lunch",
        "test_preparation_course",
    ]
    SCORE_COLUMNS = ["math_score", "reading_score", "writing_score"]

    def __init__(self):
        self.transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self) -> ColumnTransformer:
        try:
            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    (
                        "one_hot_encoder",
                        OneHotEncoder(handle_unknown="ignore", drop="first"),
                    ),
                ]
            )

            return ColumnTransformer(
                transformers=[
                    (
                        "categorical",
                        categorical_pipeline,
                        self.CATEGORICAL_COLUMNS,
                    )
                ],
                remainder="drop",
            )
        except Exception as e:
            raise CustomException(e, sys)

    def prepare_data(
        self,
        train_path: str,
        test_path: str,
    ):
        logging.info("Entered the data transformation method")
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train and test datasets successfully")

            for frame in (train_df, test_df):
                if frame[self.SCORE_COLUMNS].isna().any().any():
                    raise ValueError(
                        "Score columns cannot contain missing values.")

            train_average = train_df[self.SCORE_COLUMNS].mean(axis=1)
            test_average = test_df[self.SCORE_COLUMNS].mean(axis=1)

            # Compute the median threshold strictly from training data to prevent leakage.
            threshold = float(train_average.median())
            y_train = (train_average >= threshold).astype("int64")
            y_test = (test_average >= threshold).astype("int64")

            X_train = train_df[self.CATEGORICAL_COLUMNS]
            X_test = test_df[self.CATEGORICAL_COLUMNS]

            preprocessor = self.get_data_transformer_object()
            logging.info(
                "Fitting and transforming training and testing features")
            X_train_transformed = preprocessor.fit_transform(X_train)
            X_test_transformed = preprocessor.transform(X_test)

            os.makedirs(
                os.path.dirname(
                    self.transformation_config.preprocessor_obj_file_path),
                exist_ok=True,
            )
            save_object(
                file_path=self.transformation_config.preprocessor_obj_file_path,
                obj=preprocessor,
            )
            logging.info("Saved preprocessing object")

            return (
                X_train_transformed,
                X_test_transformed,
                y_train,
                y_test,
                self.transformation_config.preprocessor_obj_file_path,
                threshold,
            )
        except Exception as e:
            raise CustomException(e, sys)
