"""Modulo que genera los controllers para la gestion de usuarios."""

import logging
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.v1.services.user_service import UserService
from api.v1.schemas.users.user_create import UserCreate
from api.v1.schemas.users.user_update import UserUpdate
from core.global_config.exceptions.exceptions import InvalidCredentialsError, RepositoryConnectionError

logger = logging.getLogger("app")


class UserController:
    """Controller para la gestion de usuarios."""

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register_user(self, user_create: UserCreate):
        """Registra un nuevo usuario."""
        return self.user_service.create_user(user_create)

    def update_user_status(self, user_id: int, update_data: UserUpdate):
        """Actualiza el estado activo de un usuario."""
        updated_user = self.user_service.update_user_status(user_id, update_data)
        return updated_user

    def login_user(self, user_login_data: OAuth2PasswordRequestForm):
        """Inicia sesion de un usuario."""
        try:
            user = self.user_service.login_user(user_login_data)
            return user
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
