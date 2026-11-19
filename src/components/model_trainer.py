from dataclasses import dataclass
import os
import sys
import warnings

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

warnings.filterwarnings("ignore")


@dataclass
class ModelTrainerConfig:
    # Where should the trained model be saved
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")


class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(
        self,
        X_train,
        y_train,
        X_test,
        y_test,
    ):
        logging.info("Entered the model training component")
        try:
            # Define hyperparameter grid for Logistic Regression regularization tuning
            param_grid = {
                "C": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                "penalty": ["l1", "l2"],
                "solver": ["liblinear"],
            }

            # Run cross-validated grid search to find the best regularization setup
            logging.info("Starting GridSearchCV for Logistic Regression")
            grid_search = GridSearchCV(
                estimator=LogisticRegression(random_state=42, max_iter=1000),
                param_grid=param_grid,
                cv=5,
                scoring="accuracy",
                n_jobs=-1,
            )
            grid_search.fit(X_train, y_train)

            best_model = grid_search.best_estimator_
            logging.info(f"Best parameters found: {grid_search.best_params_}")

            # Generate predictions on the test set and evaluate classification metrics
            y_pred = best_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)

            print(f"Best Parameters: {grid_search.best_params_}")
            print(f"Test Accuracy: {accuracy:.4f}\n")
            print("Classification Report:")
            print(classification_report(y_test, y_pred))
            print("Confusion Matrix:")
            print(confusion_matrix(y_test, y_pred))

            # Persist the trained model artifact for downstream use
            os.makedirs(
                os.path.dirname(
                    self.model_trainer_config.trained_model_file_path),
                exist_ok=True,
            )
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )
            logging.info("Saved trained model artifact successfully")

            return accuracy

        except Exception as e:
            raise CustomException(e, sys)
