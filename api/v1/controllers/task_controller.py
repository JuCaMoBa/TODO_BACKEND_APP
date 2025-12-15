"""Modulo que genera los controllers para la gestion de tareas."""

import logging
from fastapi import HTTPException, status
from api.v1.schemas.tasks.task_message_response import TaskMessageResponse
from api.v1.services.task_service import TaskService
from api.v1.schemas.tasks.task_create import TaskCreate
from api.v1.schemas.tasks.task_update import TaskUpdate
from core.global_config.exceptions.exceptions import (
    RepositoryConflictError,
    RepositoryConnectionError,
    ExceptionDataError,
)

logger = logging.getLogger("app")


class TaskController:
    """Controller para la gestion de tareas."""

    def __init__(self, task_service: TaskService):
        self.task_service = task_service

    def create_task(self, task_create: TaskCreate, user_id: int):
        """Crea una nueva tarea."""
        try:
            task_id = self.task_service.create_task(task_create, user_id)
            return TaskMessageResponse(
                    success=True,
                    data={
                        "task_id": task_id
                    },
                    message="Tarea creada exitosamente.",
                    status=201
            )
        except RepositoryConflictError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except ExceptionDataError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except RepositoryConnectionError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio no disponible"
            )

    def update_task(self, task_id: int, update_data: TaskUpdate, user_id: int):
        """Actualiza una tarea existente."""
        try:
            updated_task_id = self.task_service.update_task(task_id, update_data, user_id)
            return TaskMessageResponse(
                        success=True,
                        data={
                            "task_id": updated_task_id
                        },
                        message="Tarea actualizada exitosamente.",
                        status=200
                    )
        except ExceptionDataError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except RepositoryConflictError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except RepositoryConnectionError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio no disponible"
            )

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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except RepositoryConnectionError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio no disponible"
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
        except RepositoryConnectionError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio no disponible"
            )
