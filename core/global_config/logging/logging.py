"""Modulo que configura el sistema de logging de la aplicación."""

from logging.config import dictConfig
from core.global_config.logging.logging_settings import log_config


def initialize_logging():
    """Inicializa la configuracion de logging de la aplicacion."""
    dictConfig(log_config)
