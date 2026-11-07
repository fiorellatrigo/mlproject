import sys
from src.logger import logging


def error_message_detail(error, error_detail: sys):
    # el tercer valor que devuelve exc_info me da toda la data sobre el error. Donde, cuando, etc
    _, _, exc_tb = error_detail.exc_info()
    # mamushca para obtener solo el file name donde ocurrio el error
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = 'Error occured in python script name [{0}] line number [{1}] error message [{2}]'.format(
        file_name, exc_tb.tb_lineno, str(error))  # uso placeholders con los numeros, y luego paso las variables para rellenarlos

    return error_message


class CustomException(Exception):  # nuestra own custom exception class
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message
