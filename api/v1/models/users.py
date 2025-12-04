""" Modulo que genera las tablas en la base de datos para la gestion de usuarios """

from api.v1.database.connection import DatabaseConnection
import logging


logger = logging.getLogger("app")


def create_users_tables(db_url: str):
    """Crea las tablas en la base de datos si no existen para la gestion de usuarios."""

    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE
    );
    """
    try:
        with DatabaseConnection(db_url) as cursor:
            cursor.execute(sql)
        logger.info("Tabla 'users' creada o ya existente.")
    except Exception as e:
        logger.error(f"Error al crear la tabla 'users': {e}")
        raise
