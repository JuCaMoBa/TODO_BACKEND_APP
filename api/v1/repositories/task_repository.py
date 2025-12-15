"""Modulo que genera el repositorios de tareas en la base de datos."""

from psycopg2 import DatabaseError, IntegrityError, OperationalError
from api.v1.database.connection import DatabaseConnection
import logging

from core.global_config.exceptions.exceptions import (
    RepositoryConflictError,
    RepositoryConnectionError,
    RepositoryQueryError
)


logger = logging.getLogger("app")


class TaskRepository:
    """Repositorio para la gestion de tareas en la base de datos."""

    def __init__(self, db_url: str):
        self.db_url = db_url

    def create_task(self, title: str, description: str, user_id: int, completed: bool = False):
        """Crea una nueva tarea en la base de datos."""
        sql = """
        INSERT INTO tasks (title, description, completed, user_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        try:
            with DatabaseConnection(self.db_url) as cursor:
                cursor.execute(sql, (title, description, completed, user_id))
                task_id = cursor.fetchone()[0]
            logger.info(f"[Repository] Tarea creada exitósamente con ID: {task_id}")
            return task_id
        except OperationalError as e:
            logger.error("[Repository] Base de datos no disponible al crear la tarea", exc_info=True)
            raise RepositoryConnectionError("Base de datos no disponible") from e
        except IntegrityError as e:
            logger.warning("[Repository] Violación de integridad al crear la tarea", exc_info=True)
            raise RepositoryConflictError("Conflicto de datos") from e
        except DatabaseError as e:
            logger.error("[Repository] Error de base de datos al crear la tarea", exc_info=True)
            raise RepositoryQueryError("Error interno en la base de datos") from e

    def update_task(self, task_id: int, title: str, description: str, completed: bool, user_id: int):
        """Actualiza el estado de completitud de una tarea."""
        sql = """
        UPDATE tasks
        SET title = %s,
            description = %s,
            completed = %s
        WHERE id = %s AND user_id = %s
        RETURNING id;
        """
        try:
            with DatabaseConnection(self.db_url) as cursor:
                cursor.execute(sql, (title, description, completed, task_id, user_id))
                result = cursor.fetchone()

            if result is None:
                logger.warning(f"[Repository] No se encontró la tarea {task_id} para el usuario {user_id}")
                return None
            updated_task_id = result[0]
            logger.info(f"[Repository] Tarea {task_id} actualizada exitosamente por el usuario {user_id}")
            return updated_task_id
        except OperationalError as e:
            logger.error("[Repository] Base de datos no disponible al actualizar la tarea", exc_info=True)
            raise RepositoryConnectionError("Base de datos no disponible") from e
        except IntegrityError as e:
            logger.warning("[Repository] Violación de integridad al actualizar la tarea", exc_info=True)
            raise RepositoryConflictError("Conflicto de datos") from e
        except DatabaseError as e:
            logger.error("[Repository] Error al actualizar la tarea", exc_info=True)
            raise RepositoryQueryError("No se pudo actualizar la tarea en la base de datos.") from e

    def delete_task(self, task_id: int, user_id: int):
        """Elimina una tarea de la base de datos."""
        sql = """
        DELETE FROM tasks
        WHERE id = %s AND user_id = %s
        RETURNING id;
        """
        try:
            with DatabaseConnection(self.db_url) as cursor:
                cursor.execute(sql, (task_id, user_id))
                result = cursor.fetchone()

            if result is None:
                logger.warning(f"[Repository] No se encontró la tarea {task_id} para el usuario {user_id}")
                return None
            deleted_task_id = result[0]
            logger.info(f"[Repository] Tarea {deleted_task_id} eliminada exitosamente por el usuario {user_id}")
            return deleted_task_id
        except OperationalError as e:
            logger.error("[Repository] Base de datos no disponible al eliminar la tarea", exc_info=True)
            raise RepositoryConnectionError("Base de datos no disponible") from e
        except IntegrityError as e:
            logger.warning("[Repository] Violación de integridad al eliminar la tarea", exc_info=True)
            raise RepositoryConflictError("Conflicto de datos") from e
        except DatabaseError as e:
            logger.error("[Repository] Error al eliminar la tarea", exc_info=True)
            raise RepositoryQueryError("No se pudo eliminar la tarea en la base de datos.") from e

    def get_task_by_user_id(self, user_id: int):
        """Obtiene todas las tareas asociadas a un usuario."""
        sql = """
        SELECT id, title, description, completed, user_id
        FROM tasks
        WHERE user_id = %s;
        """
        try:
            with DatabaseConnection(self.db_url) as cursor:
                cursor.execute(sql, (user_id,))
                tasks = cursor.fetchall()

            if not tasks:
                logger.warning(f"[Repository] No se encontraron tareas para el usuario con ID: {user_id}")
                return []
            task_list = [
                {
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "completed": row[3],
                    "user_id": row[4]
                }
                for row in tasks
            ]
            logger.info(f"[Repository] {len(task_list)} tareas obtenidas para el usuario {user_id}")
            return task_list
        except OperationalError as e:
            logger.error("[Repository] Base de datos no disponible al obtener las tareas", exc_info=True)
            raise RepositoryConnectionError("Base de datos no disponible") from e
        except DatabaseError as e:
            logger.error("[Repository] Error al obtener las tareas del usuario", exc_info=True)
            raise RepositoryQueryError("No se pudieron obtener las tareas del usuario desde la base de datos.") from e
