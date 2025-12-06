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
    UserDataError
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
        except UserDataError as e:
            logger.error(f"[Controller] el usuario ya exite: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
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
        except UserDataError as e:
            logger.error(f"[Controller] No se pudo actualizar el usuario: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
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

    def login_user(self, user_login_data: OAuth2PasswordRequestForm):
        """Inicia sesion de un usuario."""
        try:
            token = self.user_service.login_user(user_login_data)
            return Token(
                access_token=token.access_token,
                token_type=token.token_type
            )
        except InvalidCredentialsError as e:
            logger.error(f"[Controller] Credenciales inválidas: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"}
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
