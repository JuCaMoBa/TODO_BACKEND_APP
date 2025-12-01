""" Modulo de definicion de las rutas de la API"""

import os


class ApiPaths:
    """ Carpetas y rutas de la API"""

    base_dir = os.path.dirname(__file__)

    global_config = os.path.join(base_dir, "..", "./core/global_config")
    """ Ruta del archivo de configuracion global"""

    api_config_file = os.path.join(global_config, "api_config_files", "deployment_enviroments.yml")
    """ Ruta del archivo de configuracion de despliegue"""
