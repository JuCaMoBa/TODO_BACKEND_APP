"""Modulo de dependencias para la gestion de tareas"""

from fastapi import Depends
from api.v1.repositories.task_repository import TaskRepository
from api.v1.controllers.task_controller import TaskController
from api.v1.services.task_service import TaskService
from core.settings.settings import settings


def get_task_repository():
    return TaskRepository(settings.DB_URL)


def get_task_service(user_repository: TaskRepository = Depends(get_task_repository)):
    return TaskService(user_repository)


def get_task_controller(user_service: TaskService = Depends(get_task_service)):
    return TaskController(user_service)
