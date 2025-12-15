""" Modulo que genera el servicio para las tareas. """

from api.v1.repositories.task_repository import TaskRepository
from api.v1.schemas.tasks.task_create import TaskCreate
from api.v1.schemas.tasks.task_update import TaskUpdate
import logging

from core.global_config.exceptions.exceptions import (
    ExceptionDataError
)

logger = logging.getLogger("app")


class TaskService:
    """Servicio para la gestion de tareas."""

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create_task(self, task_create: TaskCreate, user_id: int):
        """Crea una nueva tarea."""
        task_id = self.task_repository.create_task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=user_id
        )
        if not task_id:
            logger.warning("[Service] No se pudo crear la tarea")
            raise ExceptionDataError("No se pudo crear la tarea")

        logger.info(f"[Service] Tarea creada exitosamente con ID: {task_id}")
        return task_id

    def update_task(self, task_id: int, task_update: TaskUpdate, user_id: int):
        """Actualiza una tarea existente."""
        updated_task_id = self.task_repository.update_task(
            task_id=task_id,
            title=task_update.title,
            description=task_update.description,
            completed=task_update.completed,
            user_id=user_id
        )
        if not updated_task_id:
            logger.warning(f"[Service] Tarea con ID: {task_id} no encontrada para actualizar.")
            raise ExceptionDataError("Tarea no encontrada para actualizar")

        logger.info(f"[Service] Tarea con ID: {updated_task_id} actualizada exitosamente.")
        return updated_task_id

    def delete_task(self, task_id: int, user_id: int):
        """Elimina una tarea existente."""
        deleted_task_id = self.task_repository.delete_task(
            task_id=task_id,
            user_id=user_id
        )
        if not deleted_task_id:
            logger.warning(f"[Service] Tarea con ID: {task_id} no encontrada para eliminar.")
            raise ExceptionDataError("Tarea no encontrada para eliminar")
        logger.info(f"[Service] Tarea con ID: {deleted_task_id} eliminada exitosamente.")
        return deleted_task_id

    def get_tasks(self, user_id: int):
        """Obtiene una tarea por su ID."""
        tasks = self.task_repository.get_task_by_user_id(
            user_id=user_id
        )
        if not tasks:
            logger.warning(f"[Service] Tareas para el usuario con ID: {user_id} no encontrada.")
            raise ExceptionDataError("Tareas no encontradas")
        logger.info(f"[Service] Tareas para el usuario con ID: {user_id} obtenida exitosamente.")
        return tasks
