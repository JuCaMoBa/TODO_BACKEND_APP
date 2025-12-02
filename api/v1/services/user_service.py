""" Modulo que genera el servicio para los usuarios """

from api.v1.repositories.user_repository import UserRepository
from api.v1.schemas.users.user_create import UserCreate
from api.v1.schemas.users.user_login import UserLogin
from api.v1.schemas.users.user_message_response import UserMessageResponse
from api.v1.schemas.users.user_update import UserUpdate
import logging
from core.global_config.exceptions.exceptions import RepositoryConnectionError
from utils.auth_utils import create_access_token
from utils.password_managment import hash_password, verify_password


class UserService:
    """Servicio para la gestion de usuarios."""

    def __init__(self, db_url: str):
        self.user_repository = UserRepository(db_url)

    def create_user(self, user_create: UserCreate):
        """Crea un nuevo usuario."""
        try:
            existing_user = self.user_repository.get_user_by_email_or_username(
                user_create.email
            )
            if existing_user:
                logging.warning(
                    f"[Service] El usuario con email {user_create.email} o username {user_create.username} ya existe."
                )
                return UserMessageResponse(
                    success=False,
                    data=None,
                    message="El usuario ya existe.",
                    status=400
                )

            hashed_password = hash_password(user_create.password)

            user_id = self.user_repository.create_user(
                username=user_create.username,
                email=user_create.email,
                hashed_password=hashed_password,
                is_active=user_create.is_active
            )
            logging.info(f"[Service] Usuario creado exitosamente con ID: {user_id}")
            return UserMessageResponse(
                success=True,
                data=user_id,
                message="Usuario creado exitosamente.",
                status=201
            )
        except RepositoryConnectionError as repo_exc:
            logging.error(f"[service] Error en la base de datos al crear el usuario: {repo_exc}")
            return UserMessageResponse(
                success=False,
                data=None,
                message=str(repo_exc),
                status=500
            )
        except Exception as e:
            logging.error(f"[service] Error inesperado al crear el usuario: {e}")
            return UserMessageResponse(
                success=False,
                data=None,
                message="Error interno al crear el usuario.",
                status=500
            )

    def update_user_status(self, user_id: int, user_update: UserUpdate):
        """Actualiza el estado activo de un usuario."""
        try:
            updated_user_id = self.user_repository.user_update_status(
                user_id=user_id,
                is_active=user_update.is_active
            )
            if updated_user_id is None:
                logging.warning(f"[Service] Usuario con ID {user_id} no encontrado para actualizar.")
                return UserMessageResponse(
                    success=False,
                    data=None,
                    message="Usuario no encontrado.",
                    status=404
                )

            logging.info(f"[Service] Estado del usuario con ID {user_id} actualizado exitosamente")

            return UserMessageResponse(
                success=True,
                data=updated_user_id,
                message="Estado del usuario actualizado exitosamente.",
                status=200
            )
        except RepositoryConnectionError as repo_exc:
            logging.error(f"[Service] Error la base de datos al actualizar el estado del usuario: {repo_exc}")
            return UserMessageResponse(
                success=False,
                data=None,
                message=str(repo_exc),
                status=500
            )
        except Exception as e:
            logging.error(f"[Service] Error inesperado al actualizar el estado del usuario: {e}")
            return UserMessageResponse(
                success=False,
                data=None,
                message="Error interno al actualizar usuario.",
                status=500
            )

    def login_user(self, user_login_data: UserLogin):
        """Inicia sesion de un usuario."""
        try:
            user = self.user_repository.get_user_by_email_or_username(
                user_login_data.email_or_username
            )
            if not user:
                logging.warning("[Service] Intento de inicio de sesion fallido - usuario no encontrado")
                return UserMessageResponse(
                    success=False,
                    data=None,
                    message="Credenciales invalidas.",
                    status=401
                )

            is_password_valid = verify_password(user_login_data.password, user["hashed_password"])

            if not is_password_valid:
                logging.warning("[Service] Intento de inicio de sesion fallido - credenciales invalidas")
                return UserMessageResponse(
                    success=False,
                    data=None,
                    message="Credenciales invalidas.",
                    status=401
                )

            logging.info(
                f"Usuario {user_login_data.email_or_username} ha iniciado sesion exitosamente")

            token = create_access_token(
                data={
                    "sub": user["username"],
                    "email": user["email"],
                    "user_id": user["id"],
                    "is_active": user["is_active"]
                }
            )
            return UserMessageResponse(
                success=True,
                data={
                    "user_id": user["id"],
                    "access_token": token,
                    "token_type": "bearer"
                },
                message="Inicio de sesion exitoso.",
                status=200
            )
        except RepositoryConnectionError as repo_exc:
            logging.error(f"[Service] Error en la base de datos al iniciar sesion: {repo_exc}")
            return UserMessageResponse(
                success=False,
                data=None,
                message=str(repo_exc),
                status=500
            )
        except Exception as e:
            logging.error(f"[Service] Error inesperado al iniciar sesion: {e}")
            return UserMessageResponse(
                success=False,
                data=None,
                message="Error interno al iniciar sesion.",
                status=500
            )
