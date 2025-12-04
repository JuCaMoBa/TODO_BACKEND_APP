"""Modulo que genera los controllers para la gestion de tareas."""

from api.v1.services.task_service import TaskService
from api.v1.schemas.tasks.task_create import TaskCreate
from api.v1.schemas.tasks.task_update import TaskUpdate


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
        return self.task_service.delete_task(task_id, user_id)

    def get_tasks(self, user_id: int):
        """Obtiene una tarea por su ID."""
        return self.task_service.get_tasks(user_id)
