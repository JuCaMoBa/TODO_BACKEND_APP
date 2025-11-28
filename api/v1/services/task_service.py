""" Modulo que genera el servicio para las tareas. """

from api.v1.repositories.task_repository import TaskRepository
from api.v1.schemas.tasks.task_create import TaskCreate
from api.v1.schemas.tasks.task_update import TaskUpdate
import logging
from fastapi import HTTPException


class TaskService:
    """Servicio para la gestion de tareas."""

    def __init__(self):
        self.task_repository = TaskRepository()

    def create_task(self, task_create: TaskCreate, user_id: int):
        """Crea una nueva tarea."""
        try:
            task_id = self.task_repository.create_task(
                title=task_create.title,
                description=task_create.description,
                is_completed=task_create.is_completed,
                user_id=user_id
            )
            logging.info(f"Tarea creada exitosamente con ID: {task_id}")
            return task_id
        except Exception as e:
            logging.error(f"Error en el servicio al crear la tarea: {e}")
            raise HTTPException(status_code=500, detail="Error interno al crear la tarea.")

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
                logging.warning(f"Tarea con ID: {task_id} no encontrada para actualizar.")
                raise HTTPException(status_code=404, detail="Tarea no encontrada.")
            logging.info(f"Tarea con ID: {task_id} actualizada exitosamente.")
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error en el servicio al actualizar la tarea: {e}")
            raise HTTPException(status_code=500, detail="Error interno al actualizar la tarea.")

    def delete_task(self, task_id: int, user_id: int):
        """Elimina una tarea existente."""
        try:
            deleted = self.task_repository.delete_task(
                task_id=task_id,
                user_id=user_id
            )
            if not deleted:
                logging.warning(f"Tarea con ID: {task_id} no encontrada para eliminar.")
                raise HTTPException(status_code=404, detail="Tarea no encontrada.")
            logging.info(f"Tarea con ID: {task_id} eliminada exitosamente.")
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error en el servicio al eliminar la tarea: {e}")
            raise HTTPException(status_code=500, detail="Error interno al eliminar la tarea.")

    def get_tasks(self, user_id: int):
        """Obtiene una tarea por su ID."""
        try:
            task = self.task_repository.get_task_by_user_id(
                user_id=user_id
            )
            if not task:
                logging.warning(f"Tareas para el usuario con ID: {user_id} no encontrada.")
                raise HTTPException(status_code=404, detail="Tarea no encontrada.")
            logging.info(f"Tareas para el usuario con ID: {user_id} obtenida exitosamente.")
            return task
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error en el servicio al obtener la tarea: {e}")
            raise HTTPException(status_code=500, detail="Error interno al obtener la tarea.")
