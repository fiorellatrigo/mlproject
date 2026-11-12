from setuptools import find_packages, setup
from typing import List

# Creo esta constante para borrarla de la lista de requirements. Su funcion es
HYPHEN_E_DOT = '-e .'
# que cuando se terminan de leer los requirements, se inicie setup.py


def get_requirements(file_path: str) -> List[str]:
    """
    this function will return the list of requirements
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        # elimino los saltos de linea al leer los requirements
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            # elimino la ultima linea que dice '-e .'
            requirements.remove(HYPHEN_E_DOT)
    return requirements


setup(
    name='mlproject',
    version='0.0.1',  # primera version de mi proyecto
    author='Fiorella',
    author_email='fiorellatrigo@gmail.com',
    packages=find_packages(),
    # que instale todas las librerias en el archivo requirements
    install_requires=get_requirements('requirements.txt')




)
