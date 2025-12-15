"""Modulo que genera los controllers para la gestion de usuarios."""

import logging
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.v1.schemas.auth.auth_token import Token
from api.v1.schemas.users.user_message_response import UserMessageResponse
from api.v1.services.user_service import UserService
from api.v1.schemas.users.user_create import UserCreate
from api.v1.schemas.users.user_update import UserUpdate
from core.global_config.exceptions.exceptions import (
    InvalidCredentialsError,
    RepositoryConnectionError,
    ExceptionDataError
)

logger = logging.getLogger("app")


class UserController:
    """Controller para la gestion de usuarios."""

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register_user(self, user_create: UserCreate):
        """Registra un nuevo usuario."""
        try:
            user_id = self.user_service.create_user(user_create)
            return UserMessageResponse(
                success=True,
                data=user_id,
                message="Usuario creado exitosamente.",
                status=201
            )
        except ExceptionDataError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except RepositoryConnectionError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio no disponible"
            )

    def update_user_status(self, user_id: int, update_data: UserUpdate):
        """Actualiza el estado activo de un usuario."""
        try:
            updated_user = self.user_service.update_user_status(user_id, update_data)
            return UserMessageResponse(
                success=True,
                data={
                    "user_id": updated_user
                },
                message=f"Usuario con ID {updated_user} actualizado con exito",
                status=200
            )
        except ExceptionDataError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        except RepositoryConnectionError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio no disponible"
            )

    def login_user(self, user_login_data: OAuth2PasswordRequestForm):
        """Inicia sesion de un usuario."""
        try:
            token = self.user_service.login_user(user_login_data)
            return Token(
                access_token=token.access_token,
                token_type=token.token_type
            )
        except InvalidCredentialsError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"}
                )
        except RepositoryConnectionError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Servicio no disponible"
            )
