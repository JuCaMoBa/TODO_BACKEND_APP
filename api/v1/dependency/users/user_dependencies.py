"""Modulo de dependencias para la gestion de usuarios"""

from fastapi import Depends
from api.v1.repositories.user_repository import UserRepository
from api.v1.controllers.user_controller import UserController
from api.v1.services.user_service import UserService
from core.settings.settings import settings


def get_user_repository():
    return UserRepository(settings.DB_URL)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)


def get_user_controller(user_service: UserService = Depends(get_user_service)):
    return UserController(user_service)
