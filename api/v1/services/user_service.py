""" Modulo que genera el servicio para los usuarios """

from api.v1.repositories.user_repository import UserRepository
from api.v1.schemas.users.user_create import UserCreate
from api.v1.schemas.users.user_login import UserLogin
from api.v1.schemas.users.user_update import UserUpdate
import logging
from fastapi import HTTPException
from utils.hash_password import hash_password


class UserService:
    """Servicio para la gestion de usuarios."""

    def __init__(self, db_url: str):
        self.user_repository = UserRepository(db_url)

    def create_user(self, user_create: UserCreate):
        """Crea un nuevo usuario."""
        try:
            existing_user = self.user_repository.get_user_by_email_or_username(
                email=user_create.email,
                username=user_create.username
            )
            if existing_user:
                logging.warning(
                    f"El usuario con email {user_create.email} o username {user_create.username} ya existe."
                )
                raise HTTPException(status_code=400, detail="El usuario ya existe.")

            hashed_password = hash_password(user_create.password)

            user_id = self.user_repository.create_user(
                username=user_create.username,
                email=user_create.email,
                hashed_password=hashed_password,
                is_active=user_create.is_active
            )
            logging.info(f"Usuario creado exitosamente con ID: {user_id}")
            return user_id
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error en el servicio al crear el usuario: {e}")
            raise HTTPException(status_code=500, detail="Error interno al crear el usuario.")

    def update_user_status(self, user_id: int, user_update: UserUpdate):
        """Actualiza el estado activo de un usuario."""
        try:
            updated_user_id = self.user_repository.user_update_status(
                user_id=user_id,
                is_active=user_update.is_active
            )
            if updated_user_id is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado.")

            logging.info(f"Estado del usuario con ID {user_id} actualizado exitosamente")
            return updated_user_id
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error en el servicio al actualizar el estado del usuario: {e}")
            raise HTTPException(status_code=500, detail="Error interno al actualizar usuario.")

    def login_user(self, user_login_data: UserLogin):
        """Inicia sesion de un usuario."""
        try:
            user = self.user_repository.get_user_by_email_or_username(
                email=user_login_data.email,
                username=user_login_data.username
            )
            if not user:
                logging.warning("Intento de inicio de sesion fallido")
                raise HTTPException(status_code=401, detail="Credenciales invalidas.")

            hashed_input_password = hash_password(user_login_data.password)
            if user["hashed_password"] != hashed_input_password:
                logging.warning("Intento de inicio de sesion fallido")
                raise HTTPException(status_code=401, detail="Credenciales invalidas.")

            logging.info(
                f"Usuario con email {user_login_data.email} o username {user_login_data.username} "
                f"ha iniciado sesion exitosamente")
            return user["id"]
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error en el servicio al iniciar sesion: {e}")
            raise HTTPException(status_code=500, detail="Error interno al iniciar sesion.")
