"""Modulo que genera las rutas para las tareas."""

from fastapi import APIRouter, Depends
from api.v1.controllers.task_controller import TaskController
from api.v1.dependency.dependencies import current_user_dependency
from api.v1.schemas.auth.auth_token import TokenData
from api.v1.schemas.tasks.task_create import TaskCreate
from api.v1.schemas.tasks.task_message_response import TaskMessageResponse
from api.v1.schemas.tasks.task_update import TaskUpdate
from api.v1.dependency.tasks.tasks_dependecies import get_task_controller

router = APIRouter(tags=["Tasks"])


@router.post("/create", response_model=TaskMessageResponse)
def create_task(
    task_data: TaskCreate,
    current_user: TokenData = Depends(current_user_dependency),
    controller: TaskController = Depends(get_task_controller)
):
    user_id = current_user.user_id
    return controller.create_task(task_data, user_id)


@router.put("/update", response_model=TaskMessageResponse)
def update_task(
    task_id: int,
    update_data: TaskUpdate,
    current_user: TokenData = Depends(current_user_dependency),
    controller: TaskController = Depends(get_task_controller)
):
    user_id = current_user.user_id
    return controller.update_task(task_id, update_data, user_id)


@router.delete("/delete", response_model=TaskMessageResponse)
def delete_task(
    task_id: int,
    current_user: TokenData = Depends(current_user_dependency),
    controller: TaskController = Depends(get_task_controller)
):
    user_id = current_user.user_id
    return controller.delete_task(task_id, user_id)


@router.get("/get", response_model=TaskMessageResponse)
def get_tasks(
    current_user: TokenData = Depends(current_user_dependency),
    controller: TaskController = Depends(get_task_controller)
):
    user_id = current_user.user_id
    return controller.get_tasks(user_id)
