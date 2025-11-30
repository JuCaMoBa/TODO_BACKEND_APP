"""Modulo que genera el modelo de datos para el login de usuarios"""

from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    """Modelo de datos para el login de un usuario"""
    email_or_username: str = Field(..., title="Email o Nombre de usuario")
    password: str = Field(..., title="Contrasena")
