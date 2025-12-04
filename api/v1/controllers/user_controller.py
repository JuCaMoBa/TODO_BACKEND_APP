"""Modulo que genera los controllers para la gestion de usuarios."""

from api.v1.schemas.users.user_login import UserLogin
from api.v1.services.user_service import UserService
from api.v1.schemas.users.user_create import UserCreate
from api.v1.schemas.users.user_update import UserUpdate


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

    def login_user(self, user_login_data: UserLogin):
        """Inicia sesion de un usuario."""
        user = self.user_service.login_user(user_login_data)
        return user
