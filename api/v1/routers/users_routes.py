"""Modulo que genera las rutas para los usuarios."""

from fastapi import APIRouter, Depends
from api.v1.controllers.user_controller import UserController
from api.v1.schemas.users.user_create import UserCreate
from api.v1.schemas.users.user_login import UserLogin
from api.v1.schemas.users.user_message_response import UserMessageResponse
from api.v1.schemas.users.user_update import UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_controller():
    return UserController()


@router.post("/register", response_model=UserMessageResponse)
def register_user(
    user_data: UserCreate,
    controller: UserController = Depends(get_user_controller)
):
    return controller.register_user(user_data)


@router.put("/update-status", response_model=UserMessageResponse)
def update_status_user(
    user_id: int,
    update_data: UserUpdate,
    controller: UserController = Depends(get_user_controller)
):
    return controller.update_user_status(user_id, update_data)


@router.post("/login", response_model=UserMessageResponse)
def login_user(
    user_login_data: UserLogin,
    controller: UserController = Depends(get_user_controller)
):
    return controller.login_user(user_login_data)
