"""Modulo que contine las funciones para la configuracion global de la API"""

from functools import lru_cache
import yaml
from paths.path import ApiPaths


class DevConfig:
    docs_url = "/docs"
    redoc_url = None
    URL_ALLOWED_CORS = ["*"]


class ProdConfig:
    docs_url = None
    redoc_url = None
    URL_ALLOWED_CORS = ["*"]


class TestConfig:
    docs_url = "/docs"
    redoc_url = None
    URL_ALLOWED_CORS = ["*"]


class StageConfig:
    docs_url = "/docs"
    redoc_url = None
    URL_ALLOWED_CORS = ["*"]


@lru_cache
def get_api_config_file():
    """Funcion que carga el archivo de configuracion de despliegue"""
    with open(ApiPaths.api_config_file, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


@lru_cache
def get_deployment_enviroment():
    """Funcion que obtiene el entorno de despliegue"""
    enviroments = {"PROD": ProdConfig, "DEV": DevConfig, "TEST": TestConfig, "STAGE": StageConfig}
    selected_env = enviroments[get_api_config_file().get('environment', 'PROD')]
    return selected_env
