"""Modulo que genera los repositorios de usuarios en la base de datos."""

from api.v1.database.connection import DatabaseConnection
import logging

from core.global_config.exceptions.exceptions import RepositoryConnectionError


class UserRepository:
    """Repositorio para la gestion de usuarios en la base de datos."""

    def __init__(self, db_url: str):
        self.db_url = db_url

    def create_user(self, username: str, email: str, hashed_password: str, is_active: bool = True):
        """Crea un nuevo usuario en la base de datos."""
        sql = """
        INSERT INTO users (username, email, hashed_password, is_active)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        try:
            with DatabaseConnection(self.db_url) as cursor:
                cursor.execute(sql, (username, email, hashed_password, is_active))
                user_id = cursor.fetchone()[0]
            logging.info(f"Usuario creado exitósamente con ID: {user_id}")
            return user_id
        except Exception as e:
            logging.error(f"Error al crear el usuario: {e}")
            raise RepositoryConnectionError("No se pudo crear el usuario en la base de datos.") from e

    def user_update_status(self, user_id: int, is_active: bool):
        """Actualiza el estado activo de un usuario."""
        sql = """
        UPDATE users
        SET is_active = %s
        WHERE id = %s
        RETURNING id;
        """
        try:
            with DatabaseConnection(self.db_url) as cursor:
                cursor.execute(sql, (is_active, user_id))
                result = cursor.fetchone()

            if result is None:
                logging.warning(f"No se encontró el usuario con ID: {user_id}")
                return None
            updated_user_id = result[0]
            logging.info(f"Estado del usuario con ID {user_id} actualizado a {is_active}")
            return updated_user_id
        except Exception as e:
            logging.error(f"Error al actualizar el estado del usuario: {e}")
            raise RepositoryConnectionError("No se pudo actualizar el estado del usuario en la base de datos.") from e

    def get_user_by_email_or_username(self, identifier: str):
        """Obtiene un usuario por su email o nombre de usuario."""
        sql = """
        SELECT id, username, email, hashed_password, is_active
        FROM users
        WHERE email = %s OR username = %s;
        """
        try:
            with DatabaseConnection(self.db_url) as cursor:
                cursor.execute(sql, (identifier, identifier))
                user = cursor.fetchone()

            if user is None:
                logging.info(f"No se encontró el usuario {identifier}")
                return None
            user_data = {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "hashed_password": user[3],
                "is_active": user[4]
            }
            logging.info(f"Usuario encontrado {identifier}")
            return user_data
        except Exception as e:
            logging.error(f"Error al obtener el usuario: {e}")
            raise RepositoryConnectionError("No se pudo obtener el usuario en la base de datos.") from e
