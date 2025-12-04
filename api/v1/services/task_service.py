""" Modulo que genera el servicio para las tareas. """

from api.v1.repositories.task_repository import TaskRepository
from api.v1.schemas.tasks.task_create import TaskCreate
from api.v1.schemas.tasks.task_message_response import TaskMessageResponse
from api.v1.schemas.tasks.task_update import TaskUpdate
import logging

from core.global_config.exceptions.exceptions import RepositoryConnectionError

logger = logging.getLogger("app")


class TaskService:
    """Servicio para la gestion de tareas."""

    def __init__(self, db_url: str):
        self.task_repository = TaskRepository(db_url)

    def create_task(self, task_create: TaskCreate, user_id: int):
        """Crea una nueva tarea."""
        try:
            task_id = self.task_repository.create_task(
                title=task_create.title,
                description=task_create.description,
                completed=task_create.completed,
                user_id=user_id
            )
            logger.info(f"[Service] Tarea creada exitosamente con ID: {task_id}")
            return TaskMessageResponse(
                success=True,
                data={
                    "task_id": task_id
                },
                message="Tarea creada exitosamente.",
                status=201
            )
        except RepositoryConnectionError as repo_exc:
            logger.error(f"[service] Error en la base de datos al crear la tarea: {repo_exc}")
            return TaskMessageResponse(
                success=False,
                data=None,
                message=str(repo_exc),
                status=500
            )
        except Exception as e:
            logger.error(f"[service] Error en el servicio al crear la tarea: {e}")
            return TaskMessageResponse(
                success=False,
                data=None,
                message="Error interno al crear la tarea.",
                status=500
            )

    def update_task(self, task_id: int, task_update: TaskUpdate, user_id: int):
        """Actualiza una tarea existente."""
        try:
            updated = self.task_repository.update_task(
                task_id=task_id,
                title=task_update.title,
                description=task_update.description,
                completed=task_update.completed,
                user_id=user_id
            )
            if not updated:
                logger.warning(f"[Service] Tarea con ID: {task_id} no encontrada para actualizar.")
                return TaskMessageResponse(
                    success=False,
                    data=None,
                    message="Tarea no encontrada.",
                    status=404
                )
            logger.info(f"[Service] Tarea con ID: {task_id} actualizada exitosamente.")
            return TaskMessageResponse(
                success=True,
                data={
                    "task_id": task_id
                },
                message="Tarea actualizada exitosamente.",
                status=200
            )
        except RepositoryConnectionError as repo_exc:
            logger.error(f"[service] Error en la base de datos al actualizar la tarea: {repo_exc}")
            return TaskMessageResponse(
                success=False,
                data=None,
                message=str(repo_exc),
                status=500
            )
        except Exception as e:
            logger.error(f"[service] Error en el servicio al actualizar la tarea: {e}")
            return TaskMessageResponse(
                success=False,
                data=None,
                message="Error interno al actualizar la tarea.",
                status=500
            )

    def delete_task(self, task_id: int, user_id: int):
        """Elimina una tarea existente."""
        try:
            deleted = self.task_repository.delete_task(
                task_id=task_id,
                user_id=user_id
            )
            if not deleted:
                logger.warning(f"[Service] Tarea con ID: {task_id} no encontrada para eliminar.")
                return TaskMessageResponse(
                    success=False,
                    data=None,
                    message="Tarea no encontrada.",
                    status=404
                )
            logger.info(f"[Service] Tarea con ID: {task_id} eliminada exitosamente.")
            return TaskMessageResponse(
                success=True,
                data={
                    "task_id": task_id
                },
                message="Tarea eliminada exitosamente.",
                status=200
            )
        except RepositoryConnectionError as repo_exc:
            logger.error(f"[service] Error en la base de datos al eliminar la tarea: {repo_exc}")
            return TaskMessageResponse(
                success=False,
                data=None,
                message=str(repo_exc),
                status=500
            )
        except Exception as e:
            logger.error(f"[service] Error en el servicio al eliminar la tarea: {e}")
            return TaskMessageResponse(
                success=False,
                data=None,
                message="Error interno al eliminar la tarea.",
                status=500
            )

    def get_tasks(self, user_id: int):
        """Obtiene una tarea por su ID."""
        try:
            task = self.task_repository.get_task_by_user_id(
                user_id=user_id
            )
            if not task:
                logger.warning(f"[Service] Tareas para el usuario con ID: {user_id} no encontrada.")
                return TaskMessageResponse(
                    success=False,
                    data=None,
                    message="Tareas no encontradas.",
                    status=404
                )
            logger.info(f"[Service] Tareas para el usuario con ID: {user_id} obtenida exitosamente.")
            return TaskMessageResponse(
                success=True,
                data=task,
                message="Tareas obtenidas exitosamente.",
                status=200
            )
        except RepositoryConnectionError as repo_exc:
            logger.error(f"[service] Error en la base de datos al obtener la tarea: {repo_exc}")
            return TaskMessageResponse(
                success=False,
                data=None,
                message=str(repo_exc),
                status=500
            )
        except Exception as e:
            logger.error(f"[service] Error en el servicio al obtener la tarea: {e}")
            return TaskMessageResponse(
                success=False,
                data=None,
                message="Error interno al obtener la tarea.",
                status=500
            )
