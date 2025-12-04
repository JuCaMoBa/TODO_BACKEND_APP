""" Modulo que genera las tablas en la base de datos para la gestion de tareas """

from api.v1.database.connection import DatabaseConnection
import logging


logger = logging.getLogger("app")


def create_tasks_tables(db_url: str):
    """Crea las tablas en la base de datos si no existen para la gestion de tareas."""

    sql = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT FALSE,
        user_id INTEGER NOT NULL,
        CONSTRAINT fk_user
            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
    );
    """
    try:
        with DatabaseConnection(db_url) as cursor:
            cursor.execute(sql)
        logger.info("Tabla 'tasks' creada o ya existente.")
    except Exception as e:
        logger.error(f"Error al crear la tabla 'tasks': {e}")
        raise
