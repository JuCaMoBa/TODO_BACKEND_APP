"""Modulo que genera los controllers para la gestion de tareas."""

from fastapi import HTTPException
from api.v1.services.task_service import TaskService
from api.v1.schemas.tasks.task_create import TaskCreate
from api.v1.schemas.tasks.task_update import TaskUpdate


class TaskController:
    """Controller para la gestion de tareas."""

    def __init__(self):
        self.task_service = TaskService()

    def create_task(self, task_create: TaskCreate, user_id: int):
        """Crea una nueva tarea."""
        try:
            task = self.task_service.create_task(task_create, user_id)
            return task
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_task(self, task_id: int, update_data: TaskUpdate, user_id: int):
        """Actualiza una tarea existente."""
        try:
            updated_task = self.task_service.update_task(task_id, update_data, user_id)
            return updated_task
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_task(self, task_id: int, user_id: int):
        """Elimina una tarea existente."""
        try:
            self.task_service.delete_task(task_id, user_id)
            return {"detail": "Tarea eliminada exitosamente."}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_tasks(self, user_id: int):
        """Obtiene una tarea por su ID."""
        try:
            task = self.task_service.get_tasks(user_id)
            return task
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
