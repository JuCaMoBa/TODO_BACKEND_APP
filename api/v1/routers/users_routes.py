"""Modulo que genera las rutas para los usuarios."""

from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.v1.controllers.user_controller import UserController
from api.v1.dependency.dependencies import current_user_authenticated
from api.v1.schemas.auth.auth_token import UserAuthData
from api.v1.schemas.users.user_create import UserCreate
from api.v1.schemas.users.user_message_response import UserMessageResponse
from api.v1.schemas.users.user_update import UserUpdate
from api.v1.dependency.users.user_dependencies import get_user_controller

router = APIRouter(tags=["Users"])


@router.post("/register", response_model=UserMessageResponse)
def register_user(
    user_data: UserCreate,
    controller: UserController = Depends(get_user_controller)
):
    data = controller.register_user(user_data)
    return data


@router.put("/update-status", response_model=UserMessageResponse)
def update_status_user(
    update_data: UserUpdate,
    current_user: UserAuthData = Depends(current_user_authenticated),
    controller: UserController = Depends(get_user_controller)
):
    user_id = current_user.user_id
    data = controller.update_user_status(user_id, update_data)
    return data


@router.post("/token", response_model=UserMessageResponse)
def login_user(
    user_login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    controller: UserController = Depends(get_user_controller)
):
    data = controller.login_user(user_login_data)
    return data
