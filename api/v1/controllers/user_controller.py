"""Modulo que genera los controllers para la gestion de usuarios."""

from fastapi import HTTPException
from api.v1.services.user_service import UserService
from api.v1.schemas.users.user_create import UserCreate
from api.v1.schemas.users.user_update import UserUpdate


class UserController:
    """Controller para la gestion de usuarios."""

    def __init__(self):
        self.user_service = UserService()

    def register_user(self, user_create: UserCreate):
        """Registra un nuevo usuario."""
        try:
            user = self.user_service.create_user(user_create)
            return user
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_user_status(self, user_id: int, update_data: UserUpdate):
        """Actualiza el estado activo de un usuario."""
        try:
            updated_user = self.user_service.update_user_status(user_id, update_data.is_active)
            return updated_user
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
