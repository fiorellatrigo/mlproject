import logging
import os
from datetime import datetime

# filing convention. decidimos el formato en el que se va a guardar el timestamp de cada error/log
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# cada nombre va a comenzar con "logs" seguido del log file que decidimos en la linea anterior
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
# le dice a python que cree toda la estructura de carpetas anidadas si le pasamos una ruta larga
os.makedirs(logs_path, exist_ok=True)
# y que si la carpeta ya existe, que siga adelante ignorando la orden de creacion sin mandar error


LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    # how our entire message will get printed
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

if __name__ == "__main__":
    logging.info("Logging has started")
