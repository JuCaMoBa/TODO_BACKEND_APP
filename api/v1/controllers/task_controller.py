"""Modulo que genera los controllers para la gestion de tareas."""

import logging
from fastapi import HTTPException, status
from api.v1.schemas.tasks.task_message_response import TaskMessageResponse
from api.v1.services.task_service import TaskService
from api.v1.schemas.tasks.task_create import TaskCreate
from api.v1.schemas.tasks.task_update import TaskUpdate
from core.global_config.exceptions.exceptions import RepositoryConnectionError, ExceptionDataError

logger = logging.getLogger("app")


class TaskController:
    """Controller para la gestion de tareas."""

    def __init__(self, task_service: TaskService):
        self.task_service = task_service

    def create_task(self, task_create: TaskCreate, user_id: int):
        """Crea una nueva tarea."""
        return self.task_service.create_task(task_create, user_id)

    def update_task(self, task_id: int, update_data: TaskUpdate, user_id: int):
        """Actualiza una tarea existente."""
        return self.task_service.update_task(task_id, update_data, user_id)

    def delete_task(self, task_id: int, user_id: int):
        """Elimina una tarea existente."""
        try:
            deleted_task_id = self.task_service.delete_task(task_id, user_id)
            return TaskMessageResponse(
                        success=True,
                        data={
                            "task_id": deleted_task_id
                        },
                        message="Tarea eliminada exitosamente.",
                        status=200
                    )
        except ExceptionDataError as e:
            logger.error(f"[Controller] Tarea con ID: {task_id} no encontrada para eliminar.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except RepositoryConnectionError as e:
            logger.error(f"[Controller] Error de BD: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio no disponible"
            )
        except Exception as e:
            logger.error(f"[Controller] Error inesperado: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_tasks(self, user_id: int):
        """Obtiene una tarea por su ID."""
        try:
            tasks = self.task_service.get_tasks(user_id)
            return TaskMessageResponse(
                    success=True,
                    data=tasks,
                    message="Tareas obtenidas exitosamente.",
                    status=200
                )
        except ExceptionDataError as e:
            logger.error(f"[controller] Tareas para el usuario con ID: {user_id} no encontrada.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except RepositoryConnectionError as e:
            logger.error(f"[Controller] Error de BD: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio no disponible"
            )
        except Exception as e:
            logger.error(f"[Controller] Error inesperado: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
