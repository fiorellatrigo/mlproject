import os
import sys
import numpy as np
import pandas as pd
from src.exception import CustomException


def save_object(file_path: str, obj: object) -> None:
    """
    Save a Python object to a file using pickle.

    Args:
        file_path (str): The path to the file where the object will be saved.
        obj (object): The Python object to be saved.

    Raises:
        Exception: If there is an error while saving the object.
    """
    try:
        import pickle
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise Exception(f"Error saving object to {file_path}: {e}")
