"""Modulo que genera las rutas para las tareas."""

from fastapi import APIRouter, Depends
from api.v1.controllers.task_controller import TaskController
from api.v1.schemas.tasks.task_create import TaskCreate
from api.v1.schemas.tasks.task_message_response import TaskMessageResponse
from api.v1.schemas.tasks.task_update import TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_tasks_controller():
    return TaskController()


@router.post("/create", response_model=TaskMessageResponse)
def create_task(
    task_data: TaskCreate,
    user_id: int,
    controller: TaskController = Depends(get_tasks_controller)
):
    return controller.create_task(task_data, user_id)


@router.put("/update", response_model=TaskMessageResponse)
def update_task(
    task_id: int,
    user_id: int,
    update_data: TaskUpdate,
    controller: TaskController = Depends(get_tasks_controller)
):
    return controller.update_task(task_id, update_data, user_id)


@router.delete("/delete", response_model=TaskMessageResponse)
def delete_task(
    task_id: int,
    user_id: int,
    controller: TaskController = Depends(get_tasks_controller)
):
    return controller.delete_task(task_id, user_id)


@router.get("/get", response_model=TaskMessageResponse)
def get_tasks(
    user_id: int,
    controller: TaskController = Depends(get_tasks_controller)
):
    return controller.get_tasks(user_id)
